from InstagramAPI import InstagramAPI
from PIL import Image

api = InstagramAPI("cpen391_ohsnap", "ohsnap_391pass")


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
    img = Image.open(photo_path)

    img.save('instagram/'+filename.split(".")[0], 'jpg')
    caption = "Testing"

    api.uploadPhoto('instagram/'+filename.split(".")[0] + '.jpg', caption=caption)
