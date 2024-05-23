
# moveNet documentation 1: https://www.tensorflow.org/lite/examples/pose_estimation/overview
# moveNet documentation 2: https://www.tensorflow.org/hub/tutorials/movenet


# Venv documentation: https://code.visualstudio.com/docs/python/environments
# ./venv/Scripts/activate
# pip install pandas
# pip install imageio
# pip install opencv-python
# pip install git+https://github.com/tensorflow/docs
# pip install tensorflow
# pip install tensforflow_hub
# pip install ipython
# pip install matplotlib
# pip install imageio[ffmpeg]

# pip freeze > requirements.txt



import sys
import warnings
import pandas as pd
import tensorflow as tf
import tensorflow_hub as hub
from tensorflow_docs.vis import embed
import numpy as np
import cv2


# Import matplotlib libraries
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
import matplotlib.patches as patches


# Some modules to display an animation using imageio.
import imageio
from IPython.display import HTML, display


# Absolute path
# path_to_csv = r'C:\Users\gm82\OneDrive - ITConcepts Professional GmbH\Visual_Studio_Code\MoveNet\Data\iris.csv'
# path_to_csv = r'C:\Users\gmei\OneDrive - ITConcepts Professional GmbH\Visual_Studio_Code\MoveNet\Data\iris.csv'


# Relative path
path_to_csv = r'.\Data\iris.csv'


df = pd.read_csv(path_to_csv, delimiter=';')
print(df[0:3])