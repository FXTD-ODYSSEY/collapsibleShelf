# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-03-20 11:43:43'

"""

"""

import os
import sys
DIR = os.path.dirname(__file__)

try:
    import Qt
except ImportError:
    sys.path.insert(0,os.path.join(DIR,"_vendor"))
    
import shelf
reload(shelf)
from shelf import install