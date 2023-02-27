
import subprocess
import os
import sys
from glob import glob

BASE_PATH = '/home/pedrofrancescon/Desktop/TCC/container'
BIN_PATH = os.path.join(BASE_PATH, 'bin')

os.environ['PYTHONPATH'] = os.path.join(BASE_PATH, 'MedicalDataAugmentationTool')

def main():
    base_image_folder = os.path.join(BASE_PATH, 'data')
    base_output_folder = os.path.join(base_image_folder, 'results')
    base_intermediate_folder = os.path.join(base_image_folder, 'tmp')
    models_folder = os.path.join(BASE_PATH, 'models')

    pipeline = sys.argv[1:] if len(sys.argv) > 1 else ['all']
    print('Using pipeline: ', pipeline)

    all_image_folders = [os.path.split(path)[-1] for path in glob(os.path.join(base_image_folder, '*')) if os.path.isdir(path) and path != base_output_folder]
    for current_image_folder in sorted(all_image_folders):
        print('Processing folder ', current_image_folder)

        if current_image_folder == 'tmp' or current_image_folder == 'results':
            continue
    
        image_folder = os.path.join(base_image_folder, current_image_folder)
        output_folder = os.path.join(base_output_folder, current_image_folder)
        intermediate_folder = os.path.join(base_intermediate_folder, current_image_folder)
        
        preprocessed_image_folder = os.path.join(intermediate_folder, 'data_preprocessed')
        spine_localization_folder = os.path.join(intermediate_folder, 'spine_localization')
        spine_localization_model = os.path.join(models_folder, 'spine_localization')
        vertebrae_localization_folder = os.path.join(intermediate_folder, 'vertebrae_localization')
        vertebrae_localization_model = os.path.join(models_folder, 'vertebrae_localization')
        vertebrae_segmentation_folder = os.path.join(intermediate_folder, 'vertebrae_segmentation')

        if 'preprocessing' in pipeline or 'all' in pipeline:
            subprocess.run(['python', os.path.join(BIN_PATH, 'preprocess.py'),
                            '--image_folder', image_folder,
                            '--output_folder', preprocessed_image_folder,
                            '--sigma', '0.75'])
        if 'spine_localization' in pipeline or 'all' in pipeline:
            subprocess.run(['python', os.path.join(BIN_PATH, 'main_spine_localization.py'),
                            '--image_folder', preprocessed_image_folder,
                            '--setup_folder', intermediate_folder,
                            '--model_files', spine_localization_model,
                            '--output_folder', spine_localization_folder])
        if 'vertebrae_localization' in pipeline or 'all' in pipeline:
            subprocess.run(['python', os.path.join(BIN_PATH, 'main_vertebrae_localization.py'),
                            '--image_folder', preprocessed_image_folder,
                            '--setup_folder', intermediate_folder,
                            '--model_files', vertebrae_localization_model,
                            '--output_folder', vertebrae_localization_folder])
        if 'postprocessing' in pipeline or 'all' in pipeline:
            subprocess.run(['python', os.path.join(BIN_PATH, 'cp_landmark_files.py'),
                            '--landmark_folder', vertebrae_localization_folder,
                            '--output_folder', output_folder])
            subprocess.run(['python', os.path.join(BIN_PATH, 'reorient_prediction_to_reference.py'),
                            '--image_folder', vertebrae_segmentation_folder,
                            '--reference_folder', image_folder,
                            '--output_folder', output_folder])


if __name__ == '__main__':
    main()
