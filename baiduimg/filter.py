#!/usr/bin/env python

import os
import shutil
from PIL import Image

BASEDIR = "/tmp/img"
files = os.listdir(BASEDIR)
for f in files:
    filename = os.path.join(BASEDIR, f)
    img = Image.open(filename)
    if img.size[0] != 220:
        shutil.move(filename, "/tmp/img2")

    
