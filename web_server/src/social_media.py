from InstagramAPI import InstagramAPI


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

    media = [
        {
            'type': 'photo',
            'file': 'logo.jpg',  # Path to the photo file.
        },
        {
            'type': 'photo',
            'file': photo_path,  # Path to the photo file.
            'usertags': [
                {  # Optional, lets you tag one or more users in a PHOTO.
                    'position': [0.5, 0.5],
                    # WARNING: THE USER ID MUST BE VALID. INSTAGRAM WILL VERIFY IT
                    # AND IF IT'S WRONG THEY WILL SAY "media configure error".
                    'user_id': '123456789',  # Must be a numerical UserPK ID.
                },
            ]
        },
    ]
    caption = "Testing"
    api.uploadAlbum(media, caption=caption)
