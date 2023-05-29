#!/usr/bin/env python

from backend import dicom_info
from backend import process_dicom

if __name__ == "__main__":
    dcm_path = '/media/viviane/2049235623EE23B2/Documentos/TCC/ImagensDICOM/1.2.840.113619.2.25.4.2147483647.1675110034.880'
    info = dicom_info(dcm_path)
    print(info)
    try:
        process_dicom(dcm_path, '/media/viviane/2049235623EE23B2/Documentos/TCC/temp')
    except Exception as err:
        print(err)