from InstagramAPI import InstagramAPI
import requests
import face_recognition
import struct
import imghdr
import numpy as np

from db import *
from social_media import *

api = InstagramAPI("ohsnap_391", "ohsnap_391pass")


def upload_to_Instagram(filename):
    if not api.isLoggedIn:

        if api.login():
            api.getSelfUserFeed()  # get self user feed
            print(api.LastJson)  # print last response JSON
            print("Login succes!")

        else:
            print("Can't login!")
            return

    print("Is logged in: " + str(api.isLoggedIn))
    photo_path = '/var/www/static/img/' + filename

    image = face_recognition.load_image_file(photo_path)
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)

    width, height = getImageSize(photo_path)

    usertags = []

    for i in range(0, len(face_encodings)):
        for row in Row.select():
            curr_encoding = row.img_encoding
            np_array = np.fromstring(curr_encoding, dtype=face_encodings[i].dtype)

            match_results = face_recognition.compare_faces([np_array], face_encodings[i])
            if match_results[0]:
                (top, right, bottom, left) = face_locations[i]
                x = ((right + left) / 2) / width
                y = bottom / height

                for user in Social.select().where(Social.user_id == row.user_id):
                    ig = user.instagram_handle

                r = requests.get('https://www.instagram.com/' + ig + '/?__a=1')
                user_pk = r.json()['graphql']['user']['id']

                usertags.append({'position': [x, y], 'user_id': user_pk})

    usertags = [
            {  # Optional, lets you tag one or more users in a PHOTO.
                'position': [0.5, 0.5],
                # WARNING: THE USER ID MUST BE VALID. INSTAGRAM WILL VERIFY IT
                # AND IF IT'S WRONG THEY WILL SAY "media configure error".
                'user_id': '536372018',  # Must be a numerical UserPK ID.
            },
            {
                'position': [0.0, 0.0],
                # WARNING: THE USER ID MUST BE VALID. INSTAGRAM WILL VERIFY IT
                # AND IF IT'S WRONG THEY WILL SAY "media configure error".
                'user_id': '352713272',  # Must be a numerical UserPK ID.
            },
        ]

    media = [
        {
            'type': 'photo',
            'file': 'logo.jpg',  # Path to the photo file.
        },
        {
            'type': 'photo',
            'file': photo_path,  # Path to the photo file.
            'usertags': usertags
        },
    ]
    caption = "Testing"
    api.uploadAlbum(media, caption=caption)


def getImageSize(fname):
    with open(fname, 'rb') as fhandle:
        head = fhandle.read(24)
        if len(head) != 24:
            raise RuntimeError("Invalid Header")
        if imghdr.what(fname) == 'png':
            check = struct.unpack('>i', head[4:8])[0]
            if check != 0x0d0a1a0a:
                raise RuntimeError("PNG: Invalid check")
            width, height = struct.unpack('>ii', head[16:24])
        elif imghdr.what(fname) == 'gif':
            width, height = struct.unpack('<HH', head[6:10])
        elif imghdr.what(fname) == 'jpeg':
            fhandle.seek(0)  # Read 0xff next
            size = 2
            ftype = 0
            while not 0xc0 <= ftype <= 0xcf:
                fhandle.seek(size, 1)
                byte = fhandle.read(1)
                while ord(byte) == 0xff:
                    byte = fhandle.read(1)
                ftype = ord(byte)
                size = struct.unpack('>H', fhandle.read(2))[0] - 2
            # We are at a SOFn block
            fhandle.seek(1, 1)  # Skip `precision' byte.
            height, width = struct.unpack('>HH', fhandle.read(4))
        else:
            raise RuntimeError("Unsupported format")
        return width, height
