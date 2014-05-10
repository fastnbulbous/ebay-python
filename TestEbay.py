from ebaysdk import finding
import json
import pprint
import urllib
import pyimgur
import re

CLIENT_ID = "b68d1dd5c268cfb" #imgur app id
ebaySearchTerms = "sprewell green gems -(retro)"

def removeDisallowedFilenameChars(filename):
	cleaned_up_filename = re.sub(r'[/\\:*?"<>|]', '', filename)
	return cleaned_up_filename

def uploadToImgur(name, path):
	im = pyimgur.Imgur(CLIENT_ID)
	uploaded_image = im.upload_image(path, title=name)
	print(uploaded_image.title)
	print(uploaded_image.link)
	print(uploaded_image.size)
	print(uploaded_image.type)

def storePicture(name, url, filename):
	print "Saving image: " + filename
	urllib.urlretrieve(url, filename )
	uploadToImgur(name, filename)

def getBaseFileName(item):
	ebayItemId = item['itemId']['value']
	itemName = item['title']['value']
	return removeDisallowedFilenameChars(str(itemName) + "-" + ebayItemId)

def convertSuperSizeToMax(url):
	return url.replace("$_3", "$_57")


def processLargePicture(item):
	try:
		bigURL = item['pictureURLSuperSize']['value']
		#there is a common pattern of larger images having $_57 as a markup 

		biggestURL = convertSuperSizeToMax(bigURL)

		bigFilename =  getBaseFileName(item)+".jpg"
		storePicture(item['title']['value'], biggestURL, bigFilename)
	except:
	 	print "Could not process large image"

def processItem(item):
	pprint.pprint(item)
	imageURL = item['galleryURL']['value']
	ebayItemId =item['itemId']['value']
	itemName =item['title']['value']
	print "ItemID:" + ebayItemId 
	print "Title:" + itemName
	print "Gallery URL:" + imageURL

	storePicture(itemName, imageURL, getBaseFileName(item)+"-gallery.jpg")
	processLargePicture(item)


api = finding(appid='TomLinge-452a-421b-bd32-289d2152277f')


keywords = 'star rubies 1997'
outputSelector =["PictureURLSuperSize"]


api.execute('findItemsAdvanced', 
		     {'keywords': ebaySearchTerms,
		     'outputSelector':['PictureURLSuperSize']})


output = api.response_dict();
#pprint.pprint(output)

count = output['searchResult']['count']['value']
numberOfItems = int(count)
print "Number of items" + count

if(numberOfItems > 0):
	items = output['searchResult']['item']
	pprint.pprint(items)
	if(numberOfItems > 1):
		for item in items:
			print "mulit items"
			processItem(item)
	else:
		#single item
		print "single item"
		processItem(items)	
else:
	print "no items!"			

