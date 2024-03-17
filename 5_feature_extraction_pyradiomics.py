import radiomics
from radiomics import featureextractor
import six
from tqdm import tqdm
import os

# Path to the patient folders which contain the different segmentations
SEG_PATH = 'Colorectal-Liver-Metastases_NIfTI\\SEG\\'
# Path to the CT images
CT_PATH = 'Colorectal-Liver-Metastases_NIfTI\\CT\\'

IDs = [ct.replace('.nii.gz', '') for ct in sorted(os.listdir(CT_PATH))]

for id in tqdm(IDs):
    maskPath = os.path.join(SEG_PATH, id, '1_resized.nrrd')
    imagePath = os.path.join(CT_PATH, f'{id}.nii.gz')

    outputFile = os.path.join(SEG_PATH, id, '1_resized_pyradiomics.csv')
    open(outputFile, 'w').close()

    feats = ['Patient-ID']
    vals = [id]

    try:
        settings = {}
        settings['binWidth'] = 25
        extractor = featureextractor.RadiomicsFeatureExtractor(**settings)
        #extractor = featureextractor.RadiomicsFeatureExtractor()
        extractor.disableAllFeatures()
        extractor.enableFeatureClassByName('firstorder')
        extractor.enableFeatureClassByName('shape')

        result_radiomics = extractor.execute(imagePath, maskPath)

        for key, val in six.iteritems(result_radiomics):
            if 'diagnostics' not in key:
                feats.append(key)
                vals.append(val)

        open(outputFile, 'w').close()

        with open(outputFile, 'a+') as f:
            for i, feat in enumerate(feats):
                if i < len(feats) - 1:
                    f.write(f'{feat},')
                elif i == len(feats) - 1:
                    f.write(f'{feat}\n')

            for i, val in enumerate(vals):
                if i < len(vals) - 1:
                    f.write(f'{val},')
                elif i == len(feats) - 1:
                    f.write(f'{val}\n')
    except ValueError:
        print(imagePath, maskPath)
