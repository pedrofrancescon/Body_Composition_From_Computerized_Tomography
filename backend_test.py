#!/usr/bin/env python

from backend import dicom_info
from backend import process_dicom

if __name__ == "__main__":
    dcm_path = '/home/pedrofrancescon/Desktop/TCC_local/images/CIMAD/sorted/4899'
    info = dicom_info(dcm_path)
    print(info)
    try:
        process_dicom(dcm_path, '/home/pedrofrancescon/Desktop/TCC/backend/tmp')
    except Exception as err:
        print(err)