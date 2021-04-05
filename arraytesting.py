
from simple_unet_model import simple_unet_model   #Use normal unet model
from keras.utils import normalize
import os
import cv2
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
from dataloader_mhd import load_itk
from datetime import datetime
from packaging import version
import tensorflow as tf
from tensorflow import keras

def loaddataB(randomstring):
    print(randomstring)
    image_directory = 'data/left_atrium/'
    mask_directory = 'data/left_atrium/'
    image_directory2 = 'data/left_atrium2/'
    mask_directory2 = 'data/left_atrium2/'
    # Define the Keras TensorBoard callback.
    # logdir="logs/fit/" + datetime.now().strftime("%Y%m%d-%H%M%S")
    # tensorboard_callback = keras.callbacks.TensorBoard(log_dir=logdir)

    # --------------------------------------------------------------------------------------------------------change
    SIZE = 160
    image_dataset = []  #Many ways to handle data, you can use pandas. Here, we are using a list format.
    mask_dataset = []  #Place holders to define add labels. We will add 0 to all parasitized images and 1 to uninfected.

    # 3d image in 32000x320 (2d format) - single patient
    # list of this 3d image in 2d format
    # 320x320 as a single element in the list
    # so there will be two for loops, one for different patients, and one for the 100 slices for each patient

    # 2d images in 256 x 256
    # list of these 2d miages

    images = os.listdir(image_directory)
    for i, folder_name in enumerate(images):    #Remember enumerate method adds a counter and returns the enumerate object
        if folder_name == 'data_readme.txt':
            continue
        path= image_directory + folder_name
        image_name = '/image.mhd'
        if folder_name.startswith('a'):
            continue # mask_name = '/gt_binary.mhd'
        else:
            mask_name = '/gt_std.mhd'

        image1, origin1, spacing1 = load_itk(path+image_name)
        maxElement1 = np.amax(image1)
        image1= image1 * 255/maxElement1
        maxElement3 = np.amax(image1)
        print(maxElement1)
        print(maxElement3)

        print('image:' ,image1.shape) 
        mask1, origin2, spacing2 = load_itk(path+mask_name)

        shape=image1.shape

        print('mask:' ,mask1.shape)    
        
        mask1 = mask1.astype(np.uint8)
        image1 = image1.astype(np.uint8)
        mask1 = (mask1 > 0)
        # maxElement2 = np.amax(mask1)
        # mask1 * 255/maxElement2
        # print(maxElement2)
        # #print(image_directory+image_name)
        # image = cv2.imread(image_directory+image_name, 0)
        # image = Image.fromarray(image)
        # image = image.resize((SIZE, SIZE))

        for i in range(shape[0]):
            
            
            temp_image = image1[i,80:240,80:240]
            temp_mask = mask1[i,80:240,80:240]

            maxElement4 = np.amax(temp_mask)
            if maxElement4 ==0:
                continue

            image_dataset.append(np.array(temp_image))
            mask_dataset.append(np.array(temp_mask))

    return image_dataset, mask_dataset

if __name__ == '__main__':

    image_dataset, mask_dataset = loaddataB('start')    

            # print(len(mask_dataset))
    # image_dataset = np.array(image_dataset)
    # print(image_dataset.shape)
    # --------------------------------------------------------------------------------------------------------change
    # images = os.listdir(image_directory)
    # for i, image_name in enumerate(images):    #Remember enumerate method adds a counter and returns the enumerate object
    #     if (image_name.split('.')[1] == 'tif'):
    #         #print(image_directory+image_name)
    #         image = cv2.imread(image_directory+image_name, 0)
    #         image = Image.fromarray(image)
    #         image = image.resize((SIZE, SIZE))
    #         image_dataset.append(np.array(image))



    # image_dataset, origin1, spacing1 = load_itk('image.mhd')
    # maxElement1 = np.amax(image_dataset)
    # image_dataset * 255/maxElement1
    # # --------------------------------------------------------------------------------------------------------change


    # #Iterate through all images in Uninfected folder, resize to 64 x 64
    # #Then save into the same numpy array 'dataset' but with label 1

    # # --------------------------------------------------------------------------------------------------------change

    # # masks = os.listdir(mask_directory)
    # # for i, image_name in enumerate(masks):
    # #     if (image_name.split('.')[1] == 'tif'):
    # #         image = cv2.imread(mask_directory+image_name, 0)
    # #         image = Image.fromarray(image)
    # #         image = image.resize((SIZE, SIZE))
    # #         mask_dataset.append(np.array(image))


    # mask_dataset, origin2, spacing2 = load_itk('gt_binary.mhd')
    # maxElement2 = np.amax(mask_dataset)
    # mask_dataset * 255/maxElement2

    # --------------------------------------------------------------------------------------------------------change
    #Normalize images
    image_dataset = np.expand_dims(normalize(np.array(image_dataset), axis=1),3)
    #D not normalize masks, just rescale to 0 to 1.
    mask_dataset = np.expand_dims((np.array(mask_dataset)),3) /255.


    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(image_dataset, mask_dataset, test_size = 0.10, random_state = 0)

    #Sanity check, view few mages
    import random
    import numpy as np
    image_number = random.randint(0, len(X_train)-1)
    plt.figure(figsize=(12, 6))
    plt.subplot(121)

    # --------------------------------------------------------------------------------------------------------change
    plt.imshow(np.reshape(X_train[image_number], (160, 160)), cmap='gray')
    plt.subplot(122)

    # --------------------------------------------------------------------------------------------------------change
    plt.imshow(np.reshape(y_train[image_number], (160, 160)), cmap='gray')
    plt.show()
