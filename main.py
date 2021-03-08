from code2img import code2img
import preprocess # beautify
import codeextractor # goodcode, badcode
from codeextractor import goodcode, badcode

from pathlib import Path
import argparse
import os
import parmap

argparser = argparse.ArgumentParser(description='Create dataset for Visual Vulnerability Detection')
argparser.add_argument('--base', help='base directory of project(containing source code')
argparser.add_argument('--out', help='output directory to store dataset, OUT/good/ and OUT/bad/ will be created')
argparser.add_argument('--exts', help='specify extensions to work on in CSV(ex: c,cpp,cxx,java)')
args = argparser.parse_args()

base_dir = os.path.realpath(args.base)
out_dir = os.path.realpath(args.out)
exts = args.exts.split(",")

# create output directories
good_dir = os.path.join(out_dir, 'good')
bad_dir = os.path.join(out_dir, 'bad')
Path(good_dir).mkdir(parents=True, exist_ok=True)
Path(bad_dir).mkdir(parents=True, exist_ok=True)

def create_dataset(file_path):
    with open(file_path, 'rb') as f:
        code = f.read().decode('utf-8')
    ext = os.path.splitext(file_path)[1][1:]
    code = preprocess.beautify(code)
    goodcodes = codeextractor.goodcode(code)
    badcodes = codeextractor.badcode(code)
    for goodcode in goodcodes:
        code2img(goodcode, ext, good_dir)
    for badcode in badcodes:
        code2img(badcode, ext, bad_dir)

    return 0

# iterate base directory for source codes
# https://stackoverflow.com/questions/49183196/python-search-files-with-multiple-extensions
source_files = []
for root, dirnames, filenames in os.walk(base_dir):
    for file in filenames:
        if os.path.splitext(file)[1][1:] in exts:
            source_files.append(os.path.join(root, file))

parmap.map(create_dataset, source_files, pm_pbar=True, pm_processes=8)