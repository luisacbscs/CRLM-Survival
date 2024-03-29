# Colorectal Liver Metastases dataset: an exploratory survival analysis

Dataset available at: https://www.cancerimagingarchive.net/collection/colorectal-liver-metastases/  [1]

[1] A.L. Simpson et al. “Preoperative CT and survival data for patients undergoing resection of colorectal liver metastases”. _Scientific Data_, vol. 11, 172 (2024). DOI: 10.1038/s41597-024-02981-2.

## Preprocessing Steps

- `1_dataset_to_NIfTI.py`:

After downloading the dataset, this script converts the CT images and masks from DICOM to the NIfTI and NRRD format, respectively. To convert the masks from DICOM to NRRD the dcmqi (DICOM for Quantitative
Imaging) library is necessary.

- `2_join_tumour_segs.py`:

This script is used to join all the masks containing the segmentation of each present mestastasis in the liver in a single mask.

- `3_resize_seg.py`:

As the available masks are not the same size as the corresponding CT images, a resampling must be done, as to later procceed to feature extraction.

## Feature Extraction

- `4_extract_seg_features.py`:

This script is used to extract a few simple and explainable features from the available masks: the liver's volume in cubic centimeters, `liver_vol`, the remnant liver's volume in cubic centimeters, 
`remnant_vol`, the liver's total tumour volume in cubic centimeters, `liver_TTV`, and the number of metastases in the liver.

- `5_feature_extraction_pyradiomics.py`:

Extracting first order statistics and shape-based features from the liver's segmentation through the PyRadiomics library.

## Exploratory Survival Analysis

The library `scikit-survival` provides not only the implementation of different modules for survival prediction and performance evaluation, but very informative tutorials that aid the understanding of the
basis behind survival analysis and the way the different methods are implemented: https://scikit-survival.readthedocs.io/en/stable/user_guide/index.html

- `CRLM-Survival.ipynb`:

This notebook (W.I.P.) contains the preprocessing of the available tabular clinical data, as well as preliminary results for hazard-based survival analysis of the CRLM dataset. The fusion of the tabular
clinical data and the features extracted from the CT images is explored.

