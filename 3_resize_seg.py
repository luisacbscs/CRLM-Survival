import os
import itk
from tqdm import tqdm

# Path to the patient folders which contain the different segmentations
SEG_PATH = 'Colorectal-Liver-Metastases_NIfTI\\SEG\\'
# Path to the CT images
CT_PATH = 'Colorectal-Liver-Metastases_NIfTI\\CT\\'

IDs = [ct.replace('.nii.gz', '') for ct in sorted(os.listdir(CT_PATH))]

for id in tqdm(IDs):
    seg = os.path.join(SEG_PATH, id, '1.nrrd')
    ct = os.path.join(CT_PATH, f'{id}.nii.gz')

    output_filename = '1_resized.nrrd'

    input_image = itk.imread(seg)
    ref_image = itk.imread(ct)

    ref_size = itk.size(ref_image)
    ref_spacing = itk.spacing(ref_image)
    ref_origin = itk.origin(ref_image)
    Dimension = ref_image.GetImageDimension()

    output_size = ref_size
    output_spacing = ref_spacing
    output_origin = ref_origin

    interpolator = itk.NearestNeighborInterpolateImageFunction.New(input_image)

    resampled = itk.resample_image_filter(
        input_image,
        #transform=scale_transform,
        interpolator=interpolator,
        size=output_size,
        output_spacing=output_spacing,
        output_origin=output_origin,
    )

    itk.imwrite(resampled, os.path.join(SEG_PATH, id,output_filename))
