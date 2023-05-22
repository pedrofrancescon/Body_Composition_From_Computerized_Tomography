#!/usr/bin/env python

from Comp2Comp.comp2comp.inference_pipeline import InferencePipeline
from Comp2Comp.comp2comp.inference_class_base import InferenceClass

import os
import json
import subprocess
import tempfile

class PayerPreprocessing(InferenceClass):
    def __init__(self, dicom_folder):
        super().__init__()
        self.dicom_folder = dicom_folder

    def __call__(self, inference_pipeline):
        
        preprocessed_image_folder = os.path.join(inference_pipeline.payer_tmp_folder, 'data_preprocessed')
        inference_pipeline.preprocessed_image_folder = preprocessed_image_folder
        inference_pipeline.basename = os.path.basename(self.dicom_folder)

        subprocess.run(['python', os.path.join(inference_pipeline.payer_bin_files, 'preprocess.py'),
                        '--image_folder', self.dicom_folder,
                        '--output_folder', preprocessed_image_folder,
                        '--basename', inference_pipeline.basename])
        
        return {}
    
class PayerSpineLocalization(InferenceClass):
    def __init__(self):
        super().__init__()

    def __call__(self, inference_pipeline):
        
        spine_localization_folder = os.path.join(inference_pipeline.payer_tmp_folder, 'spine_localization')
        
        subprocess.run(['python', os.path.join(inference_pipeline.payer_bin_files, 'main_spine_localization.py'),
                        '--image_folder', inference_pipeline.preprocessed_image_folder,
                        '--setup_folder', inference_pipeline.payer_tmp_folder,
                        '--model_files', os.path.join(inference_pipeline.payer_model_files, 'spine_localization'),
                        '--output_folder', spine_localization_folder])
        
        return {}
    
class PayerVertebraeLocalization(InferenceClass):
    def __init__(self):
        super().__init__()

    def __call__(self, inference_pipeline):

        vertebrae_localization_folder = os.path.join(inference_pipeline.payer_tmp_folder, 'vertebrae_localization')
        
        subprocess.run(['python', os.path.join(inference_pipeline.payer_bin_files, 'main_vertebrae_localization.py'),
                        '--image_folder', inference_pipeline.preprocessed_image_folder,
                        '--setup_folder', inference_pipeline.payer_tmp_folder,
                        '--model_files', os.path.join(inference_pipeline.payer_model_files, 'vertebrae_localization'),
                        '--output_folder', vertebrae_localization_folder])
        
        return {'vertebrae_localization_folder': vertebrae_localization_folder}
    

class L3Slicer(InferenceClass):
    def __init__(self):
        super().__init__()

    def __call__(self, inference_pipeline, vertebrae_localization_folder):
        
        centroids_path = os.path.join(vertebrae_localization_folder, inference_pipeline.basename + '_ctd.json')
        centroids = self.load_centroids(centroids_path)

        dicom_paths = os.path.join(inference_pipeline.preprocessed_image_folder, inference_pipeline.basename + '_paths.json')
        paths = self.load_json(dicom_paths)

        l3_z_coord = round(centroids['22']['z'])
        l3_dicom_path = paths[f'{l3_z_coord}']
        
        inference_pipeline.dicom_file_paths = [l3_dicom_path]
        
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

def main():
    pipeline = InferencePipeline([
        PayerPreprocessing('/home/pedrofrancescon/Desktop/TCC_local/images/CIMAD/sorted/4899'),
        PayerSpineLocalization(),
        PayerVertebraeLocalization(),
        L3Slicer()
    ])

    dirname = dirname = os.path.dirname(os.path.abspath(__file__))
    pipeline.payer_bin_files = os.path.join(dirname, 'container', 'bin')
    pipeline.payer_model_files = os.path.join(dirname, 'container', 'models')
    # pipeline.payer_tmp_folder = tempfile.TemporaryDirectory()
    pipeline.payer_tmp_folder = os.path.join(dirname, 'tmp')

    pipeline()


if __name__ == "__main__":
    main()