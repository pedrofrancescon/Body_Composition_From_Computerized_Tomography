#!/usr/bin/env python

import os
import tempfile
import argparse

from Comp2Comp.comp2comp.inference_pipeline import InferencePipeline
from Comp2Comp.comp2comp.muscle_adipose_tissue.muscle_adipose_tissue import (
    MuscleAdiposeTissueComputeMetrics,
    MuscleAdiposeTissueMetricsSaver,
    MuscleAdiposeTissuePostProcessing,
    MuscleAdiposeTissueSegmentation,
)
from Comp2Comp.comp2comp.muscle_adipose_tissue.muscle_adipose_tissue_visualization import (
    MuscleAdiposeTissueVisualizer,
)
from payer import (
    PayerPreprocessing,
    PayerSpineLocalization,
    PayerVertebraeLocalization,
    L3Slicer
)

os.environ['CUDA_VISIBLE_DEVICES'] = ""

def processDICOM(dicom_path, save_path):
    pipeline = InferencePipeline([
        PayerPreprocessing(dicom_path),
        PayerSpineLocalization(),
        PayerVertebraeLocalization(),
        L3Slicer(),
        MuscleAdiposeTissueSegmentation(16, 'abCT_v0.0.1'),
        MuscleAdiposeTissuePostProcessing(),
        MuscleAdiposeTissueComputeMetrics(),
        MuscleAdiposeTissueVisualizer(),
        MuscleAdiposeTissueMetricsSaver()
    ])

    with tempfile.TemporaryDirectory() as tmpdirname:
        dirname = os.path.dirname(os.path.abspath(__file__))
        pipeline.payer_bin_files = os.path.join(dirname, 'Payer', 'bin')
        pipeline.payer_model_files = os.path.join(dirname, 'Payer', 'models')
        pipeline.payer_tmp_folder = tmpdirname
        
        pipeline.model_dir = os.path.join(dirname, "Comp2Comp", "models")
        
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        
        pipeline.output_dir = save_path
        
        pipeline()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--dicom_path', type=str, required=True)
    parser.add_argument('--save_path', type=str, required=True)
    parser_args = parser.parse_args()
    processDICOM(parser_args.dicom_path, parser_args.save_path)