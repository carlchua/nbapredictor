from webscraper import *
import sys
import functools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
import shutil


#team2 is the home team!

parent_dir = os.getcwd()

#Training Data
training_path = os.path.join(parent_dir, "training_data")
training_files = glob.glob(training_path + "/*.csv")
data = []
for file in training_files:
    df = pd.read_csv(file, usecols = [i for i in range(1, 42)])
    data.append(df)
training_data = pd.concat(data, axis=0, ignore_index=True)


#Validation Data
validation_path = os.path.join(parent_dir, "validation_data")
validation_files = glob.glob(validation_path + "/*.csv")
data = []
for file in validation_files:
    df = pd.read_csv(file, usecols = [i for i in range(1, 42)])
    data.append(df)
validation_data = pd.concat(data, axis=0, ignore_index=True)

#Split features and labels
training_features = training_data.copy()
training_labels = training_features.pop('net')

validation_features = validation_data.copy()
validation_labels = validation_features.pop('net')
