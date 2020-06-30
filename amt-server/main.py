# Created by khanhdh on 6/22/20
import hashlib
import logging
import os
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, request, send_file, render_template
from pydub import AudioSegment
from werkzeug.utils import secure_filename, redirect

from amt.converter.transcript_cnn import convert_to_midi

logger = logging.getLogger('main')

DOT_ENV_PATH = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(DOT_ENV_PATH)

APP_PORT = os.getenv('APP_PORT')

DATA_FOLDER = os.getenv('DATA_FOLDER')
INPUT_FOLDER = os.path.join(DATA_FOLDER, os.getenv('INPUT_FOLDER'))
OUTPUT_FOLDER = os.path.join(DATA_FOLDER, os.getenv('OUTPUT_FOLDER'))

SUPPORTED_FORMATS = ['.mp3', '.wav']


app = Flask(__name__)


def convert_input_file_to_wav(file_name):
    new_file_name = f"{hashlib.md5((file_name + str(datetime.now())).encode()).hexdigest()}.wav"
    global audio

    if file_name[-4:] == '.wav':
        os.rename(os.path.join(INPUT_FOLDER, file_name), os.path.join(INPUT_FOLDER, new_file_name))

    if file_name[-4:] == '.mp3':
        audio = AudioSegment.from_mp3(os.path.join(INPUT_FOLDER, file_name))
        audio.export(os.path.join(INPUT_FOLDER, new_file_name), format="wav")
        os.remove(os.path.join(INPUT_FOLDER, file_name))

    return new_file_name


@app.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return render_template('submit.html', message='File has not been chosen')
    file = request.files['file']
    if file.filename == '':
        return render_template('submit.html', message='No file name')
    file_name = secure_filename(file.filename)
    if file_name[-4:] not in SUPPORTED_FORMATS:
        return render_template('submit.html', message='Not supported format')
    file.save(os.path.join(INPUT_FOLDER, file_name))
    new_file_name = convert_input_file_to_wav(file_name)[:-4]
    convert_to_midi(
        os.path.join(INPUT_FOLDER, f"{new_file_name}.wav"),
        os.path.join(OUTPUT_FOLDER, f"{new_file_name}.mid")
    )
    return new_file_name


@app.route('/download/<file_name>', methods=['GET'])
def return_files_tut(file_name):
    file_path = os.path.join(OUTPUT_FOLDER, f"{file_name}.mid")
    return send_file(file_path, as_attachment=True, attachment_filename='')


if __name__ == "__main__":
    app.run(port=APP_PORT)
