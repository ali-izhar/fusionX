import base64

from PIL import Image
from io import BytesIO
import numpy as np
from basicsr.archs.rrdbnet_arch import RRDBNet
from realesrgan import RealESRGANer
from utils.nst_utils import is_base64, convert_to_base64

'''
    in: b64 image
    out: enhanced b64 image
'''
def enhance_image(b64_string):
    # remove header
    if not is_base64(b64_string):
        print("not b64, attempting to convert from URL...")
        try:
            b64_string = convert_to_base64(b64_string)
        except Exception as e:
            print("failed to convert")

    # b64 to image
    b64_string = b64_string.split(',')[1]
    img_data = base64.b64decode(b64_string)
    image = Image.open(BytesIO(img_data))

    model_path = 'RealESRGAN_x4plus.pth'

    print('init model')
    model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)

    print('init upsampler')
    upsampler = RealESRGANer(scale=4, model_path=model_path, model=model, tile=0, tile_pad=10, pre_pad=0,
                                 half=False)


    # to np array for enhancement
    image_np = np.array(image)

    print('upsampling...')
    # returns np array
    output, _ = upsampler.enhance(image_np, outscale=4)
    print('done upsample')

    # nparr to image
    result_image = Image.fromarray(output)

    # image to b64
    buffer = BytesIO()
    result_image.save(buffer, format="PNG")
    result_image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return result_image_base64
