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


def create_affine(ipp, iop, ps):
    """Generate a NIFTI affine matrix from DICOM IPP and IOP attributes.
    The ipp (ImagePositionPatient) parameter should an Nx3 array, and
    the iop (ImageOrientationPatient) parameter should be Nx6, where
    N is the number of DICOM slices in the series.
    The return values are the NIFTI affine matrix and the NIFTI pixdim.
    Note the the output will use DICOM anatomical coordinates:
    x increases towards the left, y increases towards the back.
    """
    # solve Ax = b where x is slope, intecept
    n = ipp.shape[0]
    A = np.column_stack([np.arange(n), np.ones(n)])
    x, r, rank, s = np.linalg.lstsq(A, ipp, rcond=None)
    # round small values to zero
    x[(np.abs(x) < 1e-6)] = 0.0
    vec = x[0,:] # slope
    pos = x[1,:] # intercept

    # pixel spacing should be the same for all image
    spacing = np.ones(3)
    spacing[0:2] = ps[0,:]
    if np.sum(np.abs(ps - spacing[0:2])) > spacing[0]*1e-6:
        sys.stderr.write("Pixel spacing is inconsistent!\n");

    # compute slice spacing
    spacing[2] = np.round(np.sqrt(np.sum(np.square(vec))), 7)

    # get the orientation
    iop_average = np.mean(iop, axis=0)
    u = iop_average[0:3]
    u /= np.sqrt(np.sum(np.square(u)))
    v = iop_average[3:6]
    v /= np.sqrt(np.sum(np.square(v)))

    # round small values to zero
    u[(np.abs(u) < 1e-6)] = 0.0
    v[(np.abs(v) < 1e-6)] = 0.0

    # create the matrix
    mat = np.eye(4)
    mat[0:3,0] = u*spacing[0]
    mat[0:3,1] = v*spacing[1]
    mat[0:3,2] = vec
    mat[0:3,3] = pos

    # check whether slice vec is orthogonal to iop vectors
    dv = np.dot(vec, np.cross(u, v))
    qfac = np.sign(dv)
    if np.abs(qfac*dv - spacing[2]) > 1e-6:
        sys.stderr.write("Non-orthogonal volume!\n");

    # compute the nifti pixdim array
    pixdim = np.hstack([np.array(qfac), spacing])

    return mat, pixdim


def convert_coords(vol, mat):
    """Convert a volume from DICOM coords to NIFTI coords or vice-versa.
    For DICOM, x increases to the left and y increases to the back.
    For NIFTI, x increases to the right and y increases to the front.
    The conversion is done in-place (volume and matrix are modified).
    """
    # the x direction and y direction are flipped
    convmat = np.eye(4)
    convmat[0,0] = -1.0
    convmat[1,1] = -1.0

    # apply the coordinate change to the matrix
    mat[:] = np.dot(convmat, mat)

    # look for x and y elements with greatest magnitude
    xabs = np.abs(mat[:,0])
    yabs = np.abs(mat[:,1])
    xmaxi = np.argmax(xabs)
    yabs[xmaxi] = 0.0
    ymaxi = np.argmax(yabs)

    # re-order the data to ensure these elements aren't negative
    # (this may impact the way that the image is displayed, if the
    # software that displays the image ignores the matrix).
    if mat[xmaxi,0] < 0.0:
        # flip x
        vol[:] = np.flip(vol, 2)
        mat[:,3] += mat[:,0]*(vol.shape[2] - 1)
        mat[:,0] = -mat[:,0]
    if mat[ymaxi,1] < 0.0:
        # flip y
        vol[:] = np.flip(vol, 1)
        mat[:,3] += mat[:,1]*(vol.shape[1] - 1)
        mat[:,1] = -mat[:,1]

    # eliminate "-0.0" (negative zero) in the matrix
    mat[mat == 0.0] = 0.0


def load_dicom_series(folder):
    """Load a series of dicom files and return a list of datasets.
    The resulting list will be sorted by InstanceNumber.
    """

    files = [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

    # create list of tuples (InstanceNumber, DataSet)
    dataset_list = []
    for f in files:
        ds = pydicom.dcmread(f)
        try:
            i = int(ds.InstanceNumber)
        except (AttributeError, ValueError):
            i = -1
        dataset_list.append( (i, ds) )

    # sort by InstanceNumber (the first element of each tuple)
    dataset_list.sort(key=lambda t: t[0])

    # get the dataset from each tuple
    series = [t[1] for t in dataset_list]

    patient_name = series[0].get("PatientName", "NA")

    return series, patient_name


def dicom_to_volume(dicom_series):
    """Convert a DICOM series into a float32 volume with orientation.
    The input should be a list of 'dataset' objects from pydicom.
    The output is a tuple (voxel_array, voxel_spacing, affine_matrix)
    """
    # Create numpy arrays for volume, pixel spacing (ps),
    # slice position (ipp or ImagePositinPatient), and
    # slice orientation (iop or ImageOrientationPatient)
    n = len(dicom_series)
    shape = (n,) + dicom_series[0].pixel_array.shape
    vol = np.empty(shape, dtype=np.float32)
    ps = np.empty((n,2), dtype=np.float64)
    ipp = np.empty((n,3), dtype=np.float64)
    iop = np.empty((n,6), dtype=np.float64)

    for i, ds in enumerate(dicom_series):
        # create a single complex-valued image from real,imag
        image = ds.pixel_array
        try:
            slope = float(ds.RescaleSlope)
        except (AttributeError, ValueError):
            slope = 1.0
        try:
            intercept = float(ds.RescaleIntercept)
        except (AttributeError, ValueError):
            intercept = 0.0
        vol[i,:,:] = image*slope + intercept
        ps[i,:] = dicom_series[i].PixelSpacing
        ipp[i,:] = dicom_series[i].ImagePositionPatient
        iop[i,:] = dicom_series[i].ImageOrientationPatient

    # create nibabel-style affine matrix and pixdim
    # (these give DICOM LPS coords, not NIFTI RAS coords)
    affine, pixdim = create_affine(ipp, iop, ps)
    return vol, pixdim, affine


def dicom_to_nifti(folder):

    # load the files to create a list of slices
    series, patient_name = load_dicom_series(folder)
    if not series:
        sys.stderr.write("Unable to read DICOM files.\n")
        return 1

    # reconstruct the images into a volume
    vol, pixdim, mat = dicom_to_volume(series)

    # convert DICOM coords to NIFTI coords (in-place)
    convert_coords(vol, mat)

    return nib.Nifti1Image(vol.T, mat), patient_name


BASE_PATH = ''

for root, dirs, files in os.walk(os.path.join(BASE_PATH, 'images/CIMAD/volume_tx_abdomen_s_c')):
    for folder in dirs:
        print(f'Processing {folder}')
        try:
            img_nib, patient_name = dicom_to_nifti(os.path.join(root, folder))
            ctd_list = dutils.load_centroids(os.path.join(BASE_PATH, 'results', 'payer_l3' ,f'{folder}/{folder}_ctd.json'))
            
            # img_iso = dutils.resample_nib(img_nib, voxel_spacing=(1, 1, 1), order=3)
            # ctd_iso = dutils.rescale_centroids(ctd_list, img_nib, (1,1,1))

            img_iso = dutils.reorient_to(img_nib, axcodes_to=('I', 'P', 'L'))
            ctd_iso = dutils.reorient_centroids_to(ctd_list, img_iso)

            im_np  = img_iso.get_fdata()

            coords = [vtb_coord[1:] for vtb_coord in ctd_iso if vtb_coord[0] == 22][0]
            l3 = im_np[int(coords[0]),:,:]

            print(l3.shape)
            print(type(l3))

            cmap = plt.cm.gray
            image = cmap(dutils.wdw_sbone(l3))

            # save the image
            plt.imsave(f'TCC_local/results/comp2comp_l3/{folder}_2.png', image)
            # break
        except Exception as e:
            print(f'FAILED for {folder} with error {e}')