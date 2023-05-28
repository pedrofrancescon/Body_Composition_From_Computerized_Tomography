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
ROOT = os.path.join(BASE_PATH, 'results/payer_l3')

for folder in os.listdir(ROOT):
    print(f'Processing {folder}')
    try:

        ds = pydicom.dcmread(os.path.join(ROOT, folder, f'{folder}.dcm'))
        l3 = ds.pixel_array
        print(l3.shape)
        print(type(l3))
        break

        cmap = plt.cm.gray
        image = cmap(dutils.wdw_sbone(l3))

        # save the image
        plt.imsave(f'results/comp2comp_l3/{folder}.png', image)
        # break
    except Exception as e:
        print(f'FAILED for {folder} with error {e}')