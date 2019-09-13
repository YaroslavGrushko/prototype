# for voice recording: >>>>>>>>>>>>>>>>>>>>>>>>
import sys
from sys import byteorder
from array import array
from struct import pack

import pyaudio
import wave
# for voice recording <<<<<<<<<<<<<<<<<<<<<<<<<
# ABOUT AUDIO FILE >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
THRESHOLD = 500
CHUNK_SIZE = 1024
# mfccs parameters:
# by default
FFT_LENGTH = 8192
# FFT_LENGTH = 65536  #IN BACHLORE WORK
FORMAT = pyaudio.paInt16
RATE = 44100
# ABOUT AUDIO FILE <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
from python_speech_features import mfcc
import scipy.io.wavfile as wav


# for testing KNeighbours
# for array processing
import numpy as np
# # for graphs
# import matplotlib.pyplot as plt
# to work with .csv/txt/etc.
import pandas as pd
# Import LabelEncoder
from sklearn import preprocessing

#Import scikit-learn metrics module for accuracy calculation
from sklearn import metrics
# from sklearn.metrics.pairwise import manhattan_distances

# to save model on disk
from joblib import dump, load
# # for clustering

# Local Outlier Factor (LOF) - Neighbours:
from sklearn.neighbors import LocalOutlierFactor

# for random text:
from read_text import *

# import text_into_phrases
from text_into_phrases import *

# additional parameters from bachloar work >>>>>>
numcep = 24
lowfreq = 20
highfreq = 8000
# from bachlor work <<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# temporary directory for persons
temp_directory_for_persons = 'temp_directory_for_phrases'
# directory with big textes
PERSONS_DIRECTORY_FROM = 'real_voices_texts'
