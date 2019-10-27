from __future__ import print_function
import sys
import os
import fitz
import PyPDF2
import re
from pylovepdf.tools.compress import Compress
import glob

import subprocess

def compress_toll_docs:
    for root, dirs, files in os.walk("/Users/Leah/Google Drive (leah@cavaliercps.com)/VDOT/Norfolk 64/Test Folder/"):
        for file in files:
            if file.endswith(".pdf"):
                filename = os.path.join(root, file)
                print (filename)
                print (file)
                arg1= '-sOutputFile=' + '/Users/Leah/Google Drive (leah@cavaliercps.com)/VDOT/Norfolk 64/Test Folder/' + 'compress' + file  #added a c to the filename
                p = subprocess.Popen(['/usr/local/Cellar/ghostscript/9.27_1/bin/gs',
                                    '-sDEVICE=pdfwrite',
                                    '-dCompatibilityLevel=1.4',
                                    '-dPDFSETTINGS=/ebook', '-dNOPAUSE',
                                    '-dBATCH', '-dQUIET', str(arg1), filename],
                                    stdout=subprocess.PIPE)
                print (p.communicate())
