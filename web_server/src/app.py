import face_recognition
from flask import Flask, jsonify, request, redirect, send_file, url_for
from flask.ext.uploads import UploadSet, configure_uploads, IMAGES
import json
from playhouse.shortcuts import model_to_dict, dict_to_model
import base64
import numpy as np
import os
from werkzeug.utils import secure_filename
import hashlib



from db import *
from auth import *
from social_media import *

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


@app.route('/register_user', methods=['POST'])
def new_user():
    headers = request.headers
    username = headers.get('username')
    password = headers.get('password')

    if username:
        if password:

            hashed_password = hash_password(password)
            if new_User(username, hashed_password):
                return "New User added"
            else:
                return "Username already exists"
        else:
            return "Missing password"
    else:
        return "Missing Username"


@app.route('/login_user', methods=['POST'])
def login():
    headers = request.headers
    username = headers.get('username')
    password = headers.get('password')
    if username:
        if password:

            hashed_password = get_User_pass(username)

            if hashed_password != "Fail":
                if check_password(hashed_password, password):
                    return "Pass"
                else:
                    return "Fail"

            else:
                return "User not in Database"

            return "New User added"
        else:
            return "Missing password"
    else:
        return "Missing Username"


@app.route('/new_face/<user_id>', methods=['POST', 'GET'])
def new_image(user_id):
    # Check if a valid image file was uploaded
    if request.method == 'GET' or request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            print(file.filename)

            # Load the uploaded image file
            filename = secure_filename(file.filename)
            filename = shorten_filename(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


            img = face_recognition.load_image_file(file)

            face_encodings = face_recognition.face_encodings(img)

            # encoded_string = base64.encodestring(file.read())

            if len(face_encodings):
                if len(face_encodings) > 1:
                    response = app.response_class(
                        response="Multiple faces detected",
                        status=404,
                        mimetype='application/json'
                    )
                    return response

                # Get face encodings for any faces in the uploaded image
                # print(user_id, face_encodings.tostring(), encoded_string)

                # Add row to DB

                addUser(user_id, face_encodings[0].tostring(), filename)

                print("New_face: Found face, success")

                response = app.response_class(
                    response="Success",
                    status=200,
                    mimetype='application/json'
                )
                return response

            else:
                print("New_face: No face found, failed")

                response = app.response_class(
                    response="No face detected",
                    status=404,
                    mimetype='application/json'
                )
                return response


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
            filename = secure_filename(file.filename)
            filename = shorten_filename(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            return detect_faces_in_image(file, filename)

    # If no valid image file was uploaded, show the file upload form:
    return 'Image uploaded not valid'


@app.route('/get_images/<user_id>', methods=['GET'])
def ret_images(user_id):
    all_images = []
    for row in Row.select().where(Row.user_id == user_id):
        file_name = row.file_name
        all_images.append(file_name)

    return json.dumps(all_images)


@app.route('/upload_to_instagram/<filename>', methods=['POST'])
def post_to_ig(filename):
    upload_to_Instagram(filename)

    return "Success"



def detect_faces_in_image(file_stream, filename):
    # Load the uploaded image file
    img = face_recognition.load_image_file(file_stream)
    # Get face encodings for any faces in the uploaded image
    unknown_face_encodings = face_recognition.face_encodings(img)

    face_found = False
    result = []


    for i in range(0, len(unknown_face_encodings)):
        face_found = True
        # See if the first face in the uploaded image matches the known face of Obama

        for row in Row.select():
            curr_encoding = row.img_encoding
            np_array = np.fromstring(curr_encoding, dtype=unknown_face_encodings[i].dtype)

            match_results = face_recognition.compare_faces([np_array], unknown_face_encodings[i])
            if match_results[0]:
                result.append(row.user_id)
                addUser(result, unknown_face_encodings[0].tostring(), filename)
                break


    if not result:
        ret = {"face_found_in_image": face_found, "picture_of": "Unrecognized"}

    else:
        ret = {"face_found_in_image": face_found, "picture_of": result}

    return jsonify(ret)


def shorten_filename(filename):
    last_chunk = filename.split("-")[-1]
    return last_chunk

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
