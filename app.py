from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField
from wtforms.validators import DataRequired, ValidationError
from dotenv import load_dotenv
import os
import tensorflow as tf
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np
import cv2 as cv

model = tf.keras.models.load_model('output/model.h5')
model.compile(optimizer='adam', loss=tf.keras.losses.MeanSquaredError(),
              metrics=[tf.keras.metrics.RootMeanSquaredError()])

app = Flask(__name__)
load_dotenv()
app.secret_key = os.getenv('secret_key')
app.config['UPLOAD_FOLDER'] = 'static/images'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']

def validate_file(form, field):
    filename = field.data.filename
    extension = filename.split('.')[-1].lower()
    if '.' not in filename or extension not in ALLOWED_EXTENSIONS:
        raise ValidationError('Please choose an image file.')


class UploadForm(FlaskForm):
    image = FileField(label='Upload image', validators=[
                      DataRequired(), validate_file])
    submit = SubmitField(label='Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = UploadForm()
    roughness_value = None
    if form.validate_on_submit():
        image = form.image.data
        # Should we save the images
        # image.save(os.path.join(
        #     app.config['UPLOAD_FOLDER'], secure_filename(image.filename)))
        image = np.array(Image.open(image))
        image = cv.resize(image, (280, 180), interpolation=cv.INTER_AREA)
        image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        image = np.expand_dims(np.array(image/255), (0, 3))
        roughness_value = model.predict(image)[0][0]
        return render_template('index.html', form=form, roughness_value=roughness_value)
    return render_template('index.html', form=form, roughness_value=roughness_value)


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
