from flask import url_for
from tensorflow import keras
from keras.preprocessing import image as im
from tensorflow.keras.applications import imagenet_utils
from keras.applications.vgg16 import preprocess_input
import numpy as np
import pickle
import pandas as pd

inputShape = (244, 244)
image_path = "./static/images/"
preprocess = imagenet_utils.preprocess_input
image_model = keras.models.load_model("./static/ml_models/find_mushroom.h5")
classify_model = keras.models.load_model("./static/ml_models/find_species_of_mushroom.h5")
class_dictionary = pickle.load( open( "./static/csv/class_dictionary.p", "rb" ) )
df = pd.read_csv("./static/csv/mushroom_data.csv")

def identify_mushroom(image):
    image_filename = image.filename
    loaded_image = im.load_img(image_path+image_filename, target_size=inputShape)
    img = im.img_to_array(loaded_image).astype('uint8')
    img = preprocess(img)
    img = np.expand_dims(img, axis=0)
    predicted_result = image_model.predict(img)
    predict = np.asarray(predicted_result).flatten()
    if predict[0]==1:
        return True
    else:
        return False

def mushroom_species(image):
    image_filename = image.filename
    loaded_image = im.load_img(image_path+image_filename, target_size=(128,128))
    img = im.img_to_array(loaded_image).astype('uint8')
    img = preprocess(img)
    img = np.expand_dims(img, axis=0)
    predicted_result = classify_model.predict(img)
    arr = np.asarray(predicted_result).flatten()
    index = np.where(arr == np.amax(arr))
    name = class_dictionary.get(index[0][0]).split("_")
    category = name[1]+" "+name[2]
    supercategory = name[1]
    edibility = "NA"
    for sp_category, edible in zip(df["supercategory"], df["Edibility"]):
        if supercategory == sp_category:
            edibility = edible
            break
        else:
            pass
    return [category, supercategory, edibility]

