import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array  # type: ignore
from keras.models import load_model  # type: ignore # or any other framework you use

def load_model():
    model = load_model('deepfake_model3.h5')
    return model

def preprocess_image(path, target_size=(128, 128), color_mode='rgb'):
    img = load_img(path, color_mode = color_mode, target_size=target_size)
    img_array = img_to_array(img)
    img_array = img_array/255.0
    return img_array



def predict(image_path, model):
    processed_image = preprocess_image(image_path)
    prediction = model.predict(processed_image)
    
    if prediction[0] == 0:  
        return 'Deepfake'
    else:
        return 'Real'
