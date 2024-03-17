# The dcmqi library is necessary: https://github.com/QIICR/dcmqi
# User Guide: https://qiicr.gitbook.io/dcmqi-guide/
import subprocess
import itk
import os
from tqdm import tqdm

PATH = 'Colorectal-Liver-Metastases'
OUTPUT_PATH = 'Colorectal-Liver-Metastases_NIfTI'

if not os.path.exists(OUTPUT_PATH):
    os.mkdir(OUTPUT_PATH)

if not os.path.exists(os.path.join(OUTPUT_PATH, 'CT')):
    os.mkdir(os.path.join(OUTPUT_PATH, 'CT'))

if not os.path.exists(os.path.join(OUTPUT_PATH, 'SEG')):
    os.mkdir(os.path.join(OUTPUT_PATH, 'SEG'))

for folder in tqdm(os.listdir(PATH), total=len(os.listdir(PATH))):
    if os.path.isdir(os.path.join(PATH, folder)):
        f = os.path.join(PATH, folder, os.listdir(os.path.join(PATH, folder))[0])

        for item in os.listdir(f):
            if 'Segmentation' in item:
                seg = os.path.join(f, item, os.listdir(os.path.join(f, item))[0])
            else:
                im = os.path.join(f, item)

        im_itk = itk.imread(im)
        itk.imwrite(im_itk, os.path.join(OUTPUT_PATH, 'CT', f'{folder}.nii.gz'))

        if not os.path.exists(os.path.join(OUTPUT_PATH, 'SEG', folder)):
            os.mkdir(os.path.join(OUTPUT_PATH, 'SEG', folder))

        subprocess.run(['dcmqi-1.3.1-win64/bin/segimage2itkimage.exe',
                        f'--inputDICOM {seg}',
                        f"--outputDirectory {os.path.join(OUTPUT_PATH, 'SEG', folder)}"],
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.STDOUT,
                       )
