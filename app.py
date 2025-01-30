from flask import Flask, request, render_template, jsonify
import os
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, BatchNormalization, Dropout
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import h5py

model = Sequential([
    Conv2D(32, (3, 3), activation='relu', padding='same', 
           kernel_initializer='he_uniform', input_shape=(128, 128, 3)),
    BatchNormalization(),
    MaxPooling2D(pool_size=(2, 2)),
    
    Conv2D(64, (3, 3), activation='relu', padding='same', 
           kernel_initializer='he_uniform'),
    BatchNormalization(),
    MaxPooling2D(pool_size=(2, 2)),
    
    Conv2D(128, (3, 3), activation='relu', padding='same', 
           kernel_initializer='he_uniform'),
    BatchNormalization(),
    MaxPooling2D(pool_size=(2, 2)),
    
    Flatten(),
    Dense(256, activation='relu', kernel_initializer='he_uniform'),
    Dropout(0.5), 
    Dense(1, activation='sigmoid') 
])

opt = SGD(learning_rate=0.001, momentum=0.9)
model.compile(optimizer=opt, loss='binary_crossentropy', metrics=['accuracy'])
model.load_weights('deepfake_model3.h5')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files[]' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    files = request.files.getlist('files[]')

    if len(files) == 0 or files[0].filename == '':
        return jsonify({'message': 'No selected files.'}), 400

    results = {}

    for file in files:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        result = predict(filepath, model)
        results[file.filename] = result

    return jsonify({'results': results})

def predict(filepath, model):
    img = load_img(filepath, target_size=(128, 128))
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) 
    img_array = img_array / 255.0  

    prediction = model.predict(img_array)
    is_deepfake = prediction[0][0] < 0.5  
    confidence = prediction[0][0] * 100 

    return {
        'isDeepfake': bool(is_deepfake),
        'confidence': round(confidence, 2)
    }

if __name__ == '__main__':
    app.run(debug=True)
