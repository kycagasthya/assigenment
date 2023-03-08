# Data Science Imports
import pandas as pd
import numpy as np

# Microscopy Related Imports
import openslide
import tifffile

# Cloud Related Imports
from google.cloud import storage

# Visualization Imports
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
import matplotlib.pyplot as plt
from tqdm.notebook import tqdm
import seaborn as sns
from PIL import Image
import cv2

# Built In Imports
import os
import gc


def get_overlay_objects(slide_name, all_csv_paths, all_slide_paths, output_dir,
                        label_dir="/home/jupyter/gt/", 
                        plot_size=1920,
                        return_label_object=True):    
    
    # Step 1: Get the prediction csv path
    if not slide_name.endswith(".csv"):
        slide_name+=".csv"
    
    pred_csv_path = [path for path in all_csv_paths if slide_name in path][0]
    
    # Step 2: Create the prediction dataframe and apply changes if necessary
    pred_df = pd.read_csv(pred_csv_path)
    pred_df["preds"] = pred_df["preds"].apply(lambda x: x.lower().replace(" ", "_"))
    pred_df["preds"] = pred_df["preds"].apply(lambda x: x.replace("necrotic", "exclusion"))
    
        
    # Step 3: Get path to the slide on the local machine
    path_to_slide_on_machine = find_local_path(pred_csv_path[:-4].rsplit("/", 1)[1], all_slide_paths)
    
        
    # Step 4: Remove the slide path column as we no longer need it
    pred_df.drop(columns=["slide_path"], inplace=True)
    
    # Step 5: Create the prediction overlay tool
    pred_overlay = OverlayTool(pred_df, output_dir, path_to_slide_on_machine)
    
    # Step 6: Attempt to follow the Steps 1-5 (skip step 3) for the Ground Truth CSV if it exists
    label_csv_path = os.path.join(label_dir, pred_csv_path.rsplit("/", 1)[1])
    if return_label_object and os.path.isfile(label_csv_path):
        # Step 1B
        label_df = pd.read_csv(label_csv_path)
        
        # Step 2B
        label_df["preds"] = label_df["preds"].apply(lambda x: x.lower().replace(" ", "_"))
        label_df["preds"] = label_df["preds"].apply(lambda x: x.replace("necrotic", "exclusion"))
        
        # Step 4B
        label_df.drop(columns=["slide_path"], inplace=True)
        
        # Step 5B
        label_overlay = OverlayTool(label_df, output_dir, path_to_slide_on_machine)        
        return pred_overlay, label_overlay
    else:
        return pred_overlay, None
    

def do_evaluation(all_csv_paths, 
                  all_slide_paths, 
                  class_list=(
                      'out_of_focus', 'dim_positive', 'he', 'negative', 
                      'no_tissue','exclusion', 'strong_positive')
                 ):
    """ Conduct evaluation on file-list using csv predictions """
    def __do_binary(pred):
        """ Add binary classification score columns """
        if pred in (["no_tissue", "out_of_focus"]):
            return "BAD"
        else:
            return "GOOD"
        
    slide_prediction_df = pd.DataFrame(columns=class_list)
    for i, f_name in tqdm(enumerate(all_csv_paths), total=(len(all_csv_paths))):
        edge_preds, gt_labels = get_overlay_objects(slide_name=f_name, all_csv_paths=all_csv_paths, all_slide_paths=all_slide_paths, output_dir="/tmp", plot_size=100, return_label_object=False)
        edge_df = pd.DataFrame(edge_preds.frac_map_tissue, index=[f_name])
        edge_df["no_tissue"] = edge_preds.frac_map_all["no_tissue"]
        edge_df["heuristic_pred"] = edge_preds.slide_heuristic_label
        edge_df["folder_gt_label"] = determine_local_label(edge_preds.path_to_slide)
        slide_prediction_df = pd.concat([slide_prediction_df, edge_df],)
        
    slide_prediction_df.fillna(0, inplace=True)
    slide_prediction_df["heuristic_binary_pred"] = slide_prediction_df.heuristic_pred.apply(__do_binary)
    slide_prediction_df["folder_binary_gt_label"] = slide_prediction_df.folder_gt_label.apply(__do_binary)
    return slide_prediction_df
    
    
def return_path_dirs(
    path_to_oof_dir = "/home/jupyter/data/Focus/Out_Focus",
    path_to_no_tissue_dir = "/home/jupyter/data/Tissue/No_Tissue",
    path_to_dim_dir = "/home/jupyter/data/Stained/Dim",
    path_to_str_dir = "/home/jupyter/data/Stained/Yes",
    path_to_neg_dir = "/home/jupyter/data/Stained/No",
    path_to_he_dir = "/home/jupyter/data/H&E"):
    """ Return local directory paths """
    return path_to_oof_dir, path_to_no_tissue_dir, path_to_dim_dir, path_to_str_dir, path_to_neg_dir, path_to_he_dir



def find_local_path(f_name, all_file_paths):
    """ Find Local Path From Image Name"""
    if ".svs" not in f_name and ".qptiff" not in f_name:
        try:
            return [path for path in all_file_paths if f_name+".svs" in path][0]
        except:
            return [path for path in all_file_paths if f_name+".qptiff" in path][0]
    else:
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


def determine_local_label(slide_path, custom_fn=None):
    """ Simple function to determine class label from image path """
    
    if not custom_fn:
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
        elif "H&E" in slide_path:
            return "he"
    else:
        return custom_fn(slide_path)
    

class OverlayTool:
    """ This class if a bundling of the above functions in a custom configuration """
    def __init__(
        self, df, output_dir, path_to_slide, 
        gt_slide_label=None, cmap_name="bright", uncertain_class="-1",
        max_edge_size=1920, original_tile_size=1024, 
        class_list=(
            'out_of_focus', 'dim_positive', 'he', 'negative', 
            'no_tissue','exclusion', 'strong_positive')
    ):
        """ This function is called when a given object is created
        
        Args:
            df (pd.DataFrame): 
                Containing at least the following columns
                    --> x_coord (int)
                    --> y_coord (int)
                    --> label (str)
            output_dir (str): Path to the directory to save the overlay
            path_to_slide (str): Path to the slide (on local where it can be loaded)
            gt_slide_label (str, optional): The ground truth label to apply
            max_size (int, optional): The maximum side length to constrain the overlay's longest side to
            cmap_name (str, optional): Name of the seaborn color palette to use.
                LINK --> https://seaborn.pydata.org/tutorial/color_palettes.html
            uncertain_class (str, optional): The name given to the uncertain class
                - Often this is -1
            max_edge_size (int, optional): The maximum edge size to use when
                resizing/downsampling the slide.
            original_tile_size (int, optional): Original size of the tiles that were 
                predicted upon by the model
            class_list (tuple, optional): List of classes to be used that will tie the 
                label in the df to a specific colour in the legend/color-palette
        """
        
        # Initialize Basic Attributes
        self.df=df[["x_coords", "y_coords", "preds"]]
        self.cmap_name = cmap_name
        self.output_dir=output_dir
        self.path_to_slide=path_to_slide
        self.max_edge_size=max_edge_size
        self.original_tile_size=original_tile_size
        self.slide=openslide.OpenSlide(path_to_slide)
        self.gt_slide_label=gt_slide_label
        self.classes=class_list
        self.uncertain_class=uncertain_class        
        
        # Initialization Methods to Initialize Remaining Attributes
        self.initialize_color()
        self.initialize_dwnsampled_slide()
        self.initialize_frac_maps()        
        self.heuristic_slide_classification()
        self.initialize_lbl_color_map()
        
        # Initialization as placeholder
        self.merged_img = None
        
    def initialize_frac_maps(self):
        """ Function to initialize the fractional maps used in heuristic labelling 
        
        Args:
            None, self only; The following attributes are used:
                --> self.df
                --> self.slide_new_dim
                --> self.new_tile_size
            
        Returns:
            None; The following attributes are set:
                --> self.frac_map_tissue
                --> self.frac_map_all
        
        """
        
        # Get approximate number of total tiles expected (useful for GT slides)
        n_tiles_total = int(
            (self.slide_new_dim[0]*self.slide_new_dim[1])/ \
            (self.new_tile_size*self.new_tile_size)
        )
        
        # Calculate fractional map for tissue distribution
        tissue_value_counts = self.df[self.df.preds!="no_tissue"]["preds"].value_counts()
        self.frac_map_tissue = {k:0.0 for k in self.classes if k!="no_tissue"}
        self.frac_map_tissue.update({k:v/tissue_value_counts.sum() for k,v in tissue_value_counts.items()})
        
        # Calculate all known predictions as a fractional map
        known_value_counts = self.df.preds.value_counts()
        self.frac_map_all = {k:0.0 for k in self.classes}
        self.frac_map_all.update({k:v/max(known_value_counts.sum(), n_tiles_total) for k,v in known_value_counts.items()})
        
        # Update if labelled data includes auto-annotated background tissue
        if n_tiles_total>known_value_counts.sum():
            self.frac_map_all["no_tissue"]=(known_value_counts.get("no_tissue",0)+(n_tiles_total-known_value_counts.sum()))/n_tiles_total
    
    
    def initialize_color(self):
        """ Method to initialize color/display related things 
        
        Args:
            None, self only; The following attributes are used:
                --> self.cmap_name
                --> self.classes
            
        Returns:
            None; The following attributes are set:
                --> self.cpal_map
                --> self.class_cpal
                --> self.class_cmap
        """
        
        # Get and set color-palette map in original data type
        self.cpal_map = sns.color_palette(self.cmap_name, len(self.classes))
        
        # Create palette that is appropriate data type/scale
        self.class_cpal = np.uint8(np.array(self.cpal_map)*255)
        
        # Create color-mapping from class to color from cpal
        self.class_cmap = {c:self.class_cpal[i] for i,c in enumerate(self.classes)}

    def initialize_dwnsampled_slide(self):
        """ Method to initialize downsampled image 
        
        Args:
            None, self only; The following attributes are used:
                --> self.slide
            
        Returns:
            None; The following attributes are set:
                --> self.level_idx
                --> self.start_dwnsample
                --> self.slide_dim
                --> self.downscale_factor
                --> self.total_downscale_factor
                --> self.new_tile_size
                --> self.slide_new_dim
                --> self.dwn_slide
        """
        
        self.level_idx = self.slide.level_count-1 
        self.start_dwnsample = self.slide.level_downsamples[-1]
        self.slide_dim = self.slide.level_dimensions[-1]
        self.downscale_factor = max(self.slide_dim)/self.max_edge_size
        self.total_downscale_factor = self.downscale_factor*self.start_dwnsample
        self.new_tile_size = int(np.ceil(self.original_tile_size/(self.total_downscale_factor)))
        self.slide_new_dim = (
            int(self.slide_dim[0]/self.downscale_factor), 
            int(self.slide_dim[1]/self.downscale_factor)
        )
        region = np.asarray(
            self.slide.read_region(location=(0,0), 
                                   level=self.level_idx, 
                                   size=self.slide_dim).convert('RGB'), 
            dtype=np.uint8)    
        self.dwn_slide = cv2.resize(region, (self.slide_new_dim))
        
    def initialize_lbl_color_map(self):
        """ Method to initialize the label color map grid visual
        
        Args:
            None, self only; The following attributes are used:
                --> self.slide_new_dim
                --> self.df
                --> self.new_tile_size
                --> self.class_cmap
                --> self.total_downscale_factor
                --> self.uncertain_class
            
        Returns:
            None; The following attributes are set:
                --> self.c_lbl_map
        """
        self.c_lbl_map = np.ones((self.slide_new_dim[1], self.slide_new_dim[0], 3), dtype=np.uint8)*255
        for xmin, ymin, label in self.df.to_numpy():
            # Approximate Top-Left Corner X Value
            xmin = int(np.round(xmin/self.total_downscale_factor)) 

            # Approximate Top-Left Corner Y Value
            ymin = int(np.round(ymin/self.total_downscale_factor))

            # Update Color Map (white for uncertain, color-map for the rest)
            if label==self.uncertain_class: 
                    self.c_lbl_map[ymin:ymin+self.new_tile_size, xmin:xmin+self.new_tile_size, :] = (0,0,0)
            else:
                self.c_lbl_map[ymin:ymin+self.new_tile_size, xmin:xmin+self.new_tile_size, :] = self.class_cmap[label]
                    
    def heuristic_slide_classification(self, 
                                       str_thresh=0.150,
                                       oof_thresh=0.015,
                                       dim_thresh=0.225,
                                       neg_thresh=0.225,
                                       he_thresh=0.225,
                                       not_thresh=0.99,):
        """ Method to determine slide level class
        
        Args:
            str_thresh (float, optional): Lower threshold for fractional slide level determination
                --> Strong-Positive Label
            oof_thresh (float, optional): Lower threshold for fractional slide level determination
                --> Out-Of-Focus Label
            dim_thresh (float, optional): Lower threshold for fractional slide level determination
                --> Dim-Positive Label
            neg_thresh (float, optional): Lower threshold for fractional slide level determination
                --> Negative Label
            he_thresh (float, optional): Lower threshold for fractional slide level determination
                --> H&E Label
            not_thresh (float, optional): Lower threshold for fractional slide level determination
                --> No-Tissue Label
            
            The following object attributes are also used:
                --> self.frac_map_tissue
                --> self.frac_map_all
            
        Returns:
            None; The following attributes are set:
                --> self.slide_heuristic_label
        """
        # If not strong-positive... use strong-positive in dim-threshold determination
        all_positive_tissue = \
            self.frac_map_tissue.get("dim_positive", 0.0)+ \
            self.frac_map_tissue.get("strong_positive", 0.0)
        
        # Main logic loop
        #  1. No Tissue
        #  2. Strong Positive
        #  3. Out Of Focus
        #  4. Dim Positive
        #  5. Negative
        #  6. H&E
        #  7. Uncertain
        if self.frac_map_all.get("no_tissue", 0.0) <= not_thresh:
            if self.frac_map_tissue.get("strong_positive", 0.0) <= str_thresh:
                if self.frac_map_tissue.get("out_of_focus", 0.0) <= oof_thresh:
                    if all_positive_tissue <= dim_thresh:
                        if self.frac_map_tissue.get("negative", 0.0) <= neg_thresh:
                            if self.frac_map_tissue.get("he", 0.0) <= he_thresh:
                                self.slide_heuristic_label="uncertain"
                            else:
                                self.slide_heuristic_label="he"
                        else:
                            self.slide_heuristic_label="negative"
                    else:
                        self.slide_heuristic_label="dim_positive"
                else: 
                    self.slide_heuristic_label="out_of_focus"
            else:
                self.slide_heuristic_label="strong_positive"
        else:            
            self.slide_heuristic_label="no_tissue"
    
    
    def plot_merged(self, bg_opacity=0.65, fig_multiplier=20, gt_slide_label=None, subregion=None, save_to_dir=None):
        """ Method to plot color map overlayed ontop of the downsampled image
        
        Args:
            bg_opacity (float, optional):
            fig_multiplier (int, optional):
            gt_slide_label (str, optional):
            subregion (tuple of ints, optional):
            save_to_dir (str, optional): 
            
            The following object attributes are also used:
                --> self.gt_slide_label
                --> self.merged_igm
                --> self.c_lbl_map
                --> self.cpal_map
                --> self.path_to_slide
                --> self.slide_heuristic_label
                --> self.slide_new_dim
                --> self.classes
            
        Returns:
            None; An image is plotted and potentially saved to disk.
                  The self.merged_img attribute may also be updated
        """
        # If the ground truth slide label already exists use that...
        # if not set it to be the default attribute of the object
        if not gt_slide_label and self.gt_slide_label:
            gt_slide_label=self.gt_slide_label
            
        # Create the merged image if it does not already exist
        if self.merged_img is None:
            self.merged_img = cv2.addWeighted(
                self.dwn_slide, bg_opacity, self.c_lbl_map, 1-bg_opacity, 1
            )
        
        # Drill down to a specific subregion of the image if requested
        if subregion is not None:
            merged_img = self.merged_img[subregion[1]:subregion[3], subregion[0]:subregion[2], :]
        else:
            merged_img = self.merged_img
            
        # Design the legend
        legend_elements = [
            Patch(facecolor=np.append(c,1-bg_opacity), label=self.classes[i]) \
            for i,c in enumerate(self.cpal_map)
        ]
        legend_elements.append(Patch(facecolor=(1,1,1,1-bg_opacity), edgecolor=(0,0,0,0.1), label="background"))
        legend_elements.append(Patch(facecolor=(0,0,0,1-bg_opacity), label="uncertain"))

        # Craft the Figure to be displayed
        plt.figure(figsize=(fig_multiplier,fig_multiplier*(self.slide_new_dim[1]/self.slide_new_dim[0])))
        plt.imshow(merged_img)
        plt.legend(handles=legend_elements)
        title_str = f"{self.path_to_slide}\nHEURISTIC LABEL IS {self.slide_heuristic_label}"
        if gt_slide_label:
            title_str+=f"\nGROUND TRUTH LABEL IS {gt_slide_label}"
        
        # Adjust the grid respective to the subregion
        if subregion is not None:
            plt.xticks(ticks=np.linspace(0, subregion[2]-subregion[0], 10), labels=np.linspace(subregion[0], subregion[2], 10, dtype=np.int32))
            plt.yticks(ticks=np.linspace(0, subregion[3]-subregion[1], 10), labels=np.linspace(subregion[1], subregion[3], 10, dtype=np.int32))
            title_str+=f"\nSUBREGION: {subregion}"
        plt.title(title_str, fontweight="bold")
        plt.grid(color="gray", linestyle=":")
        
        # If we want to save to file. Do so
        if save_to_dir is not None:
            plt.savefig(os.path.join(save_to_dir, "color_maps", self.path_to_slide[:-4].rsplit("/", 1)[1]+".png"), dpi=150)
            
        # Display the image
        plt.show()

    def plot_slide_only(self, fig_multiplier=20, gt_slide_label=None, subregion=None, save_to_dir=None):
        """ Method to plot only the downsampled slide 
        
        Args:
            fig_multiplier (int, optional):
            gt_slide_label (str, optional):
            subregion (tuple of ints, optional):
            save_to_dir (str, optional): 
            
            The following object attributes are also used:
                --> self.gt_slide_label
                --> self.dwn_slide
                --> self.path_to_slide
                --> self.slide_heuristic_label
                --> self.slide_new_dim
            
        Returns:
            None; An image is plotted and potentially saved to disk.
        """
        
        # If the ground truth slide label already exists use that...
        # if not set it to be the default attribute of the object
        if not gt_slide_label and self.gt_slide_label:
            gt_slide_label=self.gt_slide_label
        
        # Drill down to a specific subregion of the image if requested
        if subregion is not None:
            dwn_slide = self.dwn_slide[subregion[1]:subregion[3], subregion[0]:subregion[2], :]
        else:
            dwn_slide = self.dwn_slide

        # Craft the Figure to be displayed
        plt.figure(figsize=(fig_multiplier,fig_multiplier*(self.slide_new_dim[1]/self.slide_new_dim[0])))
        plt.imshow(dwn_slide)
        title_str = f"{self.path_to_slide}\nHEURISTIC LABEL IS {self.slide_heuristic_label}"
        if gt_slide_label:
            title_str+=f"\nGROUND TRUTH LABEL IS {gt_slide_label}"
        
        # Adjust the grid respective to the subregion
        if subregion is not None:
            title_str+=f"\nSUBREGION: {subregion}"
            plt.xticks(ticks=np.linspace(0, subregion[2]-subregion[0], 10), labels=np.linspace(subregion[0], subregion[2], 10, dtype=np.int32))
            plt.yticks(ticks=np.linspace(0, subregion[3]-subregion[1], 10), labels=np.linspace(subregion[1], subregion[3], 10, dtype=np.int32))
            
        plt.title(title_str, fontweight="bold")
        plt.grid(color="gray", linestyle=":")
        
        # If we want to save to file. Do so
        if save_to_dir is not None:
            plt.savefig(os.path.join(save_to_dir, "slide_only", self.path_to_slide[:-4].rsplit("/", 1)[1]+".png"), dpi=150)
        
        # Display the image
        plt.show()


    def plot_side_by_side(self, bg_opacity=0.65, fig_multiplier=20, gt_slide_label=None, subregion=None):
        """ Method to plot the overlayed color map grid beside the original image 
        
        Args:
            bg_opacity (float, optional):
            fig_multiplier (int, optional):
            gt_slide_label (str, optional):
            subregion (tuple of ints, optional):
            
            The following object attributes are also used:
                --> self.gt_slide_label
                --> self.dwn_slide
                --> self.path_to_slide
                --> self.slide_heuristic_label
                --> self.slide_new_dim
                --> self.dwn_slide
                --> self.c_lbl_map
                --> self.cpal_map
                --> self.classes
            
        Returns:
            None; An image is plotted and potentially saved to disk.
                  The self.merged_img attribute may also be updated
        """
        
        # If the ground truth slide label already exists use that...
        # if not set it to be the default attribute of the object
        if not gt_slide_label and self.gt_slide_label:
            gt_slide_label=self.gt_slide_label
        
        # Create the merged image if it does not already exist
        if self.merged_img is None:
            self.merged_img = cv2.addWeighted(
                self.dwn_slide, bg_opacity, self.c_lbl_map, 1-bg_opacity, 1
            )
            
        # Drill down to a specific subregion of the image if requested
        if subregion is not None:
            merged_img = self.merged_img[subregion[1]:subregion[3], subregion[0]:subregion[2], :]
            dwn_slide = self.dwn_slide[subregion[1]:subregion[3], subregion[0]:subregion[2], :]
        else:
            merged_img = self.merged_img
            dwn_slide = self.dwn_slide
            
        # Craft the legend
        legend_elements = [
            Patch(facecolor=np.append(c,1-bg_opacity), label=self.classes[i]) \
            for i,c in enumerate(self.cpal_map)
        ]
        legend_elements.append(Patch(facecolor=(1,1,1,1-bg_opacity), edgecolor=(0,0,0,0.1), label="background"))
        legend_elements.append(Patch(facecolor=(0,0,0,1-bg_opacity), label="uncertain"))

        # Craft the Figure to be displayed
        plt.figure(figsize=(fig_multiplier,fig_multiplier*(self.slide_new_dim[1]/self.slide_new_dim[0])))
        
        # COLOR MAP OVERLAY
        plt.subplot(1,2,1)
        plt.imshow(merged_img)
        plt.legend(handles=legend_elements)
        title_str = f"{self.path_to_slide}\nHEURISTIC LABEL IS {self.slide_heuristic_label}"
        if gt_slide_label:
            title_str+=f"\nGROUND TRUTH LABEL IS {gt_slide_label}"
            
        # Adjust the grid respective to the subregion
        if subregion is not None:
            title_str+=f"\nSUBREGION: {subregion}"
            plt.xticks(ticks=np.linspace(0, subregion[2]-subregion[0], 10), labels=np.linspace(subregion[0], subregion[2], 10, dtype=np.int32))
            plt.yticks(ticks=np.linspace(0, subregion[3]-subregion[1], 10), labels=np.linspace(subregion[1], subregion[3], 10, dtype=np.int32))
        plt.title(title_str, fontweight="bold")
        plt.grid(color="gray", linestyle=":")
        
        # RAW IMAGE DISPLAY
        plt.subplot(1,2,2)
        plt.imshow(dwn_slide)
        title_str = f"{self.path_to_slide}\nHEURISTIC LABEL IS {self.slide_heuristic_label}"
        if gt_slide_label:
            title_str+=f"\nGROUND TRUTH LABEL IS {gt_slide_label}"
        if subregion is not None:
            title_str+=f"\nSUBREGION: {subregion}"
            plt.xticks(ticks=np.linspace(0, subregion[2]-subregion[0], 10), labels=np.linspace(subregion[0], subregion[2], 10, dtype=np.int32))
            plt.yticks(ticks=np.linspace(0, subregion[3]-subregion[1], 10), labels=np.linspace(subregion[1], subregion[3], 10, dtype=np.int32))
        plt.title(title_str, fontweight="bold")
        plt.grid(color="gray", linestyle=":")
        plt.show()

        
def mass_visualization(list_of_names, plot_size, all_csv_paths, all_slide_paths, show_frac_map=True, style="side_by_side"):
    """ Tool allowing for visualization of multiple images """
    
    for i, f_name in enumerate(list_of_names):
        edge_preds, gt_labels = get_overlay_objects(slide_name=f_name, 
                                                    plot_size=plot_size, 
                                                    all_csv_paths=all_csv_paths, 
                                                    all_slide_paths=all_slide_paths, 
                                                    output_dir="/tmp")
        print("\n\n-----------------------------------------------------------------------------------------------------------------\n\n")
        print(f"                                          SLIDE NAME: {f_name[:-4]}")
        print("\n\n-----------------------------------------------------------------------------------------------------------------\n\n")
        if gt_labels and show_frac_map:
            print("---------- GROUND TRUTH LABEL DISTRIBUTION ----------\n")
            for k,v in {k:v for k,v in sorted(gt_labels.frac_map_tissue.items(), key=lambda x: x[1], reverse=True)}.items(): 
                print(f"{k}\n\t%{v*100:0.2f}")
        if show_frac_map:
            print("\n\n---------- PREDICTION DISTRIBUTION ----------\n")
            for k,v in {k:v for k,v in sorted(edge_preds.frac_map_tissue.items(), key=lambda x: x[1], reverse=True)}.items(): 
                print(f"{k}\n\t%{v*100:0.2f}")
            print("\n\n")
        
        if style=="side_by_side":
            if gt_labels:
                gt_labels.plot_side_by_side()
            edge_preds.plot_side_by_side()
        elif style=="slide_only":
            if gt_labels:
                gt_labels.plot_slide_only()
            edge_preds.plot_slide_only()
        else:
            if gt_labels:
                gt_labels.plot_merged()
            edge_preds.plot_merged()
        print("\n\n-----------------------------------------------------------------------------------------------------------------\n\n")