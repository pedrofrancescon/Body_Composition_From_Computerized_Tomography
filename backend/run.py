#!/usr/bin/env python

import os

from Comp2Comp.comp2comp.inference_pipeline import InferencePipeline
from Comp2Comp.comp2comp.muscle_adipose_tissue.muscle_adipose_tissue import (
    MuscleAdiposeTissueComputeMetrics,
    MuscleAdiposeTissueH5Saver,
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

import tempfile

os.environ['CUDA_VISIBLE_DEVICES'] = ""

# TODO create custom InferenceClass for Payer algorithm

def main():
    pipeline = InferencePipeline([
        PayerPreprocessing('/home/pedrofrancescon/Desktop/TCC_local/images/CIMAD/sorted/4899'),
        PayerSpineLocalization(),
        PayerVertebraeLocalization(),
        L3Slicer(),
        MuscleAdiposeTissueSegmentation(16, 'abCT_v0.0.1'),
        MuscleAdiposeTissuePostProcessing(),
        MuscleAdiposeTissueComputeMetrics(),
        MuscleAdiposeTissueVisualizer(),
        # MuscleAdiposeTissueH5Saver(),
        MuscleAdiposeTissueMetricsSaver()
    ])

    dirname = os.path.dirname(os.path.abspath(__file__))
    
    pipeline.payer_bin_files = os.path.join(dirname, 'container', 'bin')
    pipeline.payer_model_files = os.path.join(dirname, 'container', 'models')
    pipeline.payer_tmp_folder = os.path.join(dirname, 'tmp')
    
    pipeline.model_dir = os.path.join(dirname, "Comp2Comp/models")
    pipeline.output_dir = os.path.join(dirname, "tmp")
    
    pipeline()

if __name__ == "__main__":
    main()