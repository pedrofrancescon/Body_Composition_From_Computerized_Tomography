#!/usr/bin/env python

import pydicom
import argparse
import os

def dicom_info(dicom_path):
    for root, _, files in os.walk(dicom_path):
        for file in files: 
            if ".dcm" in file: # exclude non-dicoms, good for messy folders
                ds = pydicom.read_file(os.path.join(root, file), force=True)
                return {"id": ds.get("PatientID", "NA")}
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--dicom_path', type=str, required=True)
    parser_args = parser.parse_args()
    info = dicom_info(parser_args.dicom_path)
    print(info)