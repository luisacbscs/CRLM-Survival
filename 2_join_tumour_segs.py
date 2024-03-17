import os
import itk
import numpy as np
from tqdm import tqdm

# Path to the patient folders which contain the different segmentations
PATH = 'Colorectal-Liver-Metastases_NIfTI\\SEG\\'

for patient in tqdm(sorted(os.listdir(PATH)), total=len(os.listdir(PATH))):
    segs = [seg for seg in os.listdir(os.path.join(PATH, patient)) if '.nrrd' in seg]
    segs.remove('1.nrrd')
    segs.remove('2.nrrd')
    segs.remove('3.nrrd')
    segs.remove('4.nrrd')
    for i, seg in enumerate(segs):
        arr = np.asarray(itk.imread(os.path.join(PATH, patient, seg)))
        if i == 0:
            meta = dict(itk.imread(os.path.join(PATH, patient, seg)))
            total = np.zeros(shape=arr.shape)
        total[arr >= 1] = 1

    itk_seg = itk.image_from_array(total)
    for k, v in meta.items():
        itk_seg[k] = v
    itk.imwrite(itk_seg, os.path.join(PATH, patient, '5_total.nrrd'))
