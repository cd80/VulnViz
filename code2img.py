import hashlib
from pathlib import Path
import os
from PIL import Image, ImageDraw
from matplotlib.pyplot import imshow
import numpy as np
def code2img(code, ext, output_dir):
    # print(code, ext, output_dir)
    # return: output filename
    code = bytes(code, 'utf-8')
    code_hash = hashlib.sha256(code).hexdigest()
    out_file = os.path.join(output_dir, code_hash+'.png')
    if os.path.isfile(out_file):
        # already created
        if Path(out_file).stat().st_size != 0:
            return out_file

    image = Image.new(mode='L', size=(600, 600), color='black')
    d = ImageDraw.Draw(image)
    d.text((0, 0), code, fill=255)
    image.save(out_file)
    """
    code = bytes(code, 'utf-8')
    code_hash = hashlib.sha256(code).hexdigest()
    out_file = os.path.join(output_dir, code_hash+'.png')
    if os.path.isfile(out_file):
        # already created
        if Path(out_file).stat().st_size != 0:
            return out_file
    child = subprocess.Popen(['/root/go/bin/code2img', '-t', 'algol', '-ext', ext, '-o', out_file], stdin=subprocess.PIPE)
    child.communicate(code)
    return out_file
    """