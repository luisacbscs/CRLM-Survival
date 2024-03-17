import os
import itk
import numpy as np
from tqdm import tqdm

# Path to the patient folders which contain the different segmentations
PATH = 'Colorectal-Liver-Metastases_NIfTI\\SEG\\'

FEATURE_FILE = 'Colorectal-Liver-Metastases_NIfTI\\seg_features.csv'
open(FEATURE_FILE, 'w').close()

with open(FEATURE_FILE, 'a+') as f:
    f.write('Patient-ID,liver_vol,remnant_vol,n_metastases,liver_TTV\n')

for patient in tqdm(sorted(os.listdir(PATH)), total=len(os.listdir(PATH))):
    segs = [seg for seg in os.listdir(os.path.join(PATH, patient)) if '.nrrd' in seg]

    for i, seg in enumerate(segs):
        arr = np.asarray(itk.imread(os.path.join(PATH, patient, seg)))
        meta = dict(itk.imread(os.path.join(PATH, patient, seg)))
        sp = np.asarray(meta['spacing'])
        voxel_vol = sp[0] * sp[1] * sp[2] * 0.001  # Voxel volume in cubic centimeter

        if seg == '1.nrrd':  # LIVER SEGMENTATION
            liver_vol = voxel_vol * np.count_nonzero(arr)
        elif seg == '2.nrrd':  # REMNANT LIVER SEGMENTATION
            remnant_vol = voxel_vol * np.count_nonzero(arr)
        elif seg == '5_total.nrrd':  # METASTASIS SEGMENTATION
            liver_TTV = voxel_vol * np.count_nonzero(arr)

    segs.remove('1.nrrd')
    segs.remove('2.nrrd')
    segs.remove('3.nrrd')
    segs.remove('4.nrrd')
    segs.remove('5_total.nrrd')

    n_metastasis = len(segs)

    with open(FEATURE_FILE, 'a+') as f:
        f.write(f'{patient},{liver_vol},{remnant_vol},{n_metastasis},{liver_TTV}\n')
