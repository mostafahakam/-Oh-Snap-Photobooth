from InstagramAPI import InstagramAPI

api = InstagramAPI("ohsnap_391", "ohsnap_391pass")


def upload_to_Instagram(filename):

    if api.login():
        api.getSelfUserFeed()  # get self user feed
        print(api.LastJson)  # print last response JSON
        print("Login succes!")

        photo_path = '/var/www/static/img/' + filename
        caption = "Testing"
        api.uploadPhoto(photo_path, caption=caption)
        api.logout()


    else:
        print("Can't login!")
