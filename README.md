# Talent-Squad-2

The following project was created with the aim to predict and classify images related to sports for the Talent Squad 2 Hackathon. The two main goals in the project were to predict the images and to implement the data augmentation techinques. As a matter of fact, the images were of a wide range of diversity and that could difficult our prediction capabilities. First off, It is important to not to belittle the fact that in real case scenarios we would be compelled to outsource our data to increase our training dataset. Having said that, the other option is to implement Data Augmentation techinques as mentioned earlier, which per se, works pretty well when our data is limited. 

## First steps on how the project was made

The provided dataset came in a main folder which contained the train and test folders. The train folder contained a folder for each class, whereas the test folder contained the images from all the classes mingled altogether. The main strategy to train the model was to treat those folders as subdirectories. However, the test folder was treated as a default directory since it had no separation of classes. Notwithstanding, To solve this, with the help of the "os" library new folders were created to reorganize the structure of the data so Data Augmentation became possible. Thus, we divided the training dataset into train and validation datasets with validation dataset accounting for the 20% of the initial data. In addition to that, the dimensions of the pictures were carefully metered and ploted to see if they were of the same size. In doing so, it was evident that we could face a mismatch in the range of those dimensions. To tackle down this problem, a rescaling technique was applied which consisted in normalizing those measures by dividing by 255. It was done this way because we are mainly dealing with colourful images.

## Important note regarding the use of this notebook:

The folders in the repository are exactly in their original format and order. That being said, the code is made to be run in Google Colab, if executing the cells one by one, the code will automatically create and reallocate the files for flow_from_directory() to work. Therefore, there are cells in this notebook that will work only one time and it is crucial to execute each cell in its respective order. 

## The models 

With the aim of building a Neural Network, different architectures were tested. However, in the final notebook, only two of them were saved. Both of them are exactly indentical except for the fact that the second one uses Data Augmentation. The models were more shallow than deep, they had a structure that combined max pooling with convolutional layers up until a dropout layer to reduce overfitting and facilitate generalization, which was followed by two dense layers, being the final layer host for a softmax activation function of the 3 possible outcomes. 

Due to the aim of adding more flexibility to the model, the Adam optimizer was the best option for this task. Thereupon, with the intention of balancing computational cost and time, a callback function was adjusted to specific thresholds if the metrics reached the objectives. Thus, for the sake of finding the best architecture one must go through the trials and errors when tunning the neural network's hyperparameters. 

## Evaluation

The first model performed poorly in the validation dataset, which was not a surprise. The second one outperformed in the validation metrics the training results. In addition, a huge variation in the results amongst the predictions of the 2 models was seen. However, when predicting the test images, the second model was used due to its higher val_accuracy. 

When it comes down to visually assess the results, confusion matrices are a highly versatile option since we can clearly see what are those false negatives and false positives. As a way of ilustration, one might have thought that cricket and baseball might bring some confusion in prediction, yet that was far from the truth. In contrast, more false results were made regarding the football pictures. 

## Conclusion

All in all, one must assert that the network performed quite fair with regards to the results obtained. However, it would be interesting to bring it to a higher degree of complexity in other Computer Vision problems. 
