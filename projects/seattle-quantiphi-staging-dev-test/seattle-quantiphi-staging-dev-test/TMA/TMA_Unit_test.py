#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Data Science Imports
import pandas as pd
import numpy as np
import tensorflow as tf
import random

# Microscopy Related Imports
import openslide
import tifffile

# Cloud Related Imports
from google.protobuf.struct_pb2 import Value
from google.protobuf import json_format
from google.cloud import aiplatform
from google.cloud import storage
from google.cloud import bigquery
import apache_beam as beam
from apache_beam.io import ReadFromText
from apache_beam.io.gcp.gcsio import GcsIO
from apache_beam.options.pipeline_options import PipelineOptions, SetupOptions

# Visualization Imports
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
import matplotlib.pyplot as plt
from tqdm.notebook import tqdm
import seaborn as sns
from PIL import Image
import cv2
import skimage; import skimage.color; import skimage.filters;

# Built In Imports
import base64
import glob
import os
import gc
import time
import logging
import json
import click
import pathlib
import multiprocessing


# Custom file imports #, predict_image_object_detection_sample
from core_utils.utils import load_file_gcs, get_bb_lbl_map_2, save_cores_to_disk, plot_image, predict_image_object_detection_sample, get_bbox_from_svs, predict_cloud_model, predict_cloud_model_2, preprocess_cd228, preprocess_slc1a5, postprocess_slc1a5


"""
Testing with one image - gs://ihc_dataset/ChampionsTMA_21-24/26103_TMA21.svs
local
"""


def extract_from_gcs(gcs_path):
    """Receives a GCS uri, downloads it and returns local path
    
    Args:
        path (str): GCS uri of the slide
    
    Returns:
        tuple(slide gcs path, local path of slide)
    """
    
    parent_dir = os.getcwd()
    folder_path = parent_dir+"/cores"
    destination_path = folder_path+"/"
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    print("Getting file from GCS", flush=True)
   # print(f"Mem Used : {round(psutil.virtual_memory().used/1024**3, 2)} GB")
    path = load_file_gcs(gcs_path, destination_path)
    
    return (gcs_path, path)

def open_svs(items, extra_dwn=3):
    """ Simple function to open an SVS image and downscale
    
    Args:
        path (str): Path to the svs file to be returned
        extra_dwn (int, optional): The additional factor to downscale by
    
    Return:
        PIL Image of the downsampled image, downsample factor, downsampled dimensions
    """
    
    # Open the image and get the lowest tier dimensions and respective
    # downsampling factor
    gcs_path, path = items
    
    slide = openslide.OpenSlide(path)
    new_dims = slide.level_dimensions[-1]
    dwn_sample = slide.level_downsamples[-1]
    
    name = path.rsplit("/", 1)[-1].rsplit(".", 1)[0]
    
    # Perform extra-downsampling (or not) and return the 
    if not extra_dwn:
        return (slide.read_region((0,0), slide.level_count-1, new_dims), slide.level_downsamples[-1], slide.level_dimensions[-1], name)
    else:
        new_dims = tuple([int(round(dim/extra_dwn)) for dim in new_dims])
        dwn_sample = slide.dimensions[0]/new_dims[0]
        im_original = Image.fromarray(cv2.resize(np.asarray(slide.read_region((0,0), slide.level_count-1, slide.level_dimensions[-1])), new_dims, cv2.INTER_AREA))
        im_original.save(f"{name}_Original_{new_dims[0]}_{new_dims[1]}.png", "PNG")
        
        im_RGB = im_original.convert('RGB')
        im_RGB.save(f"{name}_RGB_{new_dims[0]}_{new_dims[1]}.jpeg")  
        
        im_Gray = im_original.convert('L')
        im_Gray.save(f"{name}_Gray_{new_dims[0]}_{new_dims[1]}.jpeg")
        
        return (gcs_path, new_dims, name, path)

def store_on_gcs(items, output_path):
    """
    Store the image in GCS.
    
    Args:
        items: Tuple of slide path and a batch of tiles.
                tuple(slide name, {"tile_name": str, "tile": PIL.Image})
        output_path (str): Output GCS path for storing the image

    Returns:
        N/A
    """
    gcs_path, new_dims, name , path = items  
    file_name = f"{name}_Original_{new_dims[0]}_{new_dims[1]}.png"
    im_original = Image.open(file_name)
    store_path = os.path.join(output_path, file_name)

    with beam.io.gcp.gcsio.GcsIO().open(store_path, 'wb') as f:
        print("new image is saved as {}.png ".format(f))
        im_original.save(f, "PNG", quality=100)
    return store_path

def store_viz_on_gcs(items, output_path):
    """
    Store the image in GCS.
    
    Args:
        items: Tuple of slide path and a batch of tiles.
                tuple(slide name, {"tile_name": str, "tile": PIL.Image})
        output_path (str): Output GCS path for storing the image

    Returns:
        N/A
    """
    core_directory, filename, gcs_path, destination_path_cd228, destination_path_slc1a5,image_class = items
    
    print('&&&&&&&&&&&&&&&&&&& ', destination_path_cd228)
    
    file_name_cd228 = destination_path_cd228.rsplit("/", 1)[-1][6:]
    file_name_slc1a5 = destination_path_slc1a5.rsplit("/", 1)[-1][7:]
    
    im_cd228 = Image.open(destination_path_cd228)
    im_slc1a5 = Image.open(destination_path_slc1a5)
    
    store_path_cd288 = os.path.join(output_path, "cd228",core_directory , file_name_cd228)
    store_path_slc1a5 = os.path.join(output_path, "slc1a5",core_directory, file_name_slc1a5)

    with beam.io.gcp.gcsio.GcsIO().open(store_path_cd288, 'wb') as f:
        print("new image is saved as {}.png ".format(f))
        im_cd228.save(f, "PNG", quality=100)
    
    with beam.io.gcp.gcsio.GcsIO().open(store_path_slc1a5, 'wb') as f:
        print("new image is saved as {}.png ".format(f))
        im_slc1a5.save(f, "PNG", quality=100)
    
    os.remove(destination_path_cd228)
    os.remove(destination_path_slc1a5)
    print(core_directory+"   "+ store_path_cd288+"  " +store_path_slc1a5)
    yield (core_directory ,filename, gcs_path, store_path_cd288, store_path_slc1a5,image_class)

#gunjan - code start 
#create label map
def get_bbox_cp (items):
    gcs_path, confidences, bboxes , path_to_resized, path, image_class = items
    print("path_to_resized   "+path_to_resized )
    print(" local path for original image " + path )
    bb_lbl_map = get_bb_lbl_map_2(path_to_resized, confidences, bboxes, C_THRESH = config["function_config"]["visualization"]["C_THRESH"], dy_frac = config["function_config"]["visualization"]["dy_frac"], tl_find_mult = config["function_config"]["visualization"]["tl_find_mult"],do_nms = config["function_config"]["visualization"]["do_nms"])
    yield (bb_lbl_map, path_to_resized, path, gcs_path,image_class)

#plot visualisation    
def _plot_merged (items , output_path):
    bb_lbl_map = items[0]
    name = items[1]
    #path = items[2]
    #path_to_resized = os.path.join(path,name)
    print("name "+ name)
    plt = plot_image(bb_lbl_map, path_to_resized = name, opacity = config["function_config"]["plot_figure"]["opacity"], cmap = config["function_config"]["plot_figure"]["cmap"],plot_row_boundaries = config["function_config"]["plot_figure"]["plot_row_boundaries"],plot_box_midline = config["function_config"]["plot_figure"]["plot_box_midline"],
upper_cp = config["function_config"]["plot_figure"]["upper_cp"])
    #store_path = os.path.join(output_path, path_to_resized.rsplit("/", 1)[1] )
    store_path = os.path.join(output_path,"viz_output", name )
    with beam.io.gcp.gcsio.GcsIO().open(store_path, "wb") as f:
        logging.getLogger().setLevel(logging.INFO)
        #logging.info("new tile is saved as %s.png", f)
        logging.info("new image is saved as {}.png ".format(f))
        plt.savefig(fname = f) 
        
def save_to_gcs(img ,row_idx , row_ltr):
    save_as_rgb = config["function_config"]["visualization"]["save_cores_rgb"]
    tma_subdir, file_name = local_svs_path.rsplit(".", 1)[0].rsplit("/", 2)[1:]
    output_dir = os.path.join(output_path, tma_subdir, file_name)
    individual_core_fname = os.path.join(output_dir, f"{file_name}__{row_ltr}{row_idx:02}.jpg")
    if save_as_rgb:
        img = img.convert("RGB")
        individual_core_fname = individual_core_fname.replace(".jpg", "_rgb.png")
    else:
        img = img.convert("L")
        individual_core_fname = individual_core_fname.replace(".jpg", "_gray.png")
    with beam.io.gcp.gcsio.GcsIO().open(individual_core_fname, "wb") as f:
        img.save(f,"PNG", quality=100)       
        

def predict_cloud_model(    
    items,
    project: str,
    endpoint_id: str, 
    C_THRESH,
    location: str = "us-central1",
    api_endpoint: str = "us-central1-prediction-aiplatform.googleapis.com",
    instance_dict: dict = None
    
):
    """ Get predictions from Google AIPlatform Endpoint """
    client_options = {"api_endpoint": api_endpoint}
    
    # Initialize client that will be used to create and send requests.
    # This client only needs to be created once, and can be reused for multiple requests.
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)
    
    gcs_path, new_dims, name , local_svs_path = items
    filename = f"{name}_Original_{new_dims[0]}_{new_dims[1]}.png"
    with open(filename, "rb") as f:
        file_content = f.read()

    # The format of each instance should conform to the deployed model's prediction input schema.
    encoded_content = base64.b64encode(file_content).decode("utf-8")
    
    if not instance_dict:
        instance_dict = {"content": encoded_content}
    
    instance = json_format.ParseDict(instance_dict, Value())
    instances = [instance]
    # See gs://google-cloud-aiplatform/schema/predict/params/image_object_detection_1.0.0.yaml for the format of the parameters.
    parameters_dict = {"confidenceThreshold": C_THRESH, "maxPredictions": 200}
    parameters = json_format.ParseDict(parameters_dict, Value())
    endpoint = client.endpoint_path(
        project=project, location=location, endpoint=endpoint_id
    )
    response = client.predict(
        endpoint=endpoint, instances=instances, parameters=parameters,
    )
    print("response")
    print(" deployed_model_id:", response.deployed_model_id)
    # See gs://google-cloud-aiplatform/schema/predict/prediction/image_object_detection.yaml for the format of the predictions.
    preds = response.predictions
    preds, label = {k:v for k,v in preds[0].items()}, preds[0]["displayNames"][np.argmax(preds[0]["confidences"])]   
    print(preds, label)
    #class_ = ["not_tma","tma"]
    #class_ = ["tma"]
    #label = np.random.choice(class_)
    return (gcs_path,label,filename,local_svs_path)




#*************************************************Create testing functions**************************

#Testing extract_from_gcs


##dict parameters
#key -test_extract_from_gcs
#value - tuple - input/output

def test_extract_from_gcs():
    assert extract_from_gcs("gs://ihc_dataset/ChampionsTMA_21-24/26103_TMA21.svs") ==    ("gs://ihc_dataset/ChampionsTMA_21-24/26103_TMA21.svs","/home/jupyter/seattle-quantiphi/TMA/cores/26103_TMA21.svs")

#Testing test_open_svs

def test_open_svs():
    assert open_svs(("gs://ihc_dataset/ChampionsTMA_21-24/26103_TMA21.svs",'/home/jupyter/seattle-quantiphi/TMA/cores/26103_TMA21.svs'),extra_dwn=3) == ('gs://ihc_dataset/ChampionsTMA_21-24/26103_TMA21.svs', (1120,796), '26103_TMA21', '/home/jupyter/seattle-quantiphi/TMA/cores/26103_TMA21.svs')

    
#Testing test_store_on_gcs

def test_store_on_gcs():
    assert store_on_gcs(('gs://ihc_dataset/ChampionsTMA_21-24/26103_TMA21.svs',
 (1120, 796),
 '26103_TMA21',
 '/home/jupyter/seattle-quantiphi/TMA/cores/26103_TMA21.svs'),"gs://seagen-quantiphi/temp/Gunjan") ==\
                        ('gs://seagen-quantiphi/temp/Gunjan/26103_TMA21_Original_1120_796.png')


#Testing test_predict_cloud_model

def test_predict_cloud_model():
    assert predict_cloud_model (('gs://ihc_dataset/ChampionsTMA_21-24/26103_TMA21.svs',
 (1120, 796),
 '26103_TMA21',
 '/home/jupyter/seattle-quantiphi/TMA/cores/26103_TMA21.svs'),"ihc-qc-sandbox","9222861863459487744","0.025")==\
    ('gs://ihc_dataset/ChampionsTMA_21-24/26103_TMA21.svs',
 'tma',
 '26103_TMA21_Original_1120_796.png',
 '/home/jupyter/seattle-quantiphi/TMA/cores/26103_TMA21.svs')
    
#Testing test_predict_image_object_detection_sample

def test_predict_image_object_detection_sample():
    assert predict_image_object_detection_sample(('gs://ihc_dataset/ChampionsTMA_21-24/26103_TMA21.svs',\
 'tma',\
  '26103_TMA21_Original_1120_796.png',
 '/home/jupyter/seattle-quantiphi/TMA/cores/26103_TMA21.svs'),
    "ihc-qc-sandbox",
    "4721514035902676992",
    "0.025")==('gs://ihc_dataset/ChampionsTMA_21-24/26103_TMA21.svs',
 array([0.99995112, 0.99990678, 0.99986875, 0.99985087, 0.99984658,
        0.99974412, 0.99970066, 0.99969792, 0.99968314, 0.9996438 ,
        0.99962533, 0.99952054, 0.99952006, 0.99950874, 0.99950862,
        0.99950504, 0.99944872, 0.99943989, 0.99940836, 0.99939978,
        0.99937159, 0.99935085, 0.9993487 , 0.99926394, 0.99912924,
        0.99910623, 0.9990809 , 0.99904484, 0.9990446 , 0.99903393,
        0.99901295, 0.99897718, 0.9989692 , 0.99894637, 0.99893409,
        0.9988789 , 0.99887782, 0.99885488, 0.9988243 , 0.99878687,
        0.99874228, 0.99869627, 0.99869174, 0.998691  , 0.99868196,
        0.99863142, 0.99862349, 0.99860829, 0.99859756, 0.99857831,
        0.99855703, 0.99854809, 0.99844933, 0.99843627, 0.99840945,
        0.99835867, 0.9983387 , 0.99832922, 0.9983241 , 0.99831748,
        0.99831426, 0.99786747, 0.99782085, 0.99776888, 0.9977228 ,
        0.99767584, 0.99758267, 0.99747783, 0.99745351, 0.9973864 ,
        0.99728215, 0.99720925, 0.99695456, 0.99695063, 0.99658585,
        0.99656326, 0.99646133, 0.99635327, 0.99634486, 0.996318  ,
        0.99624443, 0.99612915, 0.995924  , 0.99588156, 0.99579054,
        0.99563968, 0.9954015 , 0.99528474, 0.99481225, 0.994491  ,
        0.9944036 , 0.99415368, 0.99404657, 0.9939884 , 0.99386036,
        0.99317729, 0.99276769, 0.99216968, 0.99206841, 0.99133331,
        0.99114311, 0.99075365, 0.99007684, 0.98963869, 0.98909658,
        0.98874378, 0.98845041, 0.98688835, 0.98653191, 0.98578578,
        0.98346275, 0.98278272, 0.981198  , 0.97871405, 0.97837925,
        0.976585  , 0.970554  , 0.96708429, 0.96436763, 0.96242434,
        0.95864242, 0.95464307, 0.9527809 , 0.95068312, 0.94738275,
        0.92873812, 0.92491537, 0.92212915, 0.92071855, 0.91303116,
        0.89838463, 0.89426136, 0.88884491, 0.88288593, 0.880806  ,
        0.88049322, 0.7790879 , 0.7670384 , 0.74086249, 0.53647894,
        0.39647675, 0.39324519, 0.37727615, 0.30645695, 0.28255829,
        0.17866117, 0.15719078, 0.14612211, 0.13620664, 0.13107878,
        0.13029148, 0.12236376, 0.10887055, 0.07924014, 0.06121022,
        0.06116582, 0.05859731, 0.05776211, 0.04910345, 0.04228069,
        0.03979046, 0.03559705, 0.03473111, 0.03208411, 0.02524013,
        0.0207602 , 0.02068326, 0.0182409 , 0.01760214, 0.01542783,
        0.01454632, 0.01439474, 0.01369738, 0.01271428, 0.01145166,
        0.01139574, 0.00990697, 0.00972274, 0.00923766, 0.00627804,
        0.00553907, 0.00545226, 0.0052857 , 0.00523446, 0.00521425,
        0.00497657, 0.00487907, 0.00478198, 0.00467652, 0.00462452,
        0.00461941, 0.00404241, 0.00403948, 0.00377697, 0.00356937,
        0.00346809, 0.00332462, 0.00314957, 0.00298488, 0.00294969]),
 array([[0.17702918, 0.23768175, 0.57026935, 0.6618728 ],
        [0.23066045, 0.29187915, 0.51011437, 0.59205174],
        [0.1215842 , 0.18283467, 0.568403  , 0.65917748],
        [0.53046614, 0.58542734, 0.81034887, 0.88709736],
        [0.64277923, 0.69708449, 0.6747762 , 0.75263447],
        [0.39285135, 0.44827259, 0.25520685, 0.33354941],
        [0.45245302, 0.50831991, 0.04279129, 0.11604981],
        [0.42986542, 0.48660529, 0.73582232, 0.81792527],
        [0.7369135 , 0.79619104, 0.812678  , 0.89583528],
        [0.33485392, 0.39549312, 0.38478258, 0.46787152],
        [0.24050979, 0.29796857, 0.17248332, 0.25213283],
        [0.81254733, 0.8663224 , 0.1577777 , 0.22956519],
        [0.81205708, 0.86811525, 0.07908117, 0.15822098],
        [0.08230776, 0.13804683, 0.23831746, 0.31458184],
        [0.65957749, 0.71300834, 0.06289874, 0.13895591],
        [0.49040136, 0.54764146, 0.4610931 , 0.53923297],
        [0.48839793, 0.54509866, 0.596178  , 0.67412436],
        [0.13567482, 0.19079325, 0.31243142, 0.3894755 ],
        [0.19161667, 0.24787259, 0.09706378, 0.17414524],
        [0.7124142 , 0.76670283, 0.06757679, 0.14906914],
        [0.80244732, 0.85601568, 0.68071306, 0.75369447],
        [0.02309109, 0.0884495 , 0.42665428, 0.519225  ],
        [0.13603696, 0.19010249, 0.23887971, 0.31353009],
        [0.597261  , 0.6530956 , 0.54265135, 0.61806071],
        [0.53678578, 0.59486866, 0.67292774, 0.76177043],
        [0.2811234 , 0.3367945 , 0.58373511, 0.65937817],
        [0.11825887, 0.17676857, 0.76905411, 0.85582256],
        [0.65126586, 0.70196229, 0.54277646, 0.61890608],
        [0.49507293, 0.550753  , 0.2592696 , 0.3383674 ],
        [0.0282098 , 0.08554503, 0.2335768 , 0.31032407],
        [0.7996065 , 0.85785884, 0.60827076, 0.68220615],
        [0.80945212, 0.862218  , 0.22467577, 0.29617408],
        [0.55873025, 0.61104375, 0.05374056, 0.13126437],
        [0.01618365, 0.07901882, 0.68379057, 0.77390623],
        [0.40069792, 0.45415127, 0.18156362, 0.2582241 ],
        [0.50353324, 0.55746937, 0.12375417, 0.19795078],
        [0.29656425, 0.35117128, 0.17405511, 0.25058994],
        [0.7926724 , 0.85197407, 0.81323218, 0.89598703],
        [0.08907577, 0.14360776, 0.02915971, 0.10145854],
        [0.60945719, 0.66239184, 0.05847654, 0.1382391 ],
        [0.24551541, 0.29820052, 0.09592979, 0.17139141],
        [0.35188556, 0.4125278 , 0.02542198, 0.11296814],
        [0.38022265, 0.43361306, 0.66592425, 0.73922026],
        [0.28897366, 0.34574723, 0.32006624, 0.39772031],
        [0.47759622, 0.53220719, 0.81168044, 0.88464373],
        [0.34393197, 0.39608505, 0.31754676, 0.38891447],
        [0.59712505, 0.65156943, 0.40505809, 0.47743693],
        [0.38898778, 0.43979731, 0.45893368, 0.52883041],
        [0.74844056, 0.8037324 , 0.672618  , 0.75218052],
        [0.27975845, 0.33573231, 0.65661532, 0.73308241],
        [0.40234217, 0.45498249, 0.10778053, 0.18162157],
        [0.18725891, 0.24317454, 0.24609347, 0.32112017],
        [0.45208394, 0.50638843, 0.18996304, 0.26318079],
        [0.65375733, 0.70822233, 0.13926473, 0.21138135],
        [0.2927793 , 0.34739956, 0.25161624, 0.3238976 ],
        [0.24130832, 0.29360005, 0.25034928, 0.32550895],
        [0.38530934, 0.4396846 , 0.5282445 , 0.59721607],
        [0.18520485, 0.24182689, 0.44511   , 0.52217275],
        [0.65371627, 0.70732075, 0.20815508, 0.28290111],
        [0.58316469, 0.64293456, 0.80467558, 0.88656   ],
        [0.43884829, 0.49030593, 0.46231008, 0.53582567],
        [0.17192546, 0.22958997, 0.77351808, 0.86167079],
        [0.50493932, 0.56085479, 0.04564921, 0.12329351],
        [0.08347016, 0.13575476, 0.31395832, 0.38976124],
        [0.22591783, 0.28218493, 0.79202235, 0.86722481],
        [0.75776088, 0.80971211, 0.22249331, 0.29246515],
        [0.7544058 , 0.8046521 , 0.2899479 , 0.36070281],
        [0.48284045, 0.539186  , 0.67079312, 0.75205094],
        [0.22587565, 0.28112367, 0.65245259, 0.72447211],
        [0.28542885, 0.33889335, 0.44836581, 0.52747005],
        [0.59810239, 0.65272963, 0.47479782, 0.54489845],
        [0.49501646, 0.54838258, 0.39096141, 0.46323746],
        [0.57780826, 0.63089609, 0.8829599 , 0.96326405],
        [0.76103127, 0.81347042, 0.15378259, 0.22430406],
        [0.14220539, 0.19682196, 0.02830735, 0.10121043],
        [0.54932743, 0.6036709 , 0.19534667, 0.26773059],
        [0.27503   , 0.33924562, 0.72915482, 0.81186616],
        [0.18550664, 0.24151816, 0.17346247, 0.24868475],
        [0.43688258, 0.49037051, 0.59657365, 0.66850853],
        [0.02805795, 0.09008751, 0.09775381, 0.1853849 ],
        [0.80406916, 0.85938853, 0.29681048, 0.36674687],
        [0.08484283, 0.13956894, 0.17246215, 0.24202709],
        [0.3754898 , 0.42978627, 0.8034538 , 0.87394697],
        [0.80591464, 0.85994148, 0.36739942, 0.43861976],
        [0.54267222, 0.596914  , 0.60522544, 0.67676896],
        [0.45318413, 0.50561237, 0.11898107, 0.19067429],
        [0.3496367 , 0.4030579 , 0.1100639 , 0.1793559 ],
        [0.43949941, 0.49549511, 0.39374009, 0.46470693],
        [0.08607334, 0.14016631, 0.10370249, 0.17494537],
        [0.549326  , 0.60238969, 0.26379222, 0.33777681],
        [0.557575  , 0.60936117, 0.12833403, 0.19526887],
        [0.13166885, 0.18791184, 0.44199136, 0.52102423],
        [0.03237411, 0.09093823, 0.02466215, 0.10052877],
        [0.59419036, 0.64939839, 0.61299777, 0.684309  ],
        [0.37070587, 0.42986581, 0.87331104, 0.95881331],
        [0.29856029, 0.35148284, 0.10427383, 0.17658159],
        [0.07660906, 0.1306608 , 0.50642425, 0.57728344],
        [0.5932734 , 0.64446163, 0.68306541, 0.75960022],
        [0.70796853, 0.76105756, 0.14874202, 0.22346142],
        [0.29228932, 0.35361382, 0.02493614, 0.10788199],
        [0.74273455, 0.79886711, 0.74777251, 0.81597048],
        [0.68223256, 0.7387386 , 0.88659865, 0.96522433],
        [0.54782605, 0.60086334, 0.33527616, 0.40597969],
        [0.34893763, 0.40262005, 0.18105316, 0.25923395],
        [0.59901684, 0.65092635, 0.33578712, 0.40523747],
        [0.59863615, 0.65317416, 0.27008793, 0.33911619],
        [0.22477016, 0.28056362, 0.7223208 , 0.79355258],
        [0.8027947 , 0.85533804, 0.48001352, 0.553814  ],
        [0.18989973, 0.24239987, 0.31965077, 0.38777888],
        [0.70672631, 0.75944966, 0.22331069, 0.2926313 ],
        [0.01932942, 0.08680736, 0.56160122, 0.65017742],
        [0.65204918, 0.70711297, 0.28327751, 0.35741383],
        [0.42823523, 0.48158574, 0.87834394, 0.95753747],
        [0.01719101, 0.0735781 , 0.76723504, 0.83932739],
        [0.33458996, 0.38790643, 0.59229177, 0.66208953],
        [0.65196312, 0.7042287 , 0.47763854, 0.54196852],
        [0.76345169, 0.8143459 , 0.07609165, 0.15456322],
        [0.06892663, 0.12458645, 0.769965  , 0.85004813],
        [0.69518763, 0.75065666, 0.67046803, 0.75159985],
        [0.68287844, 0.74005866, 0.81382406, 0.89068645],
        [0.015667  , 0.08248556, 0.83311665, 0.91772133],
        [0.18974328, 0.24369499, 0.38463572, 0.44748905],
        [0.42836982, 0.48063272, 0.81152207, 0.88197106],
        [0.65184629, 0.70745361, 0.40721381, 0.48209527],
        [0.08371934, 0.13361538, 0.44551563, 0.5114302 ],
        [0.54876369, 0.59732491, 0.40152657, 0.46947041],
        [0.13481197, 0.1892357 , 0.38683674, 0.44791189],
        [0.22586445, 0.28136912, 0.86700171, 0.93553567],
        [0.75110233, 0.80607605, 0.36112076, 0.42793369],
        [0.69909632, 0.74949   , 0.4126052 , 0.48081604],
        [0.33348608, 0.3873395 , 0.523283  , 0.59341723],
        [0.3777369 , 0.43054307, 0.73643529, 0.80822176],
        [0.52833474, 0.57976985, 0.88671762, 0.95938486],
        [0.54880595, 0.59743482, 0.46673253, 0.53481525],
        [0.69749147, 0.758666  , 0.53933507, 0.62954855],
        [0.79826438, 0.85077757, 0.7533896 , 0.81802255],
        [0.43195409, 0.48566744, 0.66786867, 0.74064577],
        [0.16953792, 0.22439589, 0.85894483, 0.93787128],
        [0.43879542, 0.49057943, 0.53150821, 0.59773606],
        [0.78239125, 0.85361284, 0.89112318, 0.98211169],
        [0.23580994, 0.28189567, 0.59033465, 0.65576959],
        [0.29788423, 0.36831096, 0.87187719, 0.9631182 ],
        [0.23714921, 0.28161892, 0.59328216, 0.65347576],
        [0.47715712, 0.5283168 , 0.88596046, 0.9610638 ],
        [0.47652772, 0.52867526, 0.8860966 , 0.96287882],
        [0.62854248, 0.68568462, 0.88286942, 0.96556348],
        [0.63192248, 0.68416822, 0.88039374, 0.9653064 ],
        [0.1702538 , 0.22603808, 0.85990536, 0.93686485],
        [0.78399831, 0.85674584, 0.89271069, 0.9804942 ],
        [0.43856618, 0.4910734 , 0.53200609, 0.59814441],
        [0.43280032, 0.4848603 , 0.67030728, 0.7376287 ],
        [0.29962882, 0.37041679, 0.87374479, 0.963635  ],
        [0.73682338, 0.79637545, 0.88698387, 0.97406751],
        [0.5277741 , 0.57981384, 0.88727581, 0.9650107 ],
        [0.79868734, 0.85261518, 0.75394148, 0.81864506],
        [0.37806597, 0.43056881, 0.73861492, 0.80887789],
        [0.54914069, 0.59825569, 0.46804824, 0.53600961],
        [0.33365691, 0.38632077, 0.5242449 , 0.59358787],
        [0.22545677, 0.28426278, 0.86275262, 0.93997389],
        [0.75089931, 0.80702889, 0.36215672, 0.42742229],
        [0.13457468, 0.18931121, 0.38736984, 0.44721919],
        [0.738874  , 0.79940712, 0.88680923, 0.97599083],
        [0.42845678, 0.48054823, 0.81236869, 0.8815766 ],
        [0.69837946, 0.76041406, 0.53638315, 0.62930977],
        [0.651661  , 0.70743144, 0.40865144, 0.48147255],
        [0.69931787, 0.75015503, 0.41159183, 0.480886  ],
        [0.54943621, 0.59762782, 0.4011465 , 0.47174439],
        [0.19003126, 0.24450764, 0.38571078, 0.44782695],
        [0.69732988, 0.7509315 , 0.67111075, 0.7518037 ],
        [0.08552735, 0.13402404, 0.44464716, 0.51180249],
        [0.76535434, 0.81475621, 0.0757282 , 0.15504639],
        [0.01513819, 0.08442673, 0.83558774, 0.92133003],
        [0.18697256, 0.24532019, 0.31748059, 0.39145544],
        [0.65130961, 0.70505858, 0.47754848, 0.54218555],
        [0.65137613, 0.71005088, 0.28110704, 0.36062482],
        [0.42789611, 0.48207402, 0.8788209 , 0.95903927],
        [0.70789486, 0.75893021, 0.22339903, 0.29256794],
        [0.01867523, 0.07771798, 0.76598388, 0.84721196],
        [0.33520457, 0.38710833, 0.5922879 , 0.66350877],
        [0.22368158, 0.28145835, 0.72194445, 0.80053234],
        [0.35159379, 0.40231383, 0.18118838, 0.25939247],
        [0.74002945, 0.8004846 , 0.74597669, 0.81957352],
        [0.60000181, 0.65315342, 0.27213031, 0.33839664],
        [0.59950566, 0.65090674, 0.33727586, 0.40510806],
        [0.08178134, 0.14324561, 0.17033033, 0.24804161],
        [0.80375356, 0.86343229, 0.36514068, 0.44219703],
        [0.54774386, 0.60084432, 0.33613574, 0.40667584],
        [0.70944577, 0.76071596, 0.14943412, 0.22279774],
        [0.75468016, 0.80721349, 0.2880545 , 0.36499441],
        [0.02055232, 0.08830914, 0.56052154, 0.65259254],
        [0.06994931, 0.12723981, 0.7687664 , 0.85190976],
        [0.59463286, 0.64879245, 0.61307216, 0.68413782],
        [0.59305489, 0.64467877, 0.68144149, 0.75915223],
        [0.68133   , 0.73941141, 0.81399703, 0.89372581],
        [0.29984882, 0.35130444, 0.10580201, 0.176058  ],
        [0.80093574, 0.85945135, 0.476616  , 0.558154  ],
        [0.55127794, 0.602261  , 0.26429394, 0.33615062],
        [0.07710566, 0.13168813, 0.50730473, 0.57792783],
        [0.18437438, 0.24120967, 0.17436548, 0.24889189],
        [0.08884959, 0.13958767, 0.10382158, 0.17571484]]),
 '26103_TMA21_Original_1120_796.png',
 '/home/jupyter/seattle-quantiphi/TMA/cores/26103_TMA21.svs',
 'tma')
