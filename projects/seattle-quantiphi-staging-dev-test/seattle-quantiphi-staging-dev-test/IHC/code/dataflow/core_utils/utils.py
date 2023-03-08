import base64
import io
import json
import requests
import math
import os
import base64
from io import BytesIO

from PIL import Image
import numpy as np

from google.cloud import storage
from google.cloud import automl

def load_file_gcs(gcs_path, destination_path):
    """
    loads  object in Google Cloud Storage bucket to local
    
    Args:
        gcs_path(str): path to file in gcs bucket
        destination_path(str): path to local directory to store the file
    
    Returns:
        local file path for the file
    """
    bucket_name = gcs_path.split('/')[2]       #extract bucket name
    source_blob_path = '/'.join(gcs_path.split('/')[3:])       #extract folder structure
    filename = source_blob_path.split('/')[-1]      #extract file name
    storage_client = storage.Client("[ihc_qc_sanbox]")
    # Create a bucket object for our bucket
    bucket = storage_client.get_bucket(bucket_name)
    # Create a blob object from the filepath
    blob = bucket.blob(source_blob_path)
    # Download the file to a destination
    blob.download_to_filename(destination_path+filename)
    print("Slide Loaded from GCS bucket as {}".format(destination_path+filename))
    return str(destination_path+filename)
    

def get_slide_region(slide, origin=(0,0), region_size=None, level_to_pull=0, as_numpy=False):
    """ Pull a specific region from a OpenSlide Object 
    
    Args:
        slide (OpenSlide Object): Image slide to pull tile from
        origin (tuple of ints, optional): Top left corner of the tile within
            the full original image
        region_size (tuple of ints, optional): Width and height of the tile
            we wish to extract from the slide image
        level_to_pull (int, optional): Which level of the svs slide we want to pull from
        as_numpy (bool, optional): Whether to convert to a numpy array (uint8) prior to returning
    
    Returns:
        Extracted tile from the origina slide image (either as a PIL Image or a ndarray)
    """
    if not region_size:
        region_size=slide.level_dimensions[level_to_pull]
    
    tile = slide.read_region(location=origin, 
                             level=level_to_pull, 
                             size=region_size).convert('RGB')
    if not as_numpy:
        return tile
    else:
        return np.asarray(tile, dtype=np.uint8)

def get_tiles(slide, tile_size, path, slide_name, batch_size, automl_mode, testing=False):
    """Loops over the slide and generates tiles.
    
    Args:
        slide (OpenSlide Object): Image slide to pull tile from
        tile_size (list): Height, width of the tiles to be extracted
        path (str): local path of the svs or qptiff image
        slide_name (str): Name of the slide
        batch_size (int): Number of tiles to be added in a single batch for automl edge prediction
        automl_mode (str): The automl mode being used for preediction
        testing (bool): To prevent looping through the whole slide, set testing=True
    
    Yields:
        Tile dict / Batch of tile dicts: {"tile_name": str, "tile": PIL.Image}
    """
    w, h = slide.dimensions
    pad_w, pad_h = math.ceil(w/tile_size[0])*tile_size[0], math.ceil(h/tile_size[1])*tile_size[1]
    #print(f"Original is {pad_w} by {pad_h} pixels")
    i = 0
    tile_batch = []
    for x in range(0, pad_w, tile_size[0]):
        for y in range(0, pad_h, tile_size[1]):
            tile = get_slide_region(slide, origin=(x,y), 
                                    region_size=tile_size, level_to_pull=0)
            
            tile_dict = {"tile_name": f"{slide_name}_{x:05}_{y:05}.png", "tile": tile}
            if automl_mode == "edge":
                tile_batch.append(tile_dict)
                if len(tile_batch) >= batch_size:
                    yield tile_batch
                    tile_batch = []
            
            elif automl_mode == "online":
                yield tile_dict
            
            ## For testing only
            print(i, end="\r")
            i += 1
            if i > 4 and testing==True:
                del slide
                os.remove(path)
                return
    
    ## Clean up the storage
    if automl_mode == "edge" and len(tile_batch) > 0:
        del slide
        os.remove(path)
        return tile_batch
    else:
        del slide
        os.remove(path)
        return
    
def predict_edge(tile_batch, config):
    """Generates automl edge prediction for tiles.
    
    Args:
        tile_batch (list): Batch of tile dicts in the format {"tile_name": "abc", "tile": PIL.Image}.
        config (dict): Configuration for automl edge prediction
    Yields:
        dict{tile name: [predicted class, confidence]}
    """
    
    url = config["endpoint"]
    thresh = config["confidence_threshold"]
    #encoded_image = base64.b64encode(item["tile"].tobytes()).decode('utf-8')
    instances = []
    for tile in tile_batch:
        buffered = BytesIO()
        tile["tile"].save(buffered, format="PNG")
        encoded_image = base64.b64encode(buffered.getvalue()).decode("utf-8")
        instances.append(
                        {'image_bytes': {'b64': str(encoded_image)},
                         'key': tile["tile_name"]}
        )
    _instances = {"instances": instances}
    response = requests.post(url, data=json.dumps(_instances))
    res = response.json()
    preds = []
    for pred in res["predictions"]:
        if max(pred["scores"]) >= thresh:
            prediction = pred['labels'][np.argmax(pred["scores"])]
            prediction = necrotic_to_exclusion(prediction)
            score = round(max(pred["scores"]), 2)
            yield {pred["key"]: [prediction, score]}
        else:
            prediction = "uncertain"
            score = round(max(pred["scores"]), 2)
            yield {pred["key"]: [prediction, score]}

def predict_online(tile_dict, config):
    """Generates automl online prediction for tiles.
    
    Args:
        tile_dict (dict): Tile dict in the format {"tile_name": "abc", "tile": PIL.Image}
        config (dict): Configuration for automl online prediction
    Yields:
        dict{tile name: [predicted class, confidence]}
    """
    prediction_client = automl.PredictionServiceClient()
    buffered = BytesIO()
    tile_dict["tile"].save(buffered, format="PNG")
    encoded_image = buffered.getvalue()
    image = automl.Image(image_bytes=encoded_image)
    payload = automl.ExamplePayload(image=image)
    params = {"score_threshold": "0.0"}

    request = automl.PredictRequest(
        name='projects/{}/locations/us-central1/models/{}'.format(config["project_id"], config["model_id"]),
        payload=payload,
        params=params
    )
    response = prediction_client.predict(request=request)

    labels = []
    scores = []
    #print(response.payload)
    for result in response.payload:
        labels.append(result.display_name)
        scores.append(result.classification.score)
    prediction = labels[np.argmax(scores)]
    score = round(max(scores), 2)
    if score >= config["confidence_threshold"]:
        return {tile_dict["tile_name"]: [prediction, score]}
    else:
        return {tile_dict["tile_name"]: ["uncertain", 0.]}

    
def slide_heuristic(frac_map, 
                    str_thresh=0.150,
                    oof_thresh=0.015,
                    dim_thresh=0.225,
                    neg_thresh=0.225,
                    he_thresh=0.225,
                    not_thresh=0.99,):
    """
    Heuristics/Decision Tree to obtain a slide level predictions based on the fraction cover of different classes
    """
        # FRAC MAP is {class:perct, ...}
    if frac_map.get("no_tissue", 0.0) <= not_thresh:
        if frac_map.get("strong_positive", 0.0) <= str_thresh:
            if frac_map.get("out_of_focus", 0.0) <= oof_thresh:
                if frac_map.get("dim_positive", 0.0)+frac_map.get("strong_positive", 0.0) <= dim_thresh:
                    if frac_map.get("negative", 0.0) <= neg_thresh:
                        if frac_map.get("HE", 0.0) <= he_thresh:
                            return "uncertain"
                        else:
                            return "HE"
                    else:
                        return "negative"
                else:
                    return "dim_positive"
            else: 
                return "out_of_focus"
        else:
            return "strong_positive"
    else:            
        return "no_tissue"
    
def update_slide_dict(tile_counts):
    """
    Updates the tile counts to fraction map
    """
    CLASS_LIST = ["no_tissue", "HE", "out_of_focus", "dim_positive", "strong_positive", "negative", "exclusion", "uncertain"]
    frac = {k:0.0 for k in CLASS_LIST}
    frac.update(tile_counts)
    n_tiles = sum(frac.values())
    n_tiles_w_tissue = sum([v for k,v in frac.items() if k!="no_tissue"])
    
    if n_tiles_w_tissue == 0:
        frac["no_tissue"] = frac["no_tissue"]/n_tiles
        return frac
    
    frac_final = {k:v/n_tiles_w_tissue for k,v in frac.items()}
    frac_final["no_tissue"] = frac["no_tissue"]/n_tiles
    return frac_final

def necrotic_to_exclusion(label):
    """
    """
    if label == "necrotic":
        return "exclusion"
    else:
        return label