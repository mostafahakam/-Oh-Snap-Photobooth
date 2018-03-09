# This is a _very simple_ example of a web service that recognizes faces in uploaded images.
# Upload an image file and it will check if the image contains a picture of Barack Obama.
# The result is returned as json. For example:
#
# $ curl -XPOST -F "file=@obama2.jpg" http://127.0.0.1:5001
#
# Returns:
#
# {
#  "face_found_in_image": true,
#  "is_picture_of_obama": true
# }
#
# This example is based on the Flask file upload example: http://flask.pocoo.org/docs/0.12/patterns/fileuploads/

# NOTE: This example requires flask to be installed! You can install it with pip:
# $ pip3 install flask

import face_recognition
from flask import Flask, jsonify, request, redirect, send_file, url_for
from flask.ext.uploads import UploadSet, configure_uploads, IMAGES
import json
from db import *
from playhouse.shortcuts import model_to_dict, dict_to_model
import base64
import numpy as np
import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = '/var/www/static/img'

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.before_request
def before_request():
    db.connect()


@app.after_request
def after_request(response):
    db.close()
    return response

@app.route('/checkout_db', methods=['GET', 'POST'])
def peek_db():
    checkout_db()
    return 1


@app.route('/new_face/<user_id>', methods=['POST'])
def new_image(user_id):
    # Check if a valid image file was uploaded
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # Load the uploaded image file
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            img = face_recognition.load_image_file(file)

            encoded_string = base64.encodestring(file.read())


            # Get face encodings for any faces in the uploaded image
            face_encodings = face_recognition.face_encodings(img)[0]


            #print(user_id, face_encodings.tostring(), encoded_string)

            # Add row to DB
            addUser(user_id, face_encodings.tostring(), filename)

            return "Success"

    # If no valid image file was uploaded, show the file upload form:
    return 'Image uploaded not valid'


@app.route('/detect_face', methods=['GET', 'POST'])
def upload_image():
    # Check if a valid image file was uploaded
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # The image file seems valid! Detect faces and return the result.
            return detect_faces_in_image(file)

    # If no valid image file was uploaded, show the file upload form:
    return 'Image uploaded not valid'


@app.route('/get_images/<user_id>', methods=['GET'])
def ret_images(user_id):
	all_images = []
	for row in Row.select().where(Row.user_id == user_id):
		all_images.append(Row.file_name)

	return json.dumps(all_images)



def detect_faces_in_image(file_stream):
    # Load the uploaded image file
    img = face_recognition.load_image_file(file_stream)
    # Get face encodings for any faces in the uploaded image
    unknown_face_encodings = face_recognition.face_encodings(img)

    face_found = False
    result = False

    if len(unknown_face_encodings) > 0:
        face_found = True
        # See if the first face in the uploaded image matches the known face of Obama

        for row in Row.select():
            curr_encoding = row.img_encoding
            np_array = np.fromstring(curr_encoding, dtype=unknown_face_encodings[0].dtype)

            match_results = face_recognition.compare_faces([np_array], unknown_face_encodings[0])
            if match_results[0]:
                result = row.user_id
                break

    if result == False:
        ret = {"face_found_in_image": face_found, "picture_of": "Unrecognized"}

    else:
        ret = {"face_found_in_image": face_found, "picture_of": result}

    return jsonify(ret)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
