from code2img import code2img
import preprocess # beautify
import codeextractor # goodcode, badcode
from codeextractor import goodcode, badcode

from pathlib import Path
import argparse
import os
import parmap

argparser = argparse.ArgumentParser(description='Create dataset for Visual Vulnerability Detection')
argparser.add_argument('--out', help='output directory to store dataset, OUT/good/ and OUT/bad/ will be created')
argparser.add_argument('--exts', help='specify extensions to work on in CSV(ex: c,cpp,cxx,java)')
args = argparser.parse_args()

out_dir = os.path.realpath(args.out)
exts = args.exts.split(",")

# create output directories
cwe119_dir = os.path.join(out_dir, 'cwe119')
cwe399_dir = os.path.join(out_dir, 'cwe399')
safe_dir = os.path.join(out_dir, 'safe')

Path(cwe119_dir).mkdir(parents=True, exist_ok=True)
Path(cwe399_dir).mkdir(parents=True, exist_ok=True)
Path(safe_dir).mkdir(parents=True, exist_ok=True)

def create_cwe119(code_gadget):
    create_dataset(code_gadget, 119)

def create_cwe399(code_gadget):
    create_dataset(code_gadget, 399)

def create_dataset(code_gadget, mode):
    lines = code_gadget.split("\n")
    code = '\n'.join(lines[1:-2])
    goodorbad = lines[-2]
    
    if goodorbad == '0':
        code2img(code, safe_dir)
    elif goodorbad == '1':
        if mode == 119:
            code2img(code, cwe119_dir)
        elif mode == 399:
            code2img(code, cwe399_dir)
    return 0

with open("cwe119_cgd.txt", "rb") as f:
    cwe119_dataset = f.read().decode("utf-8").split("---------------------------------")
with open("cwe399_cgd.txt", "rb") as f:
    cwe399_dataset = f.read().decode("utf-8").split("---------------------------------")

#create_cwe119(cwe119_dataset[0])

print("Processing CWE-119")
parmap.map(create_cwe119, cwe119_dataset, pm_pbar=True, pm_processes=8)
print("Processing CWE-399")
parmap.map(create_cwe399, cwe399_dataset, pm_pbar=True, pm_processes=8)