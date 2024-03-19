from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, SelectField, FileField
from wtforms.validators import DataRequired, ValidationError
from dotenv import load_dotenv
import os
import tensorflow as tf


model = tf.keras.models.load_model('output/model.h5')

app = Flask(__name__)
load_dotenv()
app.secret_key = os.getenv('secret_key')


class UploadForm(FlaskForm):
    image = FileField(label='Upload Image', validators=[DataRequired()])
    submit = SubmitField(label='Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = UploadForm()
    if form.validate_on_submit():
        return redirect(url_for('index'))
    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
