from ebaysdk import finding
import json
import pprint
import urllib
import pyimgur

CLIENT_ID = "b68d1dd5c268cfb"
PATH = "A Filepath to an image on your computer"

def uploadToImgur(path):
	im = pyimgur.Imgur(CLIENT_ID)
	uploaded_image = im.upload_image(path, title="Uploaded with PyImgur")
	print(uploaded_image.title)
	print(uploaded_image.link)
	print(uploaded_image.size)
	print(uploaded_image.type)



api = finding(appid='TomLinge-452a-421b-bd32-289d2152277f')


keywords = 'star rubies 1997'
outputSelector =["PictureURLSuperSize"]


api.execute('findItemsAdvanced', 
		     {'keywords': 'star rubies 1997',
		     'outputSelector':['PictureURLSuperSize']})


output = api.response_dict();
#pprint.pprint(output)

count = output['searchResult']['count']['value']
number = int(count)


items = output['searchResult']['item']
#pprint.pprint(items)


for item in output['searchResult']['item']:
	imageURL = item['galleryURL']['value']
	bigURL = item['pictureURLSuperSize']['value']
	filename = str(item['itemId']['value'])+".jpg"
	urllib.urlretrieve(bigURL, filename)
	uploadToImgur(filename)
