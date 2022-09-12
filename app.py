# -*- coding: utf-8 -*-
"""code.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1H_mEicykIf1bhyhQtAW04rx3eYZfY6dS

#####Talent Squad - Data Science II
"""

# Commented out IPython magic to ensure Python compatibility.
import os
import cv2
import shutil
import random
import matplotlib.image as mpimg
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 
import seaborn as sns
import tensorflow as tf
import sklearn.metrics as metrics
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing.image import img_to_array, load_img
# %matplotlib inline

import warnings
warnings.filterwarnings("ignore")

from google.colab import drive
from google.colab import files

drive.mount("/content/drive")

sns.set_style("darkgrid")

!ls "/content/drive/My Drive/Talent Squad 2"

# Commented out IPython magic to ensure Python compatibility.
# %cd "/content/drive/My Drive/Talent Squad 2"

base_dir = "/content/drive/My Drive/Talent Squad 2"

print("Contents of base directory:")
print(os.listdir(base_dir))

print("\nContents of train directory:")
print(os.listdir(f"{base_dir}/Imágenes-data-science-ii/train"))

print("\nContents of test directory:")
print(os.listdir(f"{base_dir}/Imágenes-data-science-ii/test"))

"""Since we will work with flow_from_directory(), we will have to create a new folder to put the test images into it. The reason to do so, is that flow_from_directory iterates over the inner folders and treats them as subdirectories belonging to a specific class. Nevertheless, our test folder has no labels. Therefore, our primary goal is to predict to which class does the images belong. So, in order to accomplish this task, let's put the test folder into a new folder that we will call "data_test"."""

folder = "data_test" 
os.makedirs(base_dir + "/Imágenes-data-science-ii/" + folder)
src_path = base_dir + "/Imágenes-data-science-ii/test"
dst_path = base_dir + "/Imágenes-data-science-ii/" + folder
shutil.move(src_path, dst_path)

train_dir = base_dir + "/Imágenes-data-science-ii/train"
test_dir =  base_dir + "/Imágenes-data-science-ii/data_test"

train_baseball_dir = os.path.join(train_dir, "baseball")
train_cricket_dir = os.path.join(train_dir, "cricket")
train_football_dir = os.path.join(train_dir, "football")

train_baseball_fnames = os.listdir(train_baseball_dir)
train_cricket_fnames = os.listdir(train_cricket_dir)
train_football_fnames = os.listdir(train_football_dir)

print("Baseball picture names -> ",  train_baseball_fnames[:10], "\n")
print("Cricket picture names-> ", train_cricket_fnames[:10], "\n")
print("Football picture names -> ", train_football_fnames[:10], "\n")

# Total number of each category in the training directory 

print("Total training baseball images:", len(os.listdir(train_baseball_dir)))
print("Total training cricket images:", len(os.listdir(train_cricket_dir)))
print("Total training football images:", len(os.listdir(train_football_dir)))

"""We can appreciate that the data is slightly unbalnced. We have a small quantity of images to work with if we want to divide the data into train and validation datasets. Yet, we will try to work with both models with and without data augmentation to make the comparison."""

train_length = len(os.listdir(train_baseball_dir)) + len(os.listdir(train_cricket_dir)) + len(os.listdir(train_football_dir))
train_length

print("Sample baseball image:")
plt.imshow(load_img(f"{os.path.join(train_baseball_dir, os.listdir(train_baseball_dir)[0])}"))
plt.grid(False)
plt.show()

print("Sample cricket image:")
plt.imshow(load_img(f"{os.path.join(train_cricket_dir, os.listdir(train_cricket_dir)[0])}"))
plt.grid(False)
plt.show()

print("Sample football image:")
plt.imshow(load_img(f"{os.path.join(train_football_dir, os.listdir(train_football_dir)[0])}"))
plt.grid(False)
plt.show()

"""Notice how the images are of different shape, which means, we cannot feed the model with a specific shape, instead, we should resize all the images. """

sample_image  = load_img(f"{os.path.join(train_baseball_dir, os.listdir(train_baseball_dir)[0])}")
sample_array = img_to_array(sample_image)

print(f"Each image has shape: {sample_array.shape}")

"""Handling the different size of the images is a critical step since our CNN won't be able to process the images properly without this step. As a matter of fact, we have different options to tackle down this problem: resizing, cropping or rescaling. To handle this properly, we will directly rescale dividing by the scalar number of 255, which is the optimum number when dealing with color images. Thus, this process will resize the images and make them all the same size. On the other hand, there is one more thing we should consider, and that is to divide the training folder into train/validation. One of our major hindrances to build a reliable model is the lack of a wide range of different images belonging to each class. Having said that, we expect to have a valdiation set of 20% max out of the original length of images. In real practice, having 43 images out of 211 belonging to 3 classes would not be an efficient split. However, since we don't have the original labels of the test dataset, we must be sure that our model performs well at least with this split on the validation dataset. Besides, images are quite diverse, and the data augmentation process will add noise to the dataset which will make our accuracy increase due to a higher flexibility in the model.

##### Train/Validation Split

In the upcoming step we will rearrange our data to our new folders "traintrain" and "trainval" which are the names derived from the original folder where our data lies (the train folder). Thus, we will create these folders and create a separate subdirectory for each class within these fodlers.
"""

classes_dir = ["baseball", "cricket", "football"] 

val_ratio = 0.2
train_length_2 = 0
val_length = 0

for cls in classes_dir:
    os.makedirs(train_dir + "train/" + cls)
    os.makedirs(train_dir + "val/" + cls)
    src = train_dir + "/" + cls 

    allFileNames = os.listdir(src)
    np.random.shuffle(allFileNames)
    train_FileNames, val_FileNames = np.split(np.array(allFileNames), [int(len(allFileNames) * (1 - val_ratio))])
    train_FileNames = [src + "/" + name for name in train_FileNames.tolist()]
    val_FileNames = [src + "/" + name for name in val_FileNames.tolist()]

    print(f"Total number of images belonging to the class {cls}: ", len(allFileNames))
    print(f"Total number of training images belonging to the class {cls}: ", len(train_FileNames))
    print(f"Total number of validation images belonging to the class {cls}: ", len(val_FileNames), "\n")
    
    for name in train_FileNames:
        shutil.copy(name, train_dir + "train/" + cls)

    for name in val_FileNames:
        shutil.copy(name, train_dir + "val/" + cls)
    
    train_length_2 += len(train_FileNames)
    val_length += len(val_FileNames)

"""We can see that overall, the train/validation split is well balanced. Furthermore, we will save the length of the train and validation sets to properly specify the number of steps per epoch."""

print(f"The total number of train and validation examples are {train_length_2} and {val_length} respectively.")

"""Now let's set our new directories and jump to our first trial without data augmentation"""

train_dir_2 = base_dir + "/Imágenes-data-science-ii/traintrain"
val_dir = base_dir + "/Imágenes-data-science-ii/trainval"

"""##### The model without data augmentation

We choose not to use a very profound model since our goal is to generalize well enough. Furthermore, building a deeper model will increase the risk of exploding gradients. We also added a dropout layer to handle overfitting and a dense layer of 128 neurons before using the last layer with softmax. In addition to that, we are interested in saving time and reducing the computational cost of our model. Hence, we will use the "Callback" class created in our code to stop our model once it reaches to our goal threshold of performance.
"""

epochs = 90
batch_size = 10
train_steps = int(train_length_2 / batch_size)
validation_steps = int(val_length / batch_size)

class myCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs={}):
        if(logs.get("loss")<0.4) and (logs.get("accuracy")>0.99):
            print("\nLoss is low and and accuracy is high so cancelling training!")
            self.model.stop_training = True

callbacks = myCallback()

model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(16, (3,3), activation="relu", input_shape=(200, 200, 3)),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(32, (3,3), activation="relu"),
    tf.keras.layers.MaxPooling2D(2,2), 
    tf.keras.layers.Flatten(), 
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(128, activation="relu"), 
    tf.keras.layers.Dense(3, activation="softmax")  
])

model.compile(optimizer="adam",
              loss="sparse_categorical_crossentropy",
              metrics = ["accuracy"])

train_datagen = ImageDataGenerator(rescale=1.0/255.)

train_generator = train_datagen.flow_from_directory(directory=train_dir_2,
                                                      color_mode="rgb",
                                                      batch_size=batch_size,
                                                      class_mode="sparse",
                                                      shuffle=False,
                                                      target_size=(200, 200))

val_datagen = ImageDataGenerator(rescale=1.0/255.)

val_generator = val_datagen.flow_from_directory(directory=val_dir,
                                                      color_mode="rgb",
                                                      batch_size=batch_size,
                                                      class_mode="sparse",
                                                      shuffle=False,
                                                      target_size=(200, 200))

test_datagen = ImageDataGenerator(rescale = 1.0/255.)

test_generator = test_datagen.flow_from_directory(
        test_dir, 
        target_size=(200, 200),
        color_mode="rgb",
        shuffle = False,
        class_mode=None,
        batch_size=batch_size)

history = model.fit(train_generator,
            steps_per_epoch=train_steps,
            epochs=epochs,
            validation_data=val_generator,
            validation_steps=validation_steps,
            callbacks=[callbacks])

model.summary()

acc = history.history["accuracy"]
val_acc = history.history["val_accuracy"]
loss = history.history["loss"]
val_loss = history.history["val_loss"]

plt.plot(acc)
plt.plot(val_acc)
plt.title("model's accuracy")
plt.ylabel("accuracy")
plt.xlabel("epoch")
plt.legend(["Accuracy", "Val_accuracy"], loc="upper left")
plt.show()

plt.plot(loss)
plt.plot(val_loss)
plt.title("model's loss")
plt.ylabel("loss")
plt.xlabel("epoch")
plt.legend(["loss", "Val_loss"], loc="upper left")
plt.show()

"""After testing with different architectures while trying to reduce the complexity of the model, it seems obvious that it works better with a more shallow model. However, we cannot ignore the fact that we are facing a clear problem of overfitting in the training dataset. Having said that, there is one thing we must do and that is to expand our dataset with data augmentation techniques. It is accurate to say that our odds of performing well without the augmentated data are significantly low, let alone expect the model to overcome the plateau of 0.5 of val_acc. Thus, the lack of data is our main drawback. Fortunately, we gona retest the model with augmented data this time to tackle down overfitting. """

probability_model = tf.keras.Sequential([model, 
                                         tf.keras.layers.Softmax()])

preds_1 = probability_model.predict(test_generator)

preds_1

predicted_classes = preds_1.argmax(axis=1)
predicted_classes

"""##### The model with data augmentation

We will provide a different set of values for the callback since it's the "val_accuracy" the main metric of interest we have to measure.
"""

class myCallback_2(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs={}):
        if(logs.get("val_loss")<0.4) and (logs.get("val_accuracy")>0.99):
            print("\nLoss is low and and val_accuracy is high so cancelling training!")
            self.model.stop_training = True

callback_2 = myCallback_2()

model_2 = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(16, (3,3), activation="relu", input_shape=(200, 200, 3)),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(32, (3,3), activation="relu"),
    tf.keras.layers.MaxPooling2D(2,2), 
    tf.keras.layers.Flatten(), 
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(128, activation="relu"), 
    tf.keras.layers.Dense(3, activation="softmax")  
])

model_2.compile(optimizer="adam",
              loss="sparse_categorical_crossentropy",
              metrics = ["accuracy"])

train_datagen_2 = ImageDataGenerator(rescale=1.0/255.,
                                     rotation_range=0.1,
                                     width_shift_range=0.1,
                                     height_shift_range=0.1,
                                     shear_range=0.1,
                                     zoom_range=0.1,
                                     horizontal_flip=False,
                                     fill_mode="nearest")

train_generator_2 = train_datagen_2.flow_from_directory(directory=train_dir,
                                                      color_mode="rgb",
                                                      batch_size=batch_size,
                                                      class_mode="sparse",
                                                      shuffle=False,
                                                      target_size=(200, 200))

val_datagen_2 = ImageDataGenerator(rescale=1.0/255.)

val_generator_2 = val_datagen_2.flow_from_directory(directory=val_dir,
                                                      color_mode="rgb",
                                                      batch_size=batch_size,
                                                      class_mode="sparse",
                                                      shuffle=False,
                                                      target_size=(200, 200))

test_datagen_2 = ImageDataGenerator(rescale = 1.0/255.)

test_generator_2 = test_datagen.flow_from_directory(
        test_dir, 
        target_size=(200, 200),
        color_mode="rgb",
        shuffle = False,
        class_mode=None,
        batch_size=batch_size)

history_2 = model_2.fit(train_generator_2,
            steps_per_epoch=train_steps,
            epochs=epochs,
            validation_data=val_generator_2,
            validation_steps=validation_steps,
            callbacks=[callback_2])

model_2.summary()

acc_2 = history_2.history["accuracy"]
val_acc_2 = history_2.history["val_accuracy"]
loss_2 = history_2.history["loss"]
val_loss_2 = history_2.history["val_loss"]

plt.plot(acc_2)
plt.plot(val_acc_2)
plt.title("model's accuracy")
plt.ylabel("accuracy")
plt.xlabel("epoch")
plt.legend(["Accuracy", "Val_accuracy"], loc="upper left")
plt.show()

plt.plot(loss_2)
plt.plot(val_loss_2)
plt.title("model's loss")
plt.ylabel("loss")
plt.xlabel("epoch")
plt.legend(["loss", "Val_loss"], loc="upper left")
plt.show()

"""Now, these are completely different results. Through each of the epoch slowly but steady, accuracy is getting higher at the pace of the val_accuracy to the top. The same behaviour is observed in loss and val_loss which is expected. We can safely assume that the model learned well on the training and augmented data. With this, we can make our predictions for the test dataset with the model_2. But before that, let's compare our results between the models and take a look at the confusion matrix. """

probability_model_2 = tf.keras.Sequential([model_2, 
                                         tf.keras.layers.Softmax()])

preds_2 = probability_model_2.predict(test_generator)

preds_2

predicted_classes_2 = preds_2.argmax(axis=1)
predicted_classes_2

"""##### Models comparison"""

ind = 0
f = 0
t = 0
for x, y in zip(predicted_classes, predicted_classes_2):
    if x == y: 
        print(str(ind) + ":", True)
        t += 1
    else:
        print(str(ind) + ":", False)
        f += 1
    ind += 1
print(f"\nThe total number of different classes between the 2 models is: {f}\nWhile the total number of equal predicted classes is: {t}")

"""We can see that there is a slight difference in predictions between the models"""

# Summarize history of model's training accuracy 
plt.plot(history.history["accuracy"])
plt.plot(history_2.history["accuracy"])
plt.title("model's accuracy")
plt.ylabel("accuracy")
plt.xlabel("epoch")
plt.legend(["model 1", "model 2"], loc="upper left")
plt.show()

# Summarize history for training loss
plt.plot(history.history["loss"])
plt.plot(history_2.history["loss"])
plt.title("model's loss")
plt.ylabel("loss")
plt.xlabel("epoch")
plt.legend(["model 1", "model 2"], loc="upper left")
plt.show()

"""The key takeaways from our plots are: model 1 quickly improves to excellence in both, accuracy and loss. However, this is a tricky obseravation. Our model 2 did not learn completely the features from the training set precisely because we did data augmentation. It takes much more for model 2 to learn and improve its metrics, however it's worth the time. """

# Summarize history of model's validation accuracy
plt.plot(history.history["val_accuracy"])
plt.plot(history_2.history["val_accuracy"])
plt.title("model's val_accuracy")
plt.ylabel("val_accuracy")
plt.xlabel("epoch")
plt.legend(["model 1", "model 2"], loc="upper left")
plt.show()

# Summarize history for validation loss
plt.plot(history.history["val_loss"])
plt.plot(history_2.history["val_loss"])
plt.title("model's val_loss")
plt.ylabel("val_loss")
plt.xlabel("epoch")
plt.legend(["model 1", "model 2"], loc="upper left")
plt.show()

"""Therefore, we can observe how our model 1 performed poorly regarding the validation set, and model 2 slowly reached the maximum val_accuracy around the 80th epoch. On the other hand, around the 30th epoch, val_loss started to fall below 0.75, where it slowly continued to descend down to minimum.

Confusion Matrices
"""

def cm_cr(test_gen, model):
    preds=model.predict(test_gen)    
    labels=test_gen.labels
    classes=list(test_gen.class_indices.keys()) 
    pred_list=[ ] 
    true_list=[]
    for i, p in enumerate(preds):
        index=np.argmax(p)
        pred_list.append(classes[index])
        true_list.append(classes[labels[i]])
    y_pred=np.array(pred_list)
    y_true=np.array(true_list)
    clr = metrics.classification_report(y_true, y_pred, target_names=classes)
    print("Classification Report:\n----------------------\n", clr)
    cm = metrics.confusion_matrix(y_true, y_pred )        
    length=len(classes)
    if length<8:
        fig_width=8
        fig_height=8
    else:
        fig_width= int(length * .5)
        fig_height= int(length * .5)
    plt.figure(figsize=(fig_width, fig_height))
    sns.heatmap(cm, annot=True, vmin=0, fmt="g", cmap="Blues", cbar=False)       
    plt.xticks(np.arange(length)+.5, classes, rotation= 90, fontsize=16)
    plt.yticks(np.arange(length)+.5, classes, rotation=0, fontsize=16)
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title("Confusion Matrix")
    plt.show()

cm_cr(val_generator, model)

cm_cr(val_generator_2, model_2)

"""We can conclude that indeed, the model_2 outperforms the capability of model_1 due to it's resilience to overfitting by the noise added with data augmentation. We can confidently rely on our second model to make predictions for the test dataset. Besides, our goal was to get the F1-Score Macro, which results in an outstanding 0.93 compared to tiny 0.40 in the first model. In conclusion, to improve our results we could get much more data to improve the flexibility of our model to learn the patterns of what type of sport it is illustrated in the image. However, in real case scenario, many times we will face the problem of having a very limited amount of data and we will have to use data augmentation to help our model to generalize well enough.

##### Results submission
"""

predicted_classes_2

labels = (train_generator.class_indices)
labels = dict((v,k) for k,v in labels.items())
preds_labels = [labels[k] for k in predicted_classes_2]

filenames=test_generator.filenames
results=pd.DataFrame({"Filename":filenames,
                      "Predictions":preds_labels,
                      "Value":predicted_classes_2})
results.to_csv("results.csv",index=False)
files.download("results.csv")

results_json = pd.read_csv("results.csv")

results_json.to_json("predictions.json")

files.download("predictions.json")