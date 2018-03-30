from InstagramAPI import InstagramAPI
import requests
import face_recognition
import struct
import imghdr

api = InstagramAPI("ohsnap_391", "ohsnap_391pass")


def upload_to_Instagram(ig, filename):

    r = requests.get('https://www.instagram.com/' + ig + '/?__a=1')
    user_pk = r.json()['graphql']['user']['id']

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

    for (top, right, bottom, left) in face_locations:
        x = ((right + left)/2)/width
        y = bottom/height


    print(getImageSize(photo_path))

    media = [
        {
            'type': 'photo',
            'file': 'logo.jpg',  # Path to the photo file.
        },
        {
            'type': 'photo',
            'file': photo_path,  # Path to the photo file.
            'usertags': [
                {
                    'position': [x, y],
                    'user_id': user_pk,
                },
            ]
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