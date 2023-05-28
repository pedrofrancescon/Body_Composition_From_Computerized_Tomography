#!/usr/bin/env python

from .Comp2Comp.comp2comp.inference_class_base import InferenceClass
from pathlib import Path

import os
import json
import subprocess
import shutil

class PayerPreprocessing(InferenceClass):
    def __init__(self, dicom_folder):
        super().__init__()
        self.dicom_folder = dicom_folder

    def __call__(self, inference_pipeline):
        
        preprocessed_image_folder = os.path.join(inference_pipeline.payer_tmp_folder, 'data_preprocessed')
        inference_pipeline.preprocessed_image_folder = preprocessed_image_folder
        inference_pipeline.basename = os.path.basename(self.dicom_folder)

        try:
            subprocess.check_output(['python', os.path.join(inference_pipeline.payer_bin_files, 'preprocess.py'),
                                    '--image_folder', self.dicom_folder,
                                    '--output_folder', preprocessed_image_folder,
                                    '--basename', inference_pipeline.basename], stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            raise Exception(f'Preprocessing failed with error [{e.returncode}]: {e.stdout}')
        
        return {}
    
class PayerSpineLocalization(InferenceClass):
    def __init__(self):
        super().__init__()

    def __call__(self, inference_pipeline):
        
        spine_localization_folder = os.path.join(inference_pipeline.payer_tmp_folder, 'spine_localization')
        
        try:
            subprocess.check_output(['python', os.path.join(inference_pipeline.payer_bin_files, 'main_spine_localization.py'),
                            '--image_folder', inference_pipeline.preprocessed_image_folder,
                            '--setup_folder', inference_pipeline.payer_tmp_folder,
                            '--model_files', os.path.join(inference_pipeline.payer_model_files, 'spine_localization'),
                            '--output_folder', spine_localization_folder], stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            raise Exception(f'SpineLocalization failed with error [{e.returncode}]: {e.stdout}')
        
        return {}
    
class PayerVertebraeLocalization(InferenceClass):
    def __init__(self):
        super().__init__()

    def __call__(self, inference_pipeline):

        vertebrae_localization_folder = os.path.join(inference_pipeline.payer_tmp_folder, 'vertebrae_localization')
        
        try:
            subprocess.check_output(['python', os.path.join(inference_pipeline.payer_bin_files, 'main_vertebrae_localization.py'),
                            '--image_folder', inference_pipeline.preprocessed_image_folder,
                            '--setup_folder', inference_pipeline.payer_tmp_folder,
                            '--model_files', os.path.join(inference_pipeline.payer_model_files, 'vertebrae_localization'),
                            '--output_folder', vertebrae_localization_folder], stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            raise Exception(f'VertebraeLocalization failed with error [{e.returncode}]: {e.stdout}')
        
        return {'vertebrae_localization_folder': vertebrae_localization_folder}
    

class L3Slicer(InferenceClass):
    def __init__(self):
        super().__init__()

    def __call__(self, inference_pipeline, vertebrae_localization_folder):
        
        try:
            centroids_path = os.path.join(vertebrae_localization_folder, inference_pipeline.basename + '_ctd.json')
            centroids = self.load_centroids(centroids_path)

            dicom_paths = os.path.join(inference_pipeline.preprocessed_image_folder, inference_pipeline.basename + '_paths.json')
            paths = self.load_json(dicom_paths)

            l3_z_coord = round(centroids['22']['z'])
            l3_dicom_path = paths[f'{l3_z_coord}']

            dicom_file_path = os.path.join(inference_pipeline.payer_tmp_folder, inference_pipeline.basename + '.dcm')

            shutil.copyfile(l3_dicom_path, dicom_file_path)
            
            inference_pipeline.dicom_file_paths = [Path(dicom_file_path)]
        except Exception as e:
            raise Exception(f'L3Slicer failed with error: {e}')
        
        return {}

    def load_centroids(self, json_path):
        dict_list = self.load_json(json_path)
        centroids = {}
        for d in dict_list:
            if 'direction' in d:
                centroids['direction'] = tuple(d['direction'])
            elif 'nan' in str(d): #skipping NaN centroids
                continue
            else:
                centroids[f'{d["label"]}'] = {'x': d['X'], 'y': d['Y'], 'z': d['Z']}
        return centroids
        
    def load_json(self, json_path):
        with open(json_path) as json_file:
            return json.load(json_file)