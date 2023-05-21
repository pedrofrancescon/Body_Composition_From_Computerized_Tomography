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
        
        preprocessed_image_folder = os.path.join(inference_pipeline.payer_tmp_folder, 'payer_image_preprocessed')
        inference_pipeline.preprocessed_image_folder = preprocessed_image_folder

        subprocess.run(['python', os.path.join(inference_pipeline.payer_bin_files, 'preprocess.py'),
                        '--image_folder', self.dicom_folder,
                        '--output_folder', preprocessed_image_folder])
        
        return {}

def main():
    pipeline = InferencePipeline([
        PayerPreprocessing('/home/pedrofrancescon/Desktop/TCC_local/images/CIMAD/sorted/4899')
    ])

    dirname = dirname = os.path.dirname(os.path.abspath(__file__))
    pipeline.payer_bin_files = os.path.join(dirname, 'container', 'bin')
    # pipeline.payer_tmp_folder = tempfile.TemporaryDirectory()
    pipeline.payer_tmp_folder = os.path.join(dirname, 'tmp')

    pipeline()


if __name__ == "__main__":
    main()