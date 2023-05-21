
import argparse
import os
import numpy as np
import itk

def reorient_to_rai(image):
    """
    Reorient image to RAI orientation.
    :param image: Input itk image.
    :return: Input image reoriented to RAI.
    """
    filter = itk.OrientImageFilter.New(image)
    filter.UseImageDirectionOn()
    filter.SetInput(image)
    m = itk.GetMatrixFromArray(np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]], np.float64))
    filter.SetDesiredCoordinateDirection(m)
    filter.Update()
    reoriented = filter.GetOutput()
    return reoriented


def smooth(image, sigma):
    """
    Smooth image with Gaussian smoothing.
    :param image: ITK image.
    :param sigma: Sigma for smoothing.
    :return: Smoothed image.
    """
    ImageType = itk.Image[itk.SS, 3]
    filter = itk.SmoothingRecursiveGaussianImageFilter[ImageType, ImageType].New()
    filter.SetInput(image)
    filter.SetSigma(sigma)
    filter.Update()
    smoothed = filter.GetOutput()
    return smoothed


def clamp(image):
    """
    Clamp image between -1024 to 8192.
    :param image: ITK image.
    :return: Clamped image.
    """
    ImageType = itk.Image[itk.SS, 3]
    filter = itk.ClampImageFilter[ImageType, ImageType].New()
    filter.SetInput(image)
    filter.SetBounds(-1024, 8192)
    filter.Update()
    clamped = filter.GetOutput()
    return clamped

def load_nifti(file_path):
    ImageType = itk.Image[itk.SS, 3]
    reader = itk.ImageFileReader[ImageType].New()
    reader.SetFileName(file_path)
    image = reader.GetOutput()
    image.Update()
    return image

def load_dicom(folder_path):
    ImageType = itk.Image[itk.SS, 3]
    reader = itk.ImageSeriesReader[ImageType].New()
    namesGenerator = itk.GDCMSeriesFileNames.New()
    namesGenerator.SetUseSeriesDetails(True)
    namesGenerator.SetGlobalWarningDisplay(False)
    namesGenerator.SetRecursive(True)
    namesGenerator.SetDirectory(folder_path)
    seriesUID = namesGenerator.GetSeriesUIDs()
    maxSlices = 0
    for uid in seriesUID:
        filenames = namesGenerator.GetFileNames(uid)
        # TODO: implement finer more robust method for determining the best series
        if len(filenames) > maxSlices: 
            maxSlices = len(filenames)
            largest_series = filenames
    # dicomIO = itk.GDCMImageIO.New()
    # reader.SetImageIO(dicomIO)
    reader.SetFileNames(largest_series)
    # reader.ForceOrthogonalDirectionOff()
    image = reader.GetOutput()
    image.Update()
    return image

def load_from_path(path):
    if os.path.isfile(path) and path.endswith('.nii.gz'):
        image = load_nifti(path)
        return image
    elif os.path.isdir(path):
        image = load_dicom(path)
        return image
    else:
        raise Exception(f'Unable to process path "{path}"')


def preprocess(image, sigma):
    reoriented = reorient_to_rai(image)
    reoriented = smooth(reoriented, sigma)
    reoriented = clamp(reoriented)
    reoriented.SetOrigin([0, 0, 0])
    m = itk.GetMatrixFromArray(np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]], np.float64))
    reoriented.SetDirection(m)
    reoriented.Update()
    return reoriented

def preprocess_from_path(path, sigma):
    image, _ = load_from_path(path)
    preprocessed = preprocess(image, sigma)
    return preprocessed


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_folder', type=str, required=True)
    parser.add_argument('--output_folder', type=str, required=True)
    parser.add_argument('--basename', type=str, required=True)
    parser_args = parser.parse_args()
    
    if not os.path.exists(parser_args.output_folder):
        os.makedirs(parser_args.output_folder)

    image = load_from_path(parser_args.image_folder)
    preprocessed = preprocess(image, 0.75)

    filename = os.path.join(parser_args.output_folder, parser_args.basename + '.nii.gz')
    itk.imwrite(preprocessed, filename)
