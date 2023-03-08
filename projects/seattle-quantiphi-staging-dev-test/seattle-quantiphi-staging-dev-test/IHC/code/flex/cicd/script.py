"""
DataFlow Pipleline code
"""
import click
import logging
import os
import shutil
import psutil
from urllib.parse import quote
import time
import datetime
import pathlib
import json
from collections import Counter
from google.cloud import storage
import numpy as np
import pandas as pd
import openslide
import apache_beam as beam
from apache_beam.io import ReadFromText
from apache_beam.options.pipeline_options import PipelineOptions, SetupOptions
from core_utils.utils import load_file_gcs, predict_edge, predict_online, get_tiles, update_slide_dict, slide_heuristic
from core_utils.vis_utils import OverlayTool
import sys
import argparse
import logging
import re
spec_chars = [".", "^", "#",'!','@','$','%','*']

def extract_from_gcs(gcs_path):
    """Receives a GCS uri, downloads it and returns local path
    Args:
        path (str): GCS uri of the slide
    Returns:
        tuple(slide gcs path, local path of slide)
    """
    parent_dir = os.getcwd()
    folder_path = parent_dir+"/new_folder"
    destination_path = folder_path+"/"
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    logging.getLogger().setLevel(logging.INFO)
    logging.info("Getting file from GCS")
    logging.info("Mem Used : %s",\
                 str(round(psutil.virtual_memory().used/1024**3, 2))+ " GB")
    path = load_file_gcs(gcs_path, destination_path)
    return (gcs_path, path)

def tiling_transform(items, config_obj, automl_mode):
    """Loads the slide using Openslide and creates a tile generator
    Args:
        items (tuple): A tuple containing slide name and local path of slide
                        tuple(slide name, local path)
        config_obj (dict): Dict containing config parameters for the transform
        automl_mode (str): Which automl model is being used for prediction.
        ("online", "edge")
    Yields:
        tuple(slide name, {"tile_name": str, "tile": PIL.Image})
    """
    testing = False
    slide_path, path = items
    slide_name = _get_slide_name(slide_path)
    src_path=path
    inpt_filename=os.path.basename(path)
    dirname=os.path.dirname(path)
    name,extension=os.path.splitext(inpt_filename)
    #replaces special charcaters with '_'
    if any(special_chars in name for special_chars in spec_chars):
        replace_chars = re.sub('[.!^&@#$]', '_', name)
        path=os.path.join(dirname+'/' + replace_chars  + extension)
        os.replace(src_path,path)
    
    slide = openslide.OpenSlide(path)
    tile_size = (config_obj["tile_size"][0], config_obj["tile_size"][1])
    logging.getLogger().setLevel(logging.INFO)
    logging.info("Opened Slide")
    logging.info("Mem Used : %s",\
                 str(format(round(psutil.virtual_memory().used/1024**3, 2)))\
                 +"GB")
    for item in get_tiles(slide, tile_size, path, slide_name,
                          config_obj["batch_size"],automl_mode, testing):
        yield (slide_path, item)
def automl_predict(items, config_obj, automl_mode, test=False):
    """Gets prediction from the AutoML model
    Args:
        items (tuple): A tuple containing slide name and a batch of tiles/tile
                        tuple(slide path, {"tile_name": str, "tile": PIL.Image})
        config (dict): Dict containing config parameters for the transform
        automl_mode (str): Automl mode being used for
        prediction. ("online", "edge")
    Yields:
        tuple(slide path, "{tile_name(str): [predicted class (str),
        confidence (int)]}")
    """
    if automl_mode == "edge":
        slide_path, tile_batch = items
        predictions = predict_edge(tile_batch, config["edge"])
        for prediction in predictions:
            yield (slide_path, json.dumps(prediction))
    elif automl_mode == "online":
        slide_path, tile_dict = items
        if test:
            class_ = ["no_tissue", "no_tissue", "no_tissue",
                      "no_tissue", "no_tissue", "HE",
                      "out_of_focus", "negative"]
            score_ = [1.0, 1.0, 1.0, 1.0, 1.0, 0.9, 0.8, 0.7, 0.6]
            prediction = {tile_dict["tile_name"]: [np.random.choice(class_),
                                                   np.random.choice(score_)]}
        else:
            prediction = predict_online(tile_dict, config_obj["online"])
        yield (slide_path, json.dumps(prediction))
def combine_preds(preds):
    """Combines prediction from all the tiles into a single tile dict
    Args:
        preds (beam.iterator): List of all the predictions
        associated with a particular key (slide_name)
    Returns:
        tile_dict (dict): Dict containing tile name as
        key and predicted class as value
    """
    tile_dict = {}
    for pred in preds:
        if isinstance(pred, dict):
            tile_dict.update(pred)
        else:
            tile_dict.update(json.loads(pred))
    if len(tile_dict) > 0:
        return tile_dict
    else:
        return
def get_slide_preds(items):
    """Heuristic for collating tile predictions into slide level predictions.
    Args:
        items (tuple): Tuple containing slide_path and tile_dict
    Returns:
        tuple(slide path, slide dict)
    """
    slide_path, tile_dict = items
    slide_dict = {"slide_name": _get_slide_name(slide_path), "prediction": ""}
    tile_names, prediction = zip(*tile_dict.items())
    preds = [x[0] for x in prediction]
    counts = Counter(preds)
    frac_map = update_slide_dict(counts)
    prediction = slide_heuristic(frac_map)
    slide_dict.update(frac_map)
    slide_dict["prediction"] = prediction

    return (slide_path, slide_dict)

def store_tile_preds(items, output_path):
    """Creates dataframe with tile predictions and stores on GCS
    Args:
        items (tuple): Tuple containing slide_path and tile_dict
    Yields:
        tuple(slide path, tile dataframe to store on bigquery)
    """
    slide_path, tile_dict = items
    slide_name = _get_slide_name(slide_path)
    tile_names, prediction = zip(*tile_dict.items())
    preds = [x[0] for x in prediction]
    scores = [x[1] for x in prediction]
    x_coords = [int(x.split("_")[-2]) for x in tile_names]
    y_coords = [int(x.split("_")[-1][:-4]) for x in tile_names]
    slide_paths = [slide_path]*len(tile_names)
    slide_names = [slide_name]*len(tile_names)
    tile_df = pd.DataFrame({"slide_name": slide_name,
                            "slide_path": slide_path,
                            "x_coords": x_coords,
                            "y_coords": y_coords,
                            "preds": preds,
                            "confidence": scores})
    store_path = os.path.join(output_path,
                              "tile_preds/{}.csv".format(slide_name))
    tile_df.to_csv(store_path, index=False)
    yield (slide_path, tile_df)
def store_slide_preds(items, output_path):
    """Creates dataframe with slide predictions and stores on GCS
    Args:
        items (tuple): Tuple containing slide_path and slide_dict
    Yields:
        tuple(slide path, slide dataframe to store on bigquery)
    """
    slide_path, slide_dict = items
    slide_name = _get_slide_name(slide_path)
    bucket = storage.Client().get_bucket(output_path.split("/")[2])
    store_path = os.path.join("/".join(output_path.split("/")[3:]),
                              "slide_preds/{}.json".format(slide_name))
    blob = bucket.blob(store_path)
    blob.upload_from_string(
           data=json.dumps(slide_dict),
           content_type="application/json"
         )
    json_obj = {}
    for key in slide_dict:
        json_obj.update({key: [slide_dict[key]]})
    slide_df = pd.DataFrame(json_obj)
    yield (slide_path, slide_df)
def write_to_bigquery(items, table_id, output_path, style, viz_mode, job_name):
    """Function to write a dataframe to bigquery
    
    Args:
        items (tuple): Tuple containing slide path and dataframe
        table_id (str): Table ID in the format "dataset_id.table_id"

    Returns:
        N/A
    """
    path_prefix =  "/".join(output_path.split("/")[:3])
    slide_path, df = items
    slide_name = slide_path.rsplit("/", 1)[-1].rsplit(".", 1)[0]
    slide_name = quote(slide_name)
    store_path = os.path.join(output_path, viz_mode, style)
    store_path = os.path.join("/".join(store_path.split("/")[3:]), "{}.png".format(slide_name))
    store_path = path_prefix+"/"+store_path
    if not 'x_coords' in df.columns:
        viz_path = "https://storage.cloud.google.com/"+store_path[5:]
        df['visualization_path'] = viz_path
        df['created'] = datetime.datetime.now()
    else:
        df['slide_path'] = slide_path
    df['job_name'] = job_name
    df.to_gbq(table_id, 
                'ihc-qc-sandbox',
                chunksize=None,
                if_exists='append',
                progress_bar=False)
    return
def store_on_gcs(items, output_path, automl_mode):
    """
    Store the image tiles in GCS.
    Args:
        items: Tuple of slide path and a batch of tiles.
                tuple(slide name, {"tile_name": str, "tile": PIL.Image})
        output_path (str): Output GCS path for storing the tiles
        automl_mode (str): Automl mode being used for
        prediction. ("online", "edge")

    Returns:
        N/A
    """
    slide_name = _get_slide_name(items[0])
    store_path = os.path.join(output_path, slide_name)
    if automl_mode == "edge":
        #slide_path, tile_batch = items
        tile_batch = items[1]
        for tile in tile_batch:
            store_path = os.path.join(output_path, slide_name)
            store_path = os.path.join(store_path, tile["tile_name"])
            tile_1 = tile["tile"]
            with beam.io.gcp.gcsio.GcsIO().open(store_path, "wb") as f:
                logging.getLogger().setLevel(logging.INFO)
                logging.info("new tile is saved as %s.png", f)
                tile_1.save(f, "PNG", quality=100)
    elif automl_mode == "online":
        #slide_path, tile = items
        tile = items[1]
        store_path = os.path.join(store_path, tile["tile_name"])
        tile_1 = tile["tile"]
        with beam.io.gcp.gcsio.GcsIO().open(store_path, "wb") as f:
            logging.getLogger().setLevel(logging.INFO)
            logging.info("new tile is saved as %s.png", f)
            tile_1.save(f, "PNG", quality=100)
def _get_slide_name(path):
    """Helper function to return the slide name from the path of the slide
    """
    if path.endswith(".svs"):
        slide_name = path.rsplit("/", 1)[1][:-4]
    elif path.endswith(".qptiff"):
        slide_name = path.rsplit("/", 1)[1][:-7]
    return slide_name
def pred_overlay(item, cmap_name, image_size):
    """Call pred_overlay from viz_utils
    item (tuple) -     item[0] slide path
    item[1] pred_df
    """
    slide_path = item[0]
    pred_df = item[1]
    #create a new local folder - viz_temp
    parent_dir = os.getcwd()
    folder_path = parent_dir+"/viz_temp"
    destination_path = folder_path+"/"
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    logging.getLogger().setLevel(logging.INFO)
    logging.info("Getting file from GCS")
    logging.info("Mem Used : %s",\
                 str(round(psutil.virtual_memory().used/1024**3, 2)) +"GB")
    path = load_file_gcs(slide_path, destination_path)
    path_to_slide_on_machine = path   ##destination path
    output_dir =parent_dir+"/viz_output"
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    output_dir_slide = parent_dir+"/slide_output"
    if not os.path.exists(output_dir_slide):
        os.mkdir(output_dir_slide)
    pred_df["preds"] = pred_df["preds"].apply(lambda x: x.lower().
                                              replace(" ", "_"))
    pred_df["preds"] = pred_df["preds"].apply(lambda x: x.
                                              replace("necrotic", "exclusion"))
    pred_df.drop(columns=["slide_path"], inplace=True)
    obj_pred = OverlayTool(pred_df, output_dir,
                               path_to_slide_on_machine, cmap_name)
    dir1 =output_dir+"/color_maps"
    if not os.path.exists(dir1):
        os.mkdir(dir1)
    dir2 =output_dir_slide+"/slide_only"
    if not os.path.exists(dir2):
        os.mkdir(dir2)
    fig_multiplier = image_size/150
    obj_pred.plot_merged(fig_multiplier=fig_multiplier,
                             save_to_dir=output_dir) ##plot_slide_only also
    obj_pred.plot_slide_only(fig_multiplier=fig_multiplier,
                                 save_to_dir=output_dir_slide)
    slide_name = slide_path.rsplit("/", 1)[-1]
    logging.getLogger().setLevel(logging.INFO)
    logging.info("slide_name %s",slide_name)
    logging.info("output_dir %s",dir1)
    os.remove(path_to_slide_on_machine)
    yield (slide_name, dir1, dir2)
def save_visualization(items, output_path, style, viz_mode):
    """
    Store final visualization on GCS bukcet
    Args:
    items: Tuple of slide path and local path of png output
                tuple(slide name, local_path)
    output_path (str): Output GCS path for storing the tiles
    tyle(str): String of different styles to print
                        slide_only / color_maps
    viz_mode (str): Visulaisation mode being used
    for prediction. ("gt", "edge")
    Returns:
    N/A
    """
    source_path = items[1]
    slide_only_path = items[2]
    slide_name = items[0].rsplit(".", 1)[0]
    source_path = os.path.join(source_path,"{}.png".format(slide_name))
    slide_only_path = os.path.join(slide_only_path,
                                   "{}.png".format(slide_name))
    logging.getLogger().setLevel(logging.INFO)
    logging.info("source_path %s",source_path)
    logging.info("slide_only_path %s", slide_only_path)
    store_path = os.path.join(output_path, viz_mode)
    bucket = storage.Client().get_bucket(output_path.split("/")[2])
    store_path = os.path.join(output_path,viz_mode,style)
    store_path_slide = os.path.join("/".join(store_path.split("/")[3:-1]),
                                        "slide_only/{}.png".format(slide_name))
    store_path = os.path.join("/".join(store_path.split("/")[3:]),
                                  "{}.png".format(slide_name))
    logging.getLogger().setLevel(logging.INFO)
    logging.info("store_path %s", store_path)
    blob = bucket.blob(store_path)
    blob.upload_from_filename(source_path)
    blob2 = bucket.blob(store_path_slide)
    blob2.upload_from_filename(slide_only_path)

def download_from_gcs(project_id, file_url, save_file):
    
    bucket_name = file_url.split("/")[2]
    bucket_path_temp = file_url.split("/")[3:]
    bucket_path = "/".join(bucket_path_temp)
    # Initialise a client
    storage_client = storage.Client(project_id)
    # Create a bucket object for our bucket
    bucket = storage_client.get_bucket(bucket_name)
    # Create a blob object from the filepath
    blob = bucket.blob(bucket_path)
    # Download the file to a destination
    blob.download_to_filename(save_file)
    
def run(config_obj, input_path, output_path):
    """
    Function for building and deploying the pipeline
    based on the config provided.
    Args:
        config (dict): Configuration for the
        pipeline and its functions
    Returns:
        N/A
    """
    automl_mode = config_obj["pipeline_config"]["automl_mode"]
    is_test = config_obj["function_config"]\
    ["automl_prediction"]["online"]["test"]
    click.echo("Running job: {}".
               format(config_obj["pipeline_config"]["job_name"]))
    now = time.strftime("%Y%m%d-%H%M%S")
    job_name = config_obj["pipeline_config"]["job_name"] + f"-{now}"
    output_path = os.path.join(output_path, job_name)
    if config_obj["pipeline_config"]["run_local"]:
        runner_options = {
            "runner": "DirectRunner",
        }
    else:
        runner_options = {
            "runner": "DataflowRunner",
            "temp_location": os.path.join(output_path, "temp_location"),
            "staging_location": os.path.join(output_path, "staging_location"),
            "max_num_workers": config_obj["pipeline_config"]["max_num_workers"],
            "machine_type": config_obj["pipeline_config"]["machine_type"],
            "num_workers": config_obj["pipeline_config"]["num_workers"],
            "network": config_obj["environment"]["network"],
            "subnetwork": config_obj["environment"]["subnetwork"]
        }
    options = PipelineOptions(
        project=config_obj["pipeline_config"]["project_id"],
        job_name=job_name,
        region=config_obj["pipeline_config"]["region"],
        **runner_options
    )
    options.view_as(SetupOptions).save_main_session = True
    options.view_as(SetupOptions).setup_file = os.path.join(
        pathlib.Path(__file__).parent.absolute(), "setup.py")
    logging.getLogger().setLevel(logging.INFO)
    logging.info("Building Pipeline........")
    with beam.Pipeline(options=options) as p:
        tiled_img = (p
             | "source" >> ReadFromText(input_path)
             | "extract_from_gcs" >> beam.Map(extract_from_gcs)
             | "tiling_transform" >> beam.ParDo(tiling_transform,
                                                config_obj["function_config"]
                                                ["tiling_transform"],
                                                automl_mode))
        if config_obj["pipeline_config"]\
        ["store_tiled_img"]:
            _ = (tiled_img | "store_tile_on_gcs" >>\
                 beam.Map(store_on_gcs,output_path,automl_mode))
        predictions = (tiled_img | "automl_prediction" >>
                       beam.ParDo(automl_predict, config_obj["function_config"]
                                                          ["automl_prediction"],
                                                          automl_mode, is_test)
                      | "combine_preds" >> beam.CombinePerKey(combine_preds))
        output_tile_preds = (predictions
                        | "store_tile_preds" >>
                             beam.ParDo(store_tile_preds, output_path))
        output_slide_preds = (predictions
                            | "get_slide_preds" >> beam.Map(get_slide_preds)
                            | "store_slide_preds" >>
                              beam.ParDo(store_slide_preds, output_path))
        _ = (output_tile_preds
                              | "create_overlay" >>
                          beam.ParDo(pred_overlay, config_obj["function_config"]
                                     ["visualization"]["cmap_name"],
                                     config_obj["function_config"]
                                     ["visualization"]["image_size"])
                         | "store_on_gcs" >>
                          beam.Map(save_visualization,
                                   output_path, "color_maps" ,"edge"))
        if config_obj["function_config"]\
        ["store_on_bigquery"]["store_tile_preds"]:
            _ = (output_tile_preds | "write_tile_preds_gbq" >>
                 beam.Map(write_to_bigquery,
                          config_obj["function_config"]\
                          ["store_on_bigquery"]
                          ["tile_level_preds"], output_path, "color_maps" ,"edge", job_name))
        if config_obj["function_config"]["store_on_bigquery"]\
        ["store_slide_preds"]:
            _ = (output_slide_preds | "write_slide_preds_gbq" >>
                 beam.Map(write_to_bigquery,
                          config_obj["function_config"]\
                          ["store_on_bigquery"]["slide_level_preds"], output_path, "color_maps", "edge", job_name))

if __name__ == "__main__":
    
    """Main entry point; defines and runs the pipeline."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--config_file', dest='config_file', required=False, help='Full GCS location for input CSV')
    parser.add_argument('--input_path', dest='input_path', required=False, help='Full GCS location for input CSV')
    parser.add_argument('--output_path', dest='output_path', required=False, help='Destination GCS path for storing results')

    known_args, pipeline_args = parser.parse_known_args(sys.argv)

    #config_file =  known_args.config_file
    
    download_from_gcs("ihc-qc-sandbox", known_args.config_file, "config.json")
    
    with open("./config.json", "r") as config_f:
        config = json.load(config_f)
    logging.info("config - %s", config)
    run(config, known_args.input_path, known_args.output_path)
