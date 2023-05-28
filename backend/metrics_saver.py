#!/usr/bin/env python

from .Comp2Comp.comp2comp.inference_class_base import InferenceClass
import pandas as pd
import os

class MuscleAdiposeTissueMetricsSaverAppend(InferenceClass):
    """Save metrics to a CSV file."""

    def __init__(self):
        super().__init__()

    def __call__(self, inference_pipeline, results):
        """Save metrics to a CSV file."""
        self.model_type = inference_pipeline.muscle_adipose_tissue_model_type
        self.model_name = inference_pipeline.muscle_adipose_tissue_model_name
        self.output_dir = inference_pipeline.output_dir
        self.dicom_file_paths = inference_pipeline.dicom_file_paths
        self.dicom_file_names = inference_pipeline.dicom_file_names
        self.save_results(results)
        return {}

    def save_results(self, results):
        """Save results to a CSV file."""
        
        csv_file_path = os.path.join(self.output_dir, "metrics.csv")
        
        categories = self.model_type.categories
        cats = list(categories.keys())
        
        df = pd.DataFrame(
            columns=[
                "Patient ID",
                "Muscle HU",
                "Muscle CSA (cm^2)",
                "IMAT HU",
                "IMAT CSA (cm^2)",
                "SAT HU",
                "SAT CSA (cm^2)",
                "VAT HU",
                "VAT CSA (cm^2)",
            ]
        )

        for i, result in enumerate(results):
            row = []
            row.append(self.dicom_file_names[i])
            for cat in cats:
                row.append(result[cat]["Hounsfield Unit"])
                row.append(result[cat]["Cross-sectional Area (cm^2)"])
            df.loc[i] = row
        
        try:
            saved_df = pd.read_csv(csv_file_path)
            df = pd.concat([df, saved_df])
        except:
            pass
        finally:
            df.to_csv(csv_file_path, index=False)