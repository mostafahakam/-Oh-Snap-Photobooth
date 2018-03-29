from InstagramAPI import InstagramAPI
import requests

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
