#!/usr/bin/env python

from Comp2Comp.comp2comp.inference_pipeline import InferencePipeline
from Comp2Comp.comp2comp.inference_class_base import InferenceClass

import os
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

def main():
    pipeline = InferencePipeline([
        PayerPreprocessing('/home/pedrofrancescon/Desktop/TCC_local/images/CIMAD/sorted/4899'),
        PayerSpineLocalization(),
        PayerVertebraeLocalization()
    ])

    dirname = dirname = os.path.dirname(os.path.abspath(__file__))
    pipeline.payer_bin_files = os.path.join(dirname, 'container', 'bin')
    pipeline.payer_model_files = os.path.join(dirname, 'container', 'models')
    # pipeline.payer_tmp_folder = tempfile.TemporaryDirectory()
    pipeline.payer_tmp_folder = os.path.join(dirname, 'tmp')

    pipeline()


if __name__ == "__main__":
    main()