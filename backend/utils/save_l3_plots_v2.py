"""
  Module:  dicom_to_nifti.py
  Nov 28, 2019
  David Gobbi
"""

import pydicom
import nibabel as nib
import numpy as np
import sys
import os
import matplotlib.pyplot as plt
import nibabel as nib
import verse.utils.data_utilities as dutils
import pandas as pd


BASE_PATH = ''
ROOT = os.path.join(BASE_PATH, 'backend/Comp2Comp/outputs/2023-04-24_15-43-08')

for folder in os.listdir(ROOT):
    print(f'Processing {folder}')
    try:

        metric_path = os.path.join(ROOT, folder, "metrics/muscle_adipose_tissue_metrics.csv")
        metrics = pd.read_csv(metric_path, index_col='File Name')
        dicom_path = metrics.loc['L3']['File Path']

        ds = pydicom.dcmread(dicom_path)
        image = ds.pixel_array
        try:
            slope = float(ds.RescaleSlope)
        except (AttributeError, ValueError):
            slope = 1.0
        try:
            intercept = float(ds.RescaleIntercept)
        except (AttributeError, ValueError):
            intercept = 0.0
        l3 = image*slope + intercept

        cmap = plt.cm.gray
        image = cmap(dutils.wdw_hbone(l3))

        # save the image
        plt.imsave(f'results/comp2comp_l3/{folder}.png', image)
    except Exception as e:
        print(f'FAILED for {folder} with error {e}')