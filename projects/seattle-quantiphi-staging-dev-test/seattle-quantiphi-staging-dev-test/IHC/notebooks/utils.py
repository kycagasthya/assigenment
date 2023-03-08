import matplotlib.pyplot as plt
from PIL import Image
import pandas as pd
import numpy as np
import openslide
import tifffile
import math
import os

def get_paths(path_to_folder):
    """ Simple function to return full paths of all svs and qptiff images in a folder """
    if not os.path.isdir(path_to_folder):
        print(f"Skipping as `{path_to_folder}` folder does not exist")
        return []
    
    return [
        path for path in \
        [os.path.join(path_to_folder, f_name) for f_name in os.listdir(path_to_folder)] \
        if (path[-4:] == ".svs" or path[-6:] == "qptiff")
    ]


def subsample_df(df, n=4, save_to_csv=True, save_dir="/home/jupyter/tiles", high_subset=1):
    df_list = [df.iloc[i::n] for i in range(n)]
    if save_to_csv:
        for i, _df in enumerate(df_list):
            _df.to_csv(f"{save_dir}/automl_subset_{high_subset}_{i+1}.csv", index=False, header=False, encoding="utf-8")
    return df_list


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
    
    
def tile_tiff(slide,  tile_size=1024):
    """ Tile .tiff/.qtiff format image into .PNG image tiles """
    # No images in GCS bucket are currently TIFFs or QTIFFS
    #    - As such we will not implement this function
    #    - That being said, the implementation is very similar to 
    #      the tile_svs() function with a different get_slide_region()
    #      subfunction that will index the tiff file that has been loaded
    #      using the tifffile library.
    pass


def tile_svs(slide, slide_name, output_dir, tile_size=1024, to_file=True, divert_blanks=False, divert_to=None, verbose=1):
    """ Tile .svs format image into .PNG image tiles 
    
    Args:
        slide (OpenSlide Object): Full resolution OpenSlide object that we wish
            to reduce to component tiles
        slide_name (str): Name of the image. Will be included in output tile image
            names to distinguish between source images.
        output_dir (str): Path to the output directory where we should store the
            tiled images
        tile_size (int, optional): The dimension of the square-tile to extract from
            the slide image when tiling. Every tile will be [tile_size x tile_size x 3]
        to_file (bool, optional): Whether to save the images to file or return them as
            a list. Currently only saving to file is supported.
        divert_blanks (bool, optional): Whether to use heuristics to annotate slides where
            it is very obvious that no-tissue is present. These annotated slides will then 
            be diverted into the post-annotation directory
        divert_to (str, optional): The folder to divert the heuristically annotated blanks.
            If not passed, the divert_to will default to within the `output_dir` folder
            in a subfolder called `{output_dir}/post_annotation/no_tissue`
        verbose (int, optional): Level of verbosity
            0 – Do not print progress information
            1 – Print progress update every row
            2 – Print progress update every tile
            
    Returns:
        None; Tile images are saved to file and status is printed as it progresses.
        
    Raises:
        ValueError
            - If to_file=False as it is not yet supported
    """
    
    # Handle argument parsing and folder creation
    if divert_blanks:
        if divert_to==None:
            divert_to = os.path.join(output_dir.rsplit("/", 1)[0], "post_annotation", "no_tissue")
        if not os.path.isdir(divert_to):
            os.makedirs(divert_to, exist_ok=True)
    
    # Make output directory if it does not exist
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    if not to_file:
        raise ValueError("Only `to_file`=True is currently supported. " \
                         "i.e. saving to file as we iterate over the slide.")

    w, h = slide.dimensions
    pad_w, pad_h = math.ceil(w/tile_size)*tile_size, math.ceil(h/tile_size)*tile_size
    print(f"\nOriginal is {pad_w} by {pad_h} pixels")
    print(f"This will result in {int((pad_w/tile_size)*(pad_h/tile_size))} " \
          f"individual image tiles saved to the {output_dir} directory\n")
    
    print("\n--------------------------------------------------------------")
    print("         ... Starting to iterate over the image file ...")
    print("--------------------------------------------------------------\n")
    for x in range(0, pad_w, tile_size):
        if verbose != 0:
            print(f"\n\t\t ROW {int((x/tile_size))+1}\n")
        for y in range(0, pad_h, tile_size):
            if verbose == 2:
                print(f"Working on tile ({x},{y}) to ({x+tile_size},{y+tile_size})")
            tile = get_slide_region(slide, origin=(x,y), 
                                    region_size=(tile_size, tile_size), level_to_pull=0)
            if divert_blanks:
                no_tissue_present = no_tissue_heuristic(np.asarray(tile.convert("RGB"), dtype=np.uint8))
                if no_tissue_present:
                    tile.save(os.path.join(divert_to, f"{slide_name}_{x:05}_{y:05}.png"), quality=100)
                else:
                    tile.save(os.path.join(output_dir, f"{slide_name}_{x:05}_{y:05}.png"), quality=100)
            else:
                tile.save(os.path.join(output_dir, f"{slide_name}_{x:05}_{y:05}.png"), quality=100)
                    
                
def no_tissue_heuristic(np_tile, upper_thresh=200, lower_thresh=1, heuristic_ratio_boundary=0.001):
    """ Function to heuristically determine if no tissue is present for a given tile
    
    Args:
        np_tile (nd.array(uint8)): A numpy array representing the tile
        upper_thresh (int, optional): The upper threshold for considering valid `tissue pixels`
        lower_thresh (int, optional): The lower threshold for considering valid `tissue pixels`
        heuristic_ratio (float, optional): The number of pixels with values between
            `lower_thresh` and `upper_thresh` in the whole image as a ratio of the
            total number of pixels present in the tile. 
                - i.e. 0.001 for a 1024x1024x3 image (3,145,728 pixels), indicates
                  that ~15725 pixels are allowed to have values between `lower_thresh` 
                  and `upper_thresh`... if more pixels have values (more colour, etc.),
                  then the image is heuristically determiend to NOT BE BACKGROUND.
    
    Returns:
        A bool indicating whether or not the tile contains tissue.
            - True is indicative of NO-TISSUE being present
            - False is indicative of SOME-TISSUE being present
    """
    # find frequency of pixels in range 0-255 
    histr, _ = np.histogram(np_tile.mean(axis=-1).astype(np.uint8).ravel(),256,[0,256]) 
    histr_sum = histr[lower_thresh:upper_thresh].sum()
    image_pixel_count = np.product(np_tile.shape)
    heuristic_ratio_calc = histr_sum/image_pixel_count
    
    if heuristic_ratio_calc>heuristic_ratio_boundary:
        return False
    else:
        return True
    
def determine_label(slide_path):
    """ Simple function to determine class label from image path """
    if "Stained/Yes" in slide_path:
        return "strong_positive"
    elif "Stained/Dim" in slide_path:
        return "dim_positive"
    elif "Stained/No" in slide_path:
        return "negative"
    elif "Focus/Out_Focus" in slide_path:
        return "out_of_focus"
    elif "Tissue/No_Tissue" in slide_path:
        return "no_tissue"
            
def tile_from_path(slide_path, output_dir_root, slide_name=None, style="svs", tile_size=1024, divert_blanks=False, divert_to=None, verbose=1):
    """ 
    
    Tile a full-resolution image slide from a given image path
    
    Args:
        slide_path (str): Path to the full resolution image slide to be tiled
        output_dir_root (str): Path to the output directory in which the subfolders
            containing class level directories are found
        slide_name (str, optional): Optional file name.
        style (str, optional): Which format is the full resolution image slide file
        tile_size (int, optional): The side-length to use when generating square tiles
        divert_blanks (bool, optional): Whether to use heuristics to annotate slides where
            it is very obvious that no-tissue is present. These annotated slides will then 
            be diverted into the post-annotation directory
        divert_to (str, optional): The folder to divert the heuristically annotated blanks.
            If not passed, the divert_to will default to within the `output_dir` folder
            in a subfolder called `{output_dir}/post_annotation/no_tissue`
        verbose (int, optional): Level of verbosity
            0 – Do not print progress information
            1 – Print progress update every row
            2 – Print progress update every tile
    
    Returns:
        None; The image will be tiled and saved into the correct location.
    """
    
    slide_obj = openslide.OpenSlide(slide_path)
    if slide_name == None:
        slide_name = slide_path.rsplit("/", 1)[1].split(".", 1)[0]
    else:
        if f".{style}" in slide_name:
            slide_name = slide_name.split(".", 1)[0]

    output_dir = os.path.join(output_dir_root, determine_label(slide_path))
    
    if style=="svs":
        tile_svs(slide_obj, 
                 slide_name, 
                 output_dir, 
                 tile_size=tile_size, 
                 divert_blanks=divert_blanks, 
                 divert_to=divert_to,
                 verbose=verbose)
    else:
        # Not Implemented Yet
        tile_tiff()
    
def create_automl_preannotated_csv(tile_dir, gcs_pre_path="gs://seagen-quantiphi/to-be-annotated"):
    """ Create the AUTOML CSV to be used to update annotations 
    
    Args: 
        tile_dir (str): Path to the directory containing the sub-directories
            named after the respective labels of the images/slides contained there-within
        gcs_pre_path (str): Path to the gcs bucket the images will be stored
    
    Returns: 
        None; 
            A .CSV file will be generated into the `tile_dir` directory containing
            the information required to perform annotation using AutoML
    
    """
    
    tile_map = {"image_paths":[], "labels":[]}
    for label in [name for name in os.listdir(tile_dir) if not name.endswith(".csv")]:
        full_paths = [
            os.path.join(gcs_pre_path, label, f_name) 
            for f_name in os.listdir(os.path.join(tile_dir, label)) 
            if f_name.endswith(".png")
        ]
        tile_map["labels"].extend([label,]*len(full_paths))
        tile_map["image_paths"].extend(full_paths)
    pd.DataFrame(tile_map).to_csv(os.path.join(tile_dir, "automl.csv"), 
                                  index=False, 
                                  header=False, 
                                  encoding="utf-8")
    
def create_overlay(df, output_dir, path_to_slide, slide_label,
                   max_size=1920, 
                   class_cpal=None, 
                   display=False, 
                   verbose=False, 
                   use_builtin_dwnsample=True, 
                   class_list=('out_of_focus', 'dim_positive', 'he', 'negative', 'no_tissue', 'exclusion', 'strong_positive'), 
                   uncertain_class="unsure",
                   core_opacity=0.65,
                   cmap_name="bright", 
                   original_tile_size=1024,
                   figure_dpi=120,
                   is_direct_annotation=False):
    """ Create an Overlay Showing The Tile Level Predictions
    
    Args:
        df (pd.DataFrame): Containing: x_coord (int), y_coord (int), label (str)
        output_dir (str): Path to the directory to save the overlay
        path_to_slide (str): Path to the slide (on local where it can be loaded)
        slide_label (str): The label to apply to the entire slide.
        max_size (int, optional): The maximum side length to constrain the overlay's longest side to
        class_cpal (np.array, optional): Included color palette to use for overlay
        display (bool, optional): Whether to display the generated overlay
        use_builtin_dwnsample (bool, optional): Whether to load using OpenSlide's
            builtin downsample functionality (STRONGLY RECOMMENDED)
        class_list (tuple, optional): List of classes to be used that will tie the 
            label in the df to a specific colour in the legend/color-palette
        uncertain_class (str, optional): Class name for the uncertain predictions
            to be displayed as white.
        core_opacity (float, optional): Opacity of the slide image (alpha)
            i.e 1-core_opacity will give you the opacity of the label-color-map
        cmap_name (str, optional): Name of the seaborn color palette to use.
            LINK --> https://seaborn.pydata.org/tutorial/color_palettes.html
        original_tile_size (int, optional): Original size of the tiles that were 
            predicted upon by the model
        figure_dpi (int, optional): The resolution for which to save the 
            matplotlib figure with
        is_direct_annotation (bool, optional): Whether this is ground truth data
            or predicted labels
            
    Returns:
        None; An image will be written to disk containing the overlay
              and the image can also be displayed (optional)
        
    
    """
    
    
    
    # ##############################################################################    
    #                      Initialize Display Related Things
    # ##############################################################################
    
    
    # Color Palette As A List
    cpal_map = sns.color_palette(cmap_name, len(class_list))
    
    # Get Color Palette Values in the Right Format [0-255 and uint8]
    if class_cpal is None:
        class_cpal = np.uint8(np.array(cpal_map)*255)
    
    # Map each class to a specific color value
    class_cmap = {c:class_cpal[i] for i,c in enumerate(class_list)}
    
    # Create legend elements to be used later when plotting
    legend_elements = [
        Patch(facecolor=np.append(c,1-core_opacity), label=class_list[i]) \
        for i,c in enumerate(cpal_map)
    ]
    if is_direct_annotation:
        legend_elements.append(Patch(facecolor=(0,0,0,1-core_opacity), label="background"))
    else:
        legend_elements.append(Patch(facecolor=(0,0,0,1-core_opacity), label="uncertain"))
    
    # ##############################################################################
    
    
    
    # ##############################################################################        
    #                     Creating the Downsampled Slide Image                     #
    # ##############################################################################
    
    
    # ######################## #
    # ###   Step 1. Load   ### #
    # ######################## #

    # Get the full slide as an OpenSlide object
    full_slide = openslide.OpenSlide(path_to_slide)

    
    # ################################################## #
    # ### Step 2. Get Values Related to Downsampling ### #
    # ################################################## #
    
    # If we want to use built in downsampling we set these parameters accordingly
    if use_builtin_dwnsample:
        level_idx = full_slide.level_count-1               # Downsample Level Index
        start_dwnsample = full_slide.level_downsamples[-1] # Amount to Downsample
        slide_dim = full_slide.level_dimensions[-1]        # Get Dimensions of Downsampled Slide
    else:
        level_idx = 0                     # Pick the first index
        start_dwnsample=1                 # Amount to downsample is 1 (None)
        slide_dim = full_slide.dimensions # Downsampled Slide Dims Are Original Dims
    
    # Print text on characteristics of slide if requested (verbose=True)
    if verbose:
        print(f"ORIGINAL SLIDE DIMENSIONS: {full_slide.dimensions}")
        if use_builtin_dwnsample:
            print(f"DOWNSAMPLED SLIDE DIMENSIONS: {slide_dim}")
    
    
    # ##################################### #
    # ### Step 3. Get Downsample Factor ### #
    # ##################################### #
    
    downscale_factor = max(slide_dim)/max_size
    total_downscale_factor = downscale_factor*start_dwnsample
    
    # Print text on characteristics of slide if requested (verbose=True)
    if verbose:
        print("DOWNSCALE FACTOR: ", total_downscale_factor)
    
    # ################################# #
    # ### Step 4. Get New Tile Size ### #
    # ################################# #
    
    new_tile_size = int(np.ceil(original_tile_size/(total_downscale_factor)))
    
    # Print text on characteristics of slide if requested (verbose=True)
    if verbose:
        print(f"ORIGINAL TILE DIMENSIONS: {original_tile_size}x{original_tile_size}")
        print(f"NEW TILE DIMENSIONS: {new_tile_size}x{new_tile_size}")
    
    
    # ############################################ #
    # ### Step 5. Get Display Image Dimensions ### #
    # ############################################ #
    
    slide_new_dim = (int(slide_dim[0]/downscale_factor), int(slide_dim[1]/downscale_factor))
    
    # Print text on characteristics of slide if requested (verbose=True)
    if verbose:
        print("NEW SLIDE DIMENSIONS: ", slide_new_dim)
    

    # ####################################### #
    # ### Step 6. Conduct the Downscaling ### #
    # ####################################### #
    
    # Indicate that this may take a while if requested (verbose=True)
    if verbose:
        print("\n... STARTING LOAD AND RESIZE - WILL TAKE 15-60 SECONDS ON AVERAGE ...\n")    
    
    # Load the region --> Convert from RGBA to RGB --> Covert to UINT8 ...
    region = np.asarray(
        full_slide.read_region(location=(0,0), 
                               level=level_idx, 
                               size=slide_dim).convert('RGB'), 
        dtype=np.uint8)
    
    # ... --> Resize the region to the new slide dimensions
    dwn_slide = cv2.resize(region, (slide_new_dim))
    

    # ##############################################################################
    
    
    
    # ##############################################################################        
    #                        Creating the Label Color Map                          #
    # ##############################################################################
    
    
    # ############################################## #
    # ### Step 1. Initialize the Label Color Map ### #
    # ############################################## #
    
    #      - all squares are assumed to be background to begin with (0)
    c_lbl_map = np.zeros((slide_new_dim[1], slide_new_dim[0], 3), dtype=np.uint8)
    
    
    # ##################################################### #
    # ### Step 2. Loop Over DF & Update Label Color Map ### #
    # ##################################################### #
    
    for xmin, ymin, label in df.to_numpy():
        # Approximate Top-Left Corner X Value
        xmin = int(np.round(xmin/total_downscale_factor)) 
        
        # Approximate Top-Left Corner Y Value
        ymin = int(np.round(ymin/total_downscale_factor))
        
        # Update Color Map (white for uncertain, color-map for the rest)
        if not is_direct_annotation and label==uncertain_class: 
                c_lbl_map[ymin:ymin+new_tile_size, xmin:xmin+new_tile_size, :] = (0,0,0)
        else:
            c_lbl_map[ymin:ymin+new_tile_size, xmin:xmin+new_tile_size, :] = class_cmap[label]
    
    
    # ##############################################################################
    
    
    
    # ##############################################################################        
    #                Creating the Merged Image, Plotting and Saving                #
    # ##############################################################################
    
    
    # ######################################################### #
    # ### Step 1. Merge/Overlay the Slide & Label Color Map ### #
    # ######################################################### #
    overlayed_img = cv2.addWeighted(dwn_slide, core_opacity, c_lbl_map, 1-core_opacity, 1)
    
    
    # ########################################################### #
    # ### Step 2. Setup The Matplotlib Figure, Legend & Title ### #
    # ########################################################### #
    plt.figure(figsize=(20,20*(slide_new_dim[1]/slide_new_dim[0])))
    plt.imshow(overlayed_img)
    plt.legend(handles=legend_elements)
    plt.title(f"{path_to_slide} – SLIDE LEVEL LABEL IS {slide_label}", fontweight="bold")
    
    
    # ################################################# #
    # ### Step 3. Get Output Path & Save the Figure ### #
    # ################################################# #
    out_path = os.path.join(output_dir, path_to_slide.rsplit("/", 1)[1].rsplit(".", 1)[0]+".png")
    plt.savefig(out_path, bbox_inches='tight', dpi=figure_dpi)
    
    # Print where the file was saved if requested (verbose=1)
    if verbose:
        print(f"FILE SAVED TO --> {out_path}")
    
    # ############################################## #
    # ### Step 4. Display the Image If Requested ### #
    # ############################################## #
    if display:
        plt.show()
        
        
def slide_heuristic(df, class_list):
    val_counts = df["preds"].value_counts()
    max_count_label = val_counts.idxmax()
    max_count_2nd_label = df[df["preds"]!="no_tissue"]["preds"].value_counts().idxmax()
    
    n_tiles = len(df)
    value_percts = {c:val_counts.get(c, 0)/n_tiles for c in class_list}
    
    if value_percts["no_tissue"] > 0.985:
        return "no_tissue"
    elif value_percts["no_tissue"] > 0.75 and value_percts["out_of_focus"] >0.05:
        return "no_tissue"
    
    if value_percts["out_of_focus"] >0.2:
        return "out_of_focus"
    
    if max_count_label!="no_tissue":
        return max_count_label
    else:
        return max_count_2nd_label

def find_local_path(f_name, all_file_paths):
    """ Find Local Path From Image Name"""
    return [path for path in all_file_paths if f_name in path][0]


def get_all_paths(list_of_dir_paths):
    """ Function to get all file paths from directory paths 
    
    Args (list): List of strings pointing to directories containing
        slides on the local machine
        
    Returns: A list of full paths for every slide on the local machine
        to be searched later to based on file name
    """
    def __get_full_paths(dir_path):
        """ Helper Function """
        return [os.path.join(dir_path, f_name) for f_name in os.listdir(dir_path)]
    
    all_paths = [__get_full_paths(dir_path) for dir_path in list_of_dir_paths]    
    all_paths = [path for path_list in all_paths for path in path_list]
    
    return all_paths