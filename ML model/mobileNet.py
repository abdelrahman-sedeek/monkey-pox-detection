%pip install split-folders
import splitfolders
TRAINMonkeypox_DIR = r'/content/drive/MyDrive/MonkeypoxTrain'
splitfolders.ratio(TRAINMonkeypox_DIR, output="MonkeyOutput", seed=1337, ratio=(.7, .3), group_prefix=None)
TRAINOthers_DIR = r'/content/drive/MyDrive/OthersTrain'
splitfolders.ratio(TRAINOthers_DIR, output="othersOutput", seed=1337, ratio=(.7, .3), group_prefix=None)
from tensorflow.python.ops.gen_math_ops import Max
from keras.applications.mobilenet_v2 import MobileNetV2
from google.colab import drive
drive.mount('/content/drive')
import os
import cv2
import numpy as np 
import pandas as pd
import tensorflow as tf
from tqdm import tqdm
from random import shuffle, random
from sklearn.model_selection import train_test_split
from keras.applications.resnet_v2 import ResNet50V2
import keras
from sklearn.metrics import accuracy_score
from keras.callbacks import ModelCheckpoint
import splitfolders
!pip install split-folders

MODEL_NAME = 'Monkeypox'
TrainMonkeypoxPath=r'/content/MonkeyOutput/train/Monkeypox_augmented'
TestMonkeypoxPath=r'/content/MonkeyOutput/val/Monkeypox_augmented'
TrainOthersPath=r'/content/othersOutput/train/Others_augmented'
TestOthersPath=r'/content/othersOutput/val/Others_augmented'
IMG_SIZE = 50
LR = 0.001

def create_label(image_name):
    """ Create an one-hot encoded vector from image name """
    word_label = image_name[0]
    if word_label == "M":
        return np.array([1,0])
    elif word_label == "N":
        return np.array([0,1])

def create_train_Monkeypox():
  Monkeypox_training_data = []
  for img in tqdm(os.listdir(TrainMonkeypoxPath)):
      path = os.path.join(TrainMonkeypoxPath, img)
      img_data = cv2.imread(path,0)
      img_data = cv2.resize(img_data, (IMG_SIZE, IMG_SIZE))
      Monkeypox_training_data.append([np.array(img_data,dtype=object), create_label(img)])
  shuffle(Monkeypox_training_data)
  np.save('Monkeypox_data.npy',Monkeypox_training_data)
  return Monkeypox_training_data

def create_test_Monkeypox():
  Monkeypox_testing_data = []
  for img in tqdm(os.listdir(TestMonkeypoxPath)):
      path = os.path.join(TestMonkeypoxPath, img)
      img_data = cv2.imread(path,0)
      img_data = cv2.resize(img_data, (IMG_SIZE, IMG_SIZE))
      Monkeypox_testing_data.append([np.array(img_data,dtype=object), create_label(img)])
  shuffle(Monkeypox_testing_data)
  np.save('Monkeypox_data.npy',Monkeypox_testing_data)
  return Monkeypox_testing_data

def create_train_Others():
  Others_training_data = []
  for img in tqdm(os.listdir(TrainOthersPath)):
      path = os.path.join(TrainOthersPath, img)
      img_data = cv2.imread(path,0)
      img_data = cv2.resize(img_data, (IMG_SIZE, IMG_SIZE))
      Others_training_data.append([np.array(img_data,dtype=object), create_label(img)])
  shuffle(Others_training_data)
  np.save('Others_data.npy',Others_training_data)
  return Others_training_data
#print(create_data_Others())
#print("create  data for monkeypox",create_data_Monkeypox())

def create_test_Others():
  Others_testing_data = []
  for img in tqdm(os.listdir(TestOthersPath)):
      path = os.path.join(TestOthersPath, img)
      img_data = cv2.imread(path,0)
      img_data = cv2.resize(img_data, (IMG_SIZE, IMG_SIZE))
      Others_testing_data.append([np.array(img_data,dtype=object), create_label(img)])
  shuffle(Others_testing_data)
  np.save('Others_data.npy',Others_testing_data)
  return Others_testing_data

############## Merge Train Data ###################
MonkeypoxTrainingData=create_train_Monkeypox()
OthersTrainingData=create_train_Others()
#print(Monkeypoxdata)
MergedTrainData=MonkeypoxTrainingData+OthersTrainingData
#print(MergedData)
shuffle(MergedTrainData)
#print(len(MergedData))

############## Merge Test Data #################
MonkeypoxTestingData=create_test_Monkeypox()
OthersTestingData=create_test_Others()
MergedTestData=MonkeypoxTestingData+OthersTestingData
shuffle(MergedTestData)

############## Split Train Data ###################
XTrain= np.array([i[0] for i in MergedTrainData]).reshape(-1, IMG_SIZE, IMG_SIZE, 1)
YTrain = np.array([i[1] for i in MergedTrainData])
X_train = np.asarray(XTrain).astype(np.float32)
y_train = np.asarray(YTrain).astype(np.float32)

################# Split Test Data ############
XTest = np.array([i[0] for i in MergedTestData]).reshape(-1, IMG_SIZE, IMG_SIZE, 1)
YTest = np.array([i[1] for i in MergedTestData])
X_test = np.asarray(XTest).astype(np.float32)
y_test = np.asarray(YTest).astype(np.float32)

#############MODEL CREATION###############
model=MobileNetV2(input_shape=(50,50,1),include_top=True,weights=None,pooling='avg',classes=2,classifier_activation="softmax")
opt = keras.optimizers.Adam(learning_rate=0.001)
model.compile(loss='categorical_crossentropy', optimizer=opt)
##############TRAIN################
checkPoint=ModelCheckpoint('mobileNetV2.h5',save_weights_only=True)
model.fit(x=X_train,y=y_train,epochs=2000,callbacks=[checkPoint])
model.save('mobileNetV2.h5')

t=[]
for i in range(len(y_test)):
  if y_test[i][0]==1:
    t.append(0)
  else:
    t.append(1)
########Test############
predictions=[]
for img in X_test:
  predictionList=[]
  test_img = img.reshape(IMG_SIZE, IMG_SIZE, 1)
  im = np.asarray(test_img)
  im = np.expand_dims(im, axis=0)
  prediction = model.predict(im)[0]
  print(f"MonkeyPox: {prediction[0]}, NonMonkeyPox: {prediction[1]}")
  if prediction[0]>prediction[1]:
    predictions.append(0)
  else:
    predictions.append(1)
print("ACCURACY:--------------------------")
print(accuracy_score(t, predictions, normalize=True))
print("---------------------------------------")