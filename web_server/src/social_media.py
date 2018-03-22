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

    caption = "Testing"
    api.uploadPhoto(photo_path, caption=caption)
