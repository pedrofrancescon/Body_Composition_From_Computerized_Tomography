# Automated Identification of Body Composition in Adults from Computerized Tomography
Repository for the Final Papel of the Computer Engineering undergraduate course of UTFPR

## Abstract 

The computed tomography (CT) technique emerges as one of the current reference methods
for assessing a patient’s body composition (BC), which can provide important information for
various clinical applications. The proper use of the data obtained depends on local reference
values. Brazil, however, has a large gap regarding these data for its population, thus justifying
the development of a retrospective population study to establish such normative reference
values. In order to facilitate and make possible the extensive analysis of a large number of
exams, several authors in the area of computing have worked to automate the processes of
selection and diagnostic assistance using neural networks. Therefore, the goal of this work was
to develop a system to automate the analysis of computed tomography scans to enable the
study of body composition in adults. It was necessary to automate the process of selecting of
the ideal slice (3rd lumbar vertebra, L3) on the CT for the analysis of the BC and, subsequently,
mapping the different tissues (bone, muscle and fat), facilitating the analysis of a large number
of of exams. As a result, a cross-platform system was developed in Python for processing
CT files in DICOM format. The system performs the chaining of convolutional neural network
(CNN) algorithms, such as U-Net, SpatialConfiguration-Net and EfficientNet-B6, in order to
automate the processes of L3 selection and tissue segmentation. The system has a simple
and friendly interface, intended for use by health professionals, optimizing time and human and
computational efforts to perform the study.
