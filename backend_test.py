#!/usr/bin/env python

from backend import dicom_info
from backend import process_dicom

if __name__ == "__main__":
    dcm_path = 'D:\\Documentos\\TCC\\ImagensDICOM\\1.2.840.113619.2.417.3.2831161857.450.1676458320.10'
    info = dicom_info(dcm_path)
    print(info)
    try:
        process_dicom(dcm_path, 'D:\\Documentos\\TCC\\temp')
    except Exception as err:
        print(err)