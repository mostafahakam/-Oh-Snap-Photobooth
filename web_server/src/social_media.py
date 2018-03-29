from InstagramAPI import InstagramAPI
import requests
import face_recognition

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

    for location in face_locations:
        print(location)

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
                    'position': [0.0, 0.0],
                    'user_id': user_pk,
                },
            ]
        },
    ]
    caption = "Testing"
    api.uploadAlbum(media, caption=caption)
