
import os
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import numpy as np
import tensorflow as tf

ASSET_FOLDER = 'static/assets/'

app = Flask(__name__)
app.config['ASSET_FOLDER'] = ASSET_FOLDER


bg_video = os.path.join(app.config['ASSET_FOLDER'], 'pexels-tima-miroshnichenko-6010766.mp4')
    
@app.route('/')
def upload_form():
    return render_template('index.html', type="" , bgvideo=bg_video)

@app.route('/', methods=['POST'])
def upload_image():
    file = request.files['file']
    print(file.filename)
    file.save(os.path.join("static/uploads", secure_filename(file.filename)))

    imvar = tf.keras.preprocessing.image.load_img(os.path.join("static/uploads", secure_filename(file.filename))).resize((176, 176))
    imarr = tf.keras.preprocessing.image.img_to_array(imvar)
    imarr = np.array([imarr])
    model = tf.keras.models.load_model("model")
    impred = model.predict(imarr)

    def roundoff(arr):
        """To round off according to the argmax of each predicted label array. """
        arr[np.argwhere(arr != arr.max())] = 0
        arr[np.argwhere(arr == arr.max())] = 1
        return arr

    for classpreds in impred:
        impred = roundoff(classpreds)
    
    classcount = 1
    for count in range(4):
        if impred[count] == 1.0:
            break
        else:
            classcount+=1
    
    classdict = {1: "Mild Dementia", 2: "Moderate Dementia", 3: "No Dementia, Patient is Safe", 4: "Very Mild Dementia"}
    print(classdict[classcount])
    result=classdict[classcount]

    c = 'xyz'
    return render_template('index.html', type="Patient is suffering from "+ result, bgvideo=bg_video)

if __name__ == "__main__":
    app.run()
 
