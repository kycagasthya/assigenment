# Data Science Imports
import pandas as pd
import numpy as np
import tensorflow as tf
import random
import shutil
import psutil
import re


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
from apache_beam import pvalue

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
import sys
import argparse

# Custom file imports #, predict_image_object_detection_sample
from core_utils.utils import load_file_gcs, get_bb_lbl_map_2, save_cores_to_disk, plot_image, predict_image_object_detection_sample, get_bbox_from_svs, predict_cloud_model, predict_cloud_model_2, preprocess_cd228, preprocess_slc1a5, postprocess_slc1a5, predict_cloud_model_patho, load_biomax_csv,Insert_Error_BQ, tma_core_correction, plot_image_quad
spec_chars = [".", "^", "#",'!','@','$','%','*']


def extract_from_gcs(gcs_path):
    """Receives a GCS uri, downloads it and returns local path
    
    Args:
        path (str): GCS uri of the slide and biomax excel
    
    Returns:
        tuple(tuple(gcs path image, local path image), tuple(gcs path biomax excel, local path biomax excel))
    """
    
    parent_dir = os.getcwd()
    folder_path = parent_dir+"/cores"
    destination_path = folder_path+"/"
    program = gcs_path.rsplit(',')[0]
    study = gcs_path.rsplit(',')[1]
    gcs_path_img = gcs_path.rsplit(',')[2]
    gcs_path_excel = gcs_path.rsplit(',')[3]
    logging.getLogger().setLevel(logging.INFO)
    logging.info("gcs image path : %s",\
                 str(gcs_path_img))
    logging.info("gcs excel path : %s",\
                 str(gcs_path_excel))
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    logging.info("Getting file from GCS")
    logging.info("Mem Used : %s",\
                 str(round(psutil.virtual_memory().used/1024**3, 2))+ " GB")
    #path_img = load_file_gcs(gcs_path_img, destination_path)
    #gcs_img = gcs_path_img+','+program+','+study
    #item_img = (gcs_img,path_img)
    #if (gcs_path_excel):
    #    path_excel = load_file_gcs(gcs_path_excel, destination_path)
    #    gcs_excel = gcs_path_excel+','+program+','+study
    #    item_excel = (gcs_excel,path_excel)
    #else:
    #    item_excel = None
    #return (item_img, item_excel)
     
    try :
        path_img = load_file_gcs(gcs_path_img, destination_path)
        gcs_img = gcs_path_img+','+program+','+study
        item_img = (gcs_img,path_img)
        if (gcs_path_excel):
            path_excel = load_file_gcs(gcs_path_excel, destination_path)
            gcs_excel = gcs_path_excel+','+program+','+study
            item_excel = (gcs_excel,path_excel)
        else:
            item_excel = None
        return (item_img, item_excel)
        #return pvalue.TaggedOutput("Process_Tag",(item_img, item_excel))
    except Exception as e:
        logging.exception("File load failed while extracting from GCS " + str(e))
        Insert_Error_BQ((gcs_path_img,config["function_config"]["Insert_Error_BQ"]["dataset_id"],config["function_config"]["Insert_Error_BQ"]["table_id"],job_name, 'Extract from GCS',str(e)))
        pass
        #return pvalue.TaggedOutput("Error_Tag",gcs_path_img)
    
    #return (item_img, item_excel)

def open_svs(items, extra_dwn=1.5625):
    """ Simple function to open an SVS image and downscale
    
    Args:
        path (str): Path to the svs file to be returned
        extra_dwn (int, optional): The additional factor to downscale by
    
    Return:
        PIL Image of the downsampled image, downsample factor, downsampled dimensions
    """
    
    # Open the image and get the lowest tier dimensions and respective
    # downsampling factor
    #gcs_path, path  = items[0]
    try:
        gcs_path, path  = items[0]
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
    
        
        new_dims = slide.level_dimensions[-1]
        dwn_sample = slide.level_downsamples[-1]
    
        name = path.rsplit("/", 1)[-1].rsplit(".", 1)[0]
    
    # Perform extra-downsampling (or not) and return the 
        if not extra_dwn:
            return (slide.read_region((0,0), slide.level_count-1, new_dims), slide.level_downsamples[-1],slide.level_dimensions[-1], name)
        else:
            new_dims = tuple([int(round(dim/extra_dwn)) for dim in new_dims])
            dwn_sample = slide.dimensions[0]/new_dims[0]
            im_original = Image.fromarray(cv2.resize(np.asarray(slide.read_region((0,0), slide.level_count-1,         slide.level_dimensions[-1])), new_dims, cv2.INTER_AREA))
            im_original.save(f"{name}_Original_{new_dims[0]}_{new_dims[1]}.png", "PNG")
        
            im_RGB = im_original.convert('RGB')
            im_RGB.save(f"{name}_RGB_{new_dims[0]}_{new_dims[1]}.jpeg")
            im_RGB.save(f"{name}_RGB_{new_dims[0]}_{new_dims[1]}.png", "PNG")
        
            im_Gray = im_original.convert('L')
            im_Gray.save(f"{name}_Gray_{new_dims[0]}_{new_dims[1]}.jpeg")
            im_Gray.save(f"{name}_Gray_{new_dims[0]}_{new_dims[1]}.png", "PNG")
        
            yield pvalue.TaggedOutput("Process_Tag",(gcs_path, new_dims, name, path))
            #yield (gcs_path, new_dims, name, path)
            
    except Exception as e :
        logging.exception("Unable to open image through OpenSlide  "+ str(e))
        #Insert_Error_BQ(gcs_path.split(',')[0],config["function_config"]["Insert_Error_BQ"]["dataset_id"],config["function_config"]["Insert_Error_BQ"]["table_id"],job_name,source ='Open SVS file')
        #pass
        yield pvalue.TaggedOutput("Error_Tag",(gcs_path.split(',')[0],config["function_config"]["Insert_Error_BQ"]["dataset_id"],config["function_config"]["Insert_Error_BQ"]["table_id"],job_name,'Open SVS',str(e)))
   # yield (gcs_path, new_dims, name, path)

def store_on_gcs(items, output_path):
    """
    Store the image in GCS.
    
    Args:
        items: Tuple of slide path and a batch of tiles.
                tuple(slide name, {"tile_name": str, "tile": PIL.Image})
        output_path (str): Output GCS path for storing the image

    Returns:
       tuple (gcs_path, new_dims, name , path)
    """
    gcs_path, new_dims, name , path = items  
    file_name = f"{name}_Original_{new_dims[0]}_{new_dims[1]}.png"
    im_original = Image.open(file_name)
    store_path = os.path.join(output_path, file_name)

    with beam.io.gcp.gcsio.GcsIO().open(store_path, 'wb') as f:
        logging.getLogger().setLevel(logging.INFO)
        logging.info("new image is saved as : %s",\
                 str(store_path))
        im_original.save(f, "PNG", quality=100)
    
    # gray scale image to be saved code added on 07-03-2022
    
    file_name_gray = f"{name}_Gray_{new_dims[0]}_{new_dims[1]}.png"
    store_path_gray = os.path.join(output_path, file_name_gray)
    im_gray = Image.open(file_name_gray)

    with beam.io.gcp.gcsio.GcsIO().open(store_path_gray, 'wb') as f:
        logging.getLogger().setLevel(logging.INFO)
        logging.info("new image is saved as : %s", str(store_path_gray))
        im_gray.save(f, "PNG", quality=100)

    yield (gcs_path, new_dims, name , path)

def store_viz_on_gcs(items, output_path):
    """
    Store the image in GCS.
    
    Args:
        items: tuple(core_directory, filename, gcs_path, destination_path_cd228, destination_path_slc1a5 , image_class)
        output_path (str): Output GCS path for storing the image

    Returns:
        tuple(core_directory ,filename, gcs_path, image_class)
    """
    core_directory, filename, gcs_path, destination_path_cd228, destination_path_slc1a5, image_class, mi, md, ci, cd, s, i, f = items
    
    logging.getLogger().setLevel(logging.INFO)
    logging.info("destination_path_cd228s : %s",\
                 str(destination_path_cd228))
    
    file_name_cd228 = destination_path_cd228.rsplit("/", 1)[-1][6:]
    file_name_slc1a5 = destination_path_slc1a5.rsplit("/", 1)[-1][7:]
    
    txt_name_cd228 = destination_path_cd228.rsplit("/", 1)[-1][6:].replace(".png", ".txt")
    txt_name_slc1a5 = destination_path_slc1a5.rsplit("/", 1)[-1][7:].replace(".png", ".txt")
    
    im_cd228 = Image.open(destination_path_cd228)
    im_slc1a5 = Image.open(destination_path_slc1a5)
    
    store_path_cd288 = os.path.join(output_path, "cd228",core_directory , file_name_cd228)
    store_path_slc1a5 = os.path.join(output_path, "slc1a5",core_directory, file_name_slc1a5)
    
    scalar_path_cd288 = os.path.join(output_path, "cd228",core_directory , txt_name_cd228)
    scalar_path_slc1a5 = os.path.join(output_path, "slc1a5",core_directory, txt_name_slc1a5)
    
    scalar_cd_str = f"{mi},{md},{ci},{cd}"
    scalar_slc_str = f"{s},{i},{f}"
    
    with beam.io.gcp.gcsio.GcsIO().open(store_path_cd288, 'wb') as f:
        logging.getLogger().setLevel(logging.INFO)
        logging.info("new image is saved as : %s",\
                 str(store_path_cd288))
        im_cd228.save(f, "PNG", quality=100)
    
    with beam.io.gcp.gcsio.GcsIO().open(store_path_slc1a5, 'wb') as f:
        logging.getLogger().setLevel(logging.INFO)
        logging.info("new image is saved as : %s",\
                 str(store_path_slc1a5))
        im_slc1a5.save(f, "PNG", quality=100)
    
    with beam.io.gcp.gcsio.GcsIO().open(scalar_path_cd288, 'wb', mime_type='text/plain') as text_file:
        text_file.write(scalar_cd_str.encode('utf-8'))
        
    with beam.io.gcp.gcsio.GcsIO().open(scalar_path_slc1a5, 'wb', mime_type='text/plain') as text_file:
        text_file.write(scalar_slc_str.encode('utf-8'))
    
    os.remove(destination_path_cd228)
    os.remove(destination_path_slc1a5)
    
    yield (core_directory ,filename, gcs_path, image_class)

#gunjan - code start 
#create label map
def get_bbox_cp (items):
    """ Function to get bounding boxes    
    Args:
        items: tuple(gcs_path, np.array(predictions[0]["confidences"]), np.array(predictions[0]["bboxes"]), filename, local_svs_path,image_class)        
    
    Return:      
        items:tuple (bb_lbl_map, path_to_resized, path, gcs_path,image_class)
    """
    gcs_path, confidences, bboxes , path_to_resized, path, image_class = items
    logging.getLogger().setLevel(logging.INFO)
    logging.info("path to resized : %s",\
                 str(path_to_resized))
    logging.info("local path for original image : %s",str(path))
    bb_lbl_map = get_bb_lbl_map_2(path_to_resized, confidences, bboxes, C_THRESH = config["function_config"]["visualization"]["C_THRESH"], dy_frac = config["function_config"]["visualization"]["dy_frac"], tl_find_mult = config["function_config"]["visualization"]["tl_find_mult"],do_nms = config["function_config"]["visualization"]["do_nms"])
    
    bb_lbl_map = tma_core_correction(path_to_resized, bb_lbl_map)
    
    yield (bb_lbl_map, path_to_resized, path, gcs_path,image_class)

#plot visualisation    
def _plot_merged (items , output_path):
    """ Fucntion to plot images    
    Args:
        items: tuple (bb_lbl_map, path_to_resized, path, gcs_path,image_class)     
    
    Return:      
        None
        """
    bb_lbl_map = items[0]
    name = items[1]
    
    if 'quad' in name.lower():
        plt = plot_image_quad(bb_lbl_map, path_to_resized = name, opacity = config["function_config"]["plot_figure"]["opacity"], cmap = config["function_config"]["plot_figure"]["cmap"],plot_row_boundaries = config["function_config"]["plot_figure"]["plot_row_boundaries"],plot_box_midline = config["function_config"]["plot_figure"]["plot_box_midline"],
upper_cp = config["function_config"]["plot_figure"]["upper_cp"])
    else:
        plt = plot_image(bb_lbl_map, path_to_resized = name, opacity = config["function_config"]["plot_figure"]["opacity"], cmap = config["function_config"]["plot_figure"]["cmap"],plot_row_boundaries = config["function_config"]["plot_figure"]["plot_row_boundaries"],plot_box_midline = config["function_config"]["plot_figure"]["plot_box_midline"],
upper_cp = config["function_config"]["plot_figure"]["upper_cp"])
    

    store_path = os.path.join(output_path,"viz_output", name )
    with beam.io.gcp.gcsio.GcsIO().open(store_path, "wb") as f:
        logging.getLogger().setLevel(logging.INFO)
        logging.info("new image is saved as : %s",\
                 str(store_path))
        plt.savefig(fname = f) 
        
def save_to_gcs(img ,row_idx , row_ltr):   
    """ Fucntion to image into RGB and Gray scale  
    Args:
    img: local image path
        row_idx: row index
        row_lt : column index
    Return:      
        None 
        """
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
        
        
def _save_cores_gcs(items):  
    """ Fucntion to save image cores in GCS bucker    
    Args:
        items : tuple (bb_lbl_map, path_to_resized, path, gcs_path,image_class)    
    Return:      
        val_list : list of core paths 
    """
    bb_lbl_map, filename, local_svs_path, gcs_path, image_class = items
    tma_subdir, file_name = local_svs_path.rsplit(".", 1)[0].rsplit("/", 2)[1:]
    output_dir = os.path.join(output_path, tma_subdir, file_name)
    save_as_rgb = config["function_config"]["visualization"]["save_cores_rgb"]
    cores_list = []
    for row_ltr, bbox_list in tqdm(bb_lbl_map.items(), total=len(bb_lbl_map)):
        for row_idx, bbox in tqdm(enumerate(bbox_list,1), total=len(bbox_list)):
            individual_core_fname = os.path.join(output_dir, f"{file_name}__{row_ltr}{row_idx:02}.jpg")
            logging.info("new image is saved as : %s",\
                 str(local_svs_path))
            core_img = get_bbox_from_svs(local_svs_path, bbox)
            if save_as_rgb:                    
                    img = core_img.convert("RGB")
                    individual_core_fname = individual_core_fname.replace(".jpg", "_rgb.png")
                    
            else:
                    img = core_img.convert("L")
                    individual_core_fname = individual_core_fname.replace(".jpg", "_gray.png")
             
            with beam.io.gcp.gcsio.GcsIO().open(individual_core_fname, "wb") as f:
                    img.save(f,"PNG", quality=100)
                    cores_list.append({"name": f"{row_ltr}{row_idx:02}", "path": "https://storage.cloud.google.com/" + individual_core_fname[5:], "pathology_model_1": None , "pathology_model_2": None})
                        
    os.remove(local_svs_path)
    val_list = [(list(dict_.values()), filename, gcs_path,image_class) for dict_ in cores_list]
    return val_list
    

    
    
def write_to_bigquery(items, dataset_id, table_id, output_path, save_cores,job_name):
    """Function to json into bigquery
    
    Args:
        items (tuple): (core_directory ,filename, gcs_path, image_class)
        dataset_id(str): BQ dataset 
        table_id(str): BQ table name
        output_path(str): Output path for the pipeline
        save_cores(str): save cores flag {values Y/N}

    Returns:
        N/A
    """
    cores_list = []
    if save_cores:
            core_directory,filename, gcs_path, image_class= items
            store_path_viz = "https://storage.cloud.google.com/" + os.path.join(output_path,"viz_output", filename)[5:] 
            bucket_name = output_path.split('/')[2]       #extract bucket name
            client = storage.Client()
            if (image_class == "tma"): ##get TMA core paths
                source_blob_path = os.path.join (output_path.split('/',3)[3] ,"cores", core_directory)
                cd_source_blob_path = os.path.join (output_path.split('/',3)[3] ,"cd228", core_directory)
                slc_source_blob_path = os.path.join (output_path.split('/',3)[3] ,"slc1a5", core_directory)
            
                for blob in client.list_blobs(bucket_name, prefix = source_blob_path):                   
                    name = str(blob).rsplit(",", 1)[0].rsplit("/", 2)[-1].rsplit("_",2)[-2]
                    path = "https://storage.cloud.google.com/" + bucket_name+"/"+source_blob_path +"/"+ str(blob).rsplit(",", 1)[0].rsplit("/", 2)[-1]   
                    scalar_cd_path = os.path.join("gs://", bucket_name, cd_source_blob_path, str(blob).rsplit(",", 1)[0].rsplit("/", 1)[-1].replace(".png", ".txt"))
                
                    scalar_slc_path = os.path.join("gs://", bucket_name, slc_source_blob_path, str(blob).rsplit(",", 1)[0].rsplit("/", 1)[-1].replace(".png", ".txt"))
                    try:
                        with beam.io.gcp.gcsio.GcsIO().open(scalar_cd_path, 'rb', mime_type='text/plain') as text_file:
                            scalar_cd = text_file.read().decode('utf-8').split(",")
                        pathology_model_1 = path.replace("cores","cd228")
                    except Exception as e:
                        logging.exception("Save cores to BigQuery  " + str(e))
                        Insert_Error_BQ((scalar_cd_path,config["function_config"]["Insert_Error_BQ"]["dataset_id"],config["function_config"]["Insert_Error_BQ"]["table_id"],job_name,"Save cores to BigQuery  ", str(e)))
                        
                    try:
                        with beam.io.gcp.gcsio.GcsIO().open(scalar_slc_path, 'rb', mime_type='text/plain') as text_file:
                            scalar_slc = text_file.read().decode('utf-8').split(",")                     
                        pathology_model_2 = path.replace("cores","slc1a5")
                        cores_list.append({"name": name, "path": path ,"CD228_visualization_path": pathology_model_1, "CD228_mi_value": float(scalar_cd[0]), "CD228_md_value": float(scalar_cd[1]), "CD228_ci_value": float(scalar_cd[2]), "CD228_cd_value": float(scalar_cd[3]),  "SLC1A5_visualization_path": pathology_model_2, "SLC1A5_s_value": float(scalar_slc[0]), "SLC1A5_i_value": float(scalar_slc[1]), "SLC1A5_f_value": float(scalar_slc[2])}) 
                    except Exception as e:
                        logging.exception("Save cores to BigQuery  " + str(e))
                        Insert_Error_BQ((scalar_slc_path,config["function_config"]["Insert_Error_BQ"]["dataset_id"],config["function_config"]["Insert_Error_BQ"]["table_id"],job_name,"Save cores to BigQuery  ", str(e)))


                    
            
            else: ##get non TMA core paths
                source_blob_path = os.path.join (output_path.split('/',3)[3] ,"cd228", core_directory)
                cd_source_blob_path = os.path.join (output_path.split('/',3)[3] ,"cd228", core_directory)
                slc_source_blob_path = os.path.join (output_path.split('/',3)[3] ,"slc1a5", core_directory)
                store_path_viz = None
                for blob in client.list_blobs(bucket_name, prefix = source_blob_path):
                    if str(blob).rsplit(",", 1)[0].endswith(".png"):
                        name = None 
                        path = None 
                        try:
                            scalar_cd_path = os.path.join("gs://", bucket_name, cd_source_blob_path, str(blob).rsplit(",", 1)[0].rsplit("/", 1)[-1].replace(".png", ".txt"))
                            with beam.io.gcp.gcsio.GcsIO().open(scalar_cd_path, 'rb', mime_type='text/plain') as text_file:
                                scalar_cd = text_file.read().decode('utf-8').split(",")
                            pathology_model_1 = "https://storage.cloud.google.com/" + bucket_name+"/"+source_blob_path +"/"+ str(blob).rsplit(",", 1)[0].rsplit("/", 2)[-1]
                            
                            
                        except Exception as e:
                            logging.exception("Save cores to BigQuery  " + str(e))
                            Insert_Error_BQ((scalar_cd_path,config["function_config"]["Insert_Error_BQ"]["dataset_id"],config["function_config"]["Insert_Error_BQ"]["table_id"],job_name,"Save cores to BigQuery  ", str(e)))
                            
                        try:
                            scalar_slc_path = os.path.join("gs://", bucket_name, slc_source_blob_path, str(blob).rsplit(",", 1)[0].rsplit("/", 1)[-1].replace(".png", ".txt")) 
                            with beam.io.gcp.gcsio.GcsIO().open(scalar_slc_path, 'rb', mime_type='text/plain') as text_file:
                                scalar_slc = text_file.read().decode('utf-8').split(",")
                            path_cd228 = "https://storage.cloud.google.com/" + bucket_name+"/"+source_blob_path +"/"+ str(blob).rsplit(",", 1)[0].rsplit("/", 2)[-1]
                            pathology_model_2 = path_cd228.replace("cd228","slc1a5")
                            cores_list.append({"name": name, "path": path ,"CD228_visualization_path": pathology_model_1, "CD228_mi_value": float(scalar_cd[0]), "CD228_md_value": float(scalar_cd[1]), "CD228_ci_value": float(scalar_cd[2]), "CD228_cd_value": float(scalar_cd[3]),  "SLC1A5_visualization_path": pathology_model_2, "SLC1A5_s_value": float(scalar_slc[0]), "SLC1A5_i_value": float(scalar_slc[1]), "SLC1A5_f_value": float(scalar_slc[2])})
                            
                        except Exception as e:
                            logging.exception("Save cores to BigQuery  "+ str(e))
                            Insert_Error_BQ((scalar_slc_path,config["function_config"]["Insert_Error_BQ"]["dataset_id"],config["function_config"]["Insert_Error_BQ"]["table_id"],job_name,"Save cores to BigQuery  ", str(e)))

    else:
        #_, filename, _, gcs_path = items
            bb_lbl_map, filename, path, gcs_path, image_class = items
            if (image_class == "tma"):
                store_path_viz = "https://storage.cloud.google.com/" + os.path.join(output_path,"viz_output", filename)[5:] 
            else:
                store_path_viz = None
            cores_list = [{"name": None, "path": None, "CD228_visualization_path": None, "CD228_mi_value": None, "CD228_md_value": None, "CD228_ci_value": None, "CD228_cd_value": None,  "SLC1A5_visualization_path": None, "SLC1A5_s_value": None, "SLC1A5_i_value": None, "SLC1A5_f_value": None}]
    
    
     
    input_path = "https://storage.cloud.google.com/" + gcs_path.rsplit(',',3)[0][5:]
    program = gcs_path.rsplit(',',3)[1]
    study = gcs_path.rsplit(',',3)[2]
    store_path_downsampled = "https://storage.cloud.google.com/" + os.path.join(output_path, filename)[5:]
    client = bigquery.Client()
    dataset_ref = client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)
    table = client.get_table(table_ref)  # API call    
    now = time.strftime("%Y%m%d-%H%M%S")
    rows_to_insert = [{"original_svs": input_path,
                           "downscaled_image": store_path_downsampled,
                           "downscaled_dearray_visualisation":store_path_viz,
                           "program":program,
                           "study":study,
                           "cores": cores_list,
                           "job_name": job_name
                          }]
    errors = client.insert_rows_json(table, rows_to_insert)  # API request
    return


def extract_from_gcs2(gcs_path):
    """Receives a GCS uri, downloads it and returns local path
    
    Args:
        path (str): GCS uri of the slide
    
    Returns:
        tuple(slide gcs path, local path of slide)
    """
    
    parent_dir = os.getcwd()
    folder_path = parent_dir+"/cores"
    destination_path = folder_path+"/"
    os.makedirs(folder_path, exist_ok=True)
    logging.info("Getting file from GCS")
    path = load_file_gcs(gcs_path, destination_path)
    return (gcs_path, path)

def perform_inference_flatmap(items):
    """Receives a tuple, performs pathology model prediction
    
    Args:
        items (tuple): (lists of cores for slide images)
    
    Returns:
        tuple(core_directory, filename, gcs_path, destination_path_cd228, destination_path_slc1a5,image_class)
        """
    logging.info("***********Performing Inference")
    try:
        core, filename, gcs_path, image_class = items
        logging.info("Core list values are : {}".format(' '.join(map(str, core))))   
        core = {'name': core[0], 'path':  core[1], 'pathology_model_1':  core[2], 'pathology_model_2':  core[3]}
        tma_core_path = core["path"].replace("https://storage.cloud.google.com/", "gs://")
        _, path = extract_from_gcs2(tma_core_path)
    
        img = np.asarray(Image.open(path))
    
        cd228_core_img = preprocess_cd228(img)
        slc1a5_core_img = preprocess_slc1a5(img)
                 
        parent_dir = os.getcwd()
        subdir_name = filename.replace(".png", "")
        folder_path1 = parent_dir + f"tmp/PreprocessedImages/{subdir_name}"
        os.makedirs(folder_path1, exist_ok=True)

        cd_fpath = folder_path1 + "/cd228_" +  core['name']  + ".png"
        cd_img = tf.cast(65535.0*(cd228_core_img + 1.732052)/3.732052, tf.uint16).numpy()
        cv2.imwrite(cd_fpath, cd_img)

        slc_fpath = folder_path1 + "/slc1a5_" +  core['name']  + ".png"
        slc_img = tf.cast(65535.0*slc1a5_core_img, tf.uint16).numpy()
        cv2.imwrite(slc_fpath, slc_img)

        PROJECT_NAME = "ihc-qc-sandbox"
        predictions_cd = predict_cloud_model_patho(PROJECT_NAME, "1796285340437184512", cd_fpath)
        predictions_slc = predict_cloud_model_patho(PROJECT_NAME, "3949005962320281600", slc_fpath)
        s = round(predictions_slc[0]['s'][0], 3)
        i = round(predictions_slc[0]['i']*3.0, 3)
        f = round(predictions_slc[0]['f']*4.0, 3)
        
        mi = float(predictions_cd[0]["mi"])*3.0
        md = float(predictions_cd[0]["md"])*4.0
        ci = float(predictions_cd[0]["ci"])*3.0
        cd = float(predictions_cd[0]["cd"])*4.0
    
    
        os.remove(path)
        os.remove(cd_fpath)
        os.remove(slc_fpath)

        folder_path = parent_dir + f"tmp/InferenceVisualization/{subdir_name}"
        destination_path_cd228 = folder_path+"/cd228_"+tma_core_path.rsplit("/", 1)[-1]
        destination_path_slc1a5 = folder_path+"/slc1a5_"+tma_core_path.rsplit("/", 1)[-1]
        os.makedirs(folder_path, exist_ok=True)

        plt.imsave(destination_path_cd228, predictions_cd[0]["activation_2"], cmap="Spectral")
        plt.imsave(destination_path_slc1a5, predictions_slc[0]["attention_layer"], cmap="Spectral")

        core_directory = core["path"].rsplit("/")[-2]

        yield (core_directory, filename, gcs_path, destination_path_cd228, destination_path_slc1a5,image_class, mi, md, ci, cd, s, i, f)
        
    except Exception as e:
        logging.exception("Model response is blank for pathology models : TMA "+str(e))
        Insert_Error_BQ((tma_core_path,config["function_config"]["Insert_Error_BQ"]["dataset_id"],config["function_config"]["Insert_Error_BQ"]["table_id"],job_name, 'Performing Inference',str(e)))
        pass
    
def perform_inference_core(items):
    """Receives a tuple, performs pathology model prediction for core images
    
    Args:
        items (tuple): (lists of cores for slide images)
    
    Returns:
        tuple(core_directory, filename, gcs_path, destination_path_cd228, destination_path_slc1a5,image_class)
        """
    logging.info("***********Performing Inference")
    try:
        gcs_path, image_class, filename, _ = items
        
        filename = filename.replace("Gray","Original")
        
        img = Image.open(filename)
        img = img.convert('RGB')
        img = np.asarray(img)
    
        cd228_core_img = preprocess_cd228(img)
        slc1a5_core_img = preprocess_slc1a5(img)
        
        parent_dir = os.getcwd()
        folder_path1 = parent_dir + "/PreprocessedImages"
        if not os.path.exists(folder_path1):
            os.mkdir(folder_path1)
    
    
        cd_fpath = folder_path1 + "/cd228_" +  filename  + ".png"
        cd_img = tf.cast(65535.0*(cd228_core_img + 1.732052)/3.732055, tf.uint16).numpy()
        cv2.imwrite(cd_fpath, cd_img)
        
        slc_fpath = folder_path1 + "/slc1a5_" +  filename  + ".png"
        slc_img = tf.cast(65535.0*slc1a5_core_img, tf.uint16).numpy()
        cv2.imwrite(slc_fpath, slc_img)
        
        PROJECT_NAME = "ihc-qc-sandbox"
    
        
        predictions_cd = predict_cloud_model_patho(PROJECT_NAME, "1796285340437184512", cd_fpath)
        predictions_slc = predict_cloud_model_patho(PROJECT_NAME, "3949005962320281600", slc_fpath)
        s = round(predictions_slc[0]['s'][0], 3)
        i = round(predictions_slc[0]['i']*3.0, 3)
        f = round(predictions_slc[0]['f']*4.0, 3)
        mi = float(predictions_cd[0]["mi"])*3.0
        md = float(predictions_cd[0]["md"])*4.0
        ci = float(predictions_cd[0]["ci"])*3.0
        cd = float(predictions_cd[0]["cd"])*4.0  
    
        folder_path = parent_dir+"/InferenceVisualization"
        destination_path_cd228 = folder_path+"/cd228_"+filename
        destination_path_slc1a5 = folder_path+"/slc1a5_"+filename
    
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
        
        plt.imsave(destination_path_cd228, predictions_cd[0]["activation_2"], cmap="Spectral")
        plt.imsave(destination_path_slc1a5, predictions_slc[0]["attention_layer"], cmap="Spectral")
    
        os.remove(filename)
        os.remove(cd_fpath)
        os.remove(slc_fpath)
    
        core_directory = filename.rsplit("_Original", 1)[0]
           
        yield (core_directory, filename, gcs_path, destination_path_cd228, destination_path_slc1a5,image_class, mi, md, ci, cd, s, i, f)
        
    except Exception as e:
        logging.exception("Model response is blank for pathology models : Core  "+str(e))
        Insert_Error_BQ((filename,config["function_config"]["Insert_Error_BQ"]["dataset_id"],config["function_config"]["Insert_Error_BQ"]["table_id"],job_name,'Performing Inferencing non - TMA',str(e)))
        pass
        
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

def run(config, input_path, output_arg):
    """
    Function for building and deploying the pipeline based on the config provided.
    
    Args:
        config (dict): Configuration for the pipeline and its functions
    
    Returns:
        N/A
    """
    global output_path
    output_path = output_arg
    global job_name
    project_id = config["pipeline_config"]["project_id"]
    
    extra_dwn = config["function_config"]["open_svs"]["extra_dwn"]
    endpoint_id = config["function_config"]["predict_image_object_detection_sample"]["endpoint_id"]
    location = config["function_config"]["predict_image_object_detection_sample"]["location"]
    api_endpoint = config["function_config"]["predict_image_object_detection_sample"]["api_endpoint"]
    save_cores_ = config["function_config"]["visualization"]["save_cores"]
    dataset_id = config["function_config"]["write_to_bigquery"]["dataset_id"]
    table_id = config["function_config"]["write_to_bigquery"]["table_id"]
    
    click.echo("Running job: {}".format(config["pipeline_config"]["job_name"]))
    
    now = time.strftime("%Y%m%d-%H%M%S")
    output_path = os.path.join(output_path, config["pipeline_config"]["job_name"] + f"-{now}")

    if config["pipeline_config"]["run_local"]:
        # Execute pipeline in your local machine.
        runner_options = {
            "runner": "DirectRunner",
        }
    else:
        runner_options = {
            "runner": "DataflowRunner",
            "temp_location": os.path.join(output_path, "temp_location"),
            "staging_location": os.path.join(output_path, "staging_location"),
            "max_num_workers": config["pipeline_config"]["max_num_workers"],
            "machine_type": config["pipeline_config"]["machine_type"],
            "disk_size_gb": config["pipeline_config"]["disk_size_gb"],
            "num_workers": config["pipeline_config"]["num_workers"],
            "network": config["environment"]["network"],
            "subnetwork": config["environment"]["subnetwork"]
        }
    job_name=config["pipeline_config"]["job_name"] + f"-{now}"
    options = PipelineOptions(
        project=config["pipeline_config"]["project_id"],
        job_name=job_name,
        region=config["pipeline_config"]["region"],
        **runner_options
    )
    options.view_as(SetupOptions).save_main_session = True
    options.view_as(SetupOptions).setup_file = os.path.join(
        pathlib.Path(__file__).parent.absolute(), "setup.py")
    
    logging.info("Building Pipeline........")
    logging.info("Job name ...."+str(job_name))
    #input_path_biomax = config["function_config"]["load_biomax_csv"]["input_path_biomax"]
    table_id_biomax = config["function_config"]["load_biomax_csv"]["table_id_biomax"]
    with beam.Pipeline(options=options) as p:
        ## Read slide paths from CSV >> Download Slide from GCS to local runner >> Read & Downscale
        read_img = (p| "Source image path" >> ReadFromText(input_path))
        extract_files = read_img | "Extract from GCS" >> beam.Map(extract_from_gcs)  |"filter none " >>beam.Filter((lambda x : None if(x == None) else x))
        
        #extract_files = read_img | "Extract from GCS" >>\
        #beam.Map(extract_from_gcs).with_outputs('Process_Tag','Error_tag')
        
        #extract_files = read_img | "Extract from GCS" >>beam.Map(extract_from_gcs)
       
        downscale  =extract_files | "filter svs" >> beam.Filter((lambda x : None if(x[0] == None) else x)) | "Open SVS" >> beam.ParDo(open_svs, extra_dwn=extra_dwn).with_outputs('Error_Tag','Process_Tag')
        
        
        
        #downscale  =extract_files | "Open SVS" >> beam.ParDo(open_svs,extra_dwn=extra_dwn)
       ##handle edge case
        _    = extract_files |"filter biomax csv" >> beam.Filter((lambda x : None if(x[1] == None) else x))| "Load BQ biomax" >> beam.ParDo(load_biomax_csv , dataset_id ,table_id_biomax,config=config,job_name=job_name)      
         
        gcs_store_slide = (downscale.Process_Tag
                          | "Store Slide on GCS" >> beam.ParDo(store_on_gcs, output_path))
        
        ##TMA / non tma classifier
        classifier =  gcs_store_slide | "TMA classifier Pred" >> beam.ParDo(predict_cloud_model ,project=project_id, endpoint_id="9222861863459487744", C_THRESH = config["function_config"]["visualization"]["C_THRESH"],config=config,job_name=job_name,location=location, api_endpoint=api_endpoint ).with_outputs('classfication_error','classfication_svs')
        
        
       ##Pcollection for TMA 
        TMA_pcollection = classifier.classfication_svs | "TMA list" >> beam.Filter((lambda x : x if(x[1] =='tma') else None))                      ### Pcollection for Cores -> input for pathology models        
        Cores_pcollection_1 =  (classifier.classfication_svs
                              | "Cores list" >> beam.Filter((lambda x : x if(x[1] == 'not_tma') else None))
                              | "Performing Inferencing (non-TMA)" >> beam.ParDo(perform_inference_core))
        Cores_pcollection_2 = Cores_pcollection_1 | "Store Visualizations on GCS (non-TMA)" >> beam.ParDo(store_viz_on_gcs, output_path)
       
       ###Start de-array processing -> do visulization and save cores for tma svs
        prediction = (TMA_pcollection
                     | "Prediction" >> beam.ParDo(predict_image_object_detection_sample, project=project_id, endpoint_id=endpoint_id,C_THRESH = config["function_config"]["visualization"]["C_THRESH"],config=config,job_name=job_name, location=location, api_endpoint=api_endpoint).with_outputs('Process_Tag','Error_Tag'))

        get_label_map = prediction.Process_Tag | "create label map" >> beam.ParDo(get_bbox_cp)                              
        visualisation =  get_label_map |"save visualisation" >> beam.Map(_plot_merged,output_path)
        
        if save_cores_:
            save_cores  = (get_label_map | "save cores in gcs" >> beam.FlatMap(_save_cores_gcs)
                                         | "Prevent Fusion" >> beam.Reshuffle())
            inference_1 = (save_cores 
                    | "Performing Inference" >> beam.ParDo(perform_inference_flatmap))
            inference_2 = inference_1 | "Store Visualizations on GCS" >> beam.ParDo(store_viz_on_gcs, output_path)
            
            merged = ((inference_2,Cores_pcollection_2) | 'Merge PCollections' >> beam.Flatten())
            bq_path_cores =   merged | "Filter Duplicate" >> beam.Distinct()|  "Save cores to Bigquery" >> beam.ParDo(write_to_bigquery, dataset_id, table_id, output_path, save_cores_,job_name=job_name)
            
        else:
            save_to_bigquery = get_label_map | "Save paths to Bigquery" >> beam.ParDo(write_to_bigquery, dataset_id, table_id, output_path, save_cores_,job_name=job_name)
            
         ###End dearray pipeline 
        
        merged_2 =   ((downscale.Error_Tag,prediction.Error_Tag,classifier.classfication_error) |"Merge Error" >>beam.Flatten())
        
        _ = merged_2 |"Filter Duplicate 2" >> beam.Distinct()| "insert error in  BQ" >>beam.ParDo(Insert_Error_BQ)
        
        
             

if __name__ == "__main__":
    """Main entry point; defines and runs the pipeline."""
    logging.getLogger().setLevel(logging.INFO)
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--config_file', dest='config_file', required=False, help='Full GCS location for config.json file')
    parser.add_argument('--input_path', dest='input_path', required=False, help='Full GCS location for input CSV')
    parser.add_argument('--output_path', dest='output_path', required=False, help='Destination GCS path for storing results')

    known_args, pipeline_args = parser.parse_known_args(sys.argv)
    
    download_from_gcs("ihc-qc-sandbox", known_args.config_file, "config.json")
    
    with open("./config.json", "r") as f:
        config = json.load(f)
    print(config)
    run(config, known_args.input_path, known_args.output_path)
