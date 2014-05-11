from ebaysdk import finding, shopping
import json
import pprint
import urllib
import pyimgur
import re
import logging
logging.basicConfig(filename='ebayupload.log',level=logging.DEBUG)

IMGUR_CLIENT_ID = "b68d1dd5c268cfb" 
EBAY_APP_ID = "TomLinge-452a-421b-bd32-289d2152277f"
ebaySearchTerms = "sprewell star rubies (1997, 1998, 1999) -(retro)"
outputSelector =["PictureURLSuperSize"]

def removeDisallowedFilenameChars(filename):
	cleaned_up_filename = re.sub(r'[/\\:*?"<>|]', '', filename)
	return cleaned_up_filename

def uploadToImgur(name, path):
	return
	im = pyimgur.Imgur(IMGUR_CLIENT_ID)
	uploaded_image = im.upload_image(path, title=name)
	logging.info(uploaded_image.title)
	logging.info(uploaded_image.link)
	logging.info(uploaded_image.size)
	logging.info(uploaded_image.type)

def storePicture(name, url, filename):
	logging.info("Saving image: " + filename)
	urllib.urlretrieve(url, filename )
	uploadToImgur(name, filename)

def getBaseFileName(item):
	ebayItemId = item['itemId']['value']
	itemName = item['title']['value']
	return removeDisallowedFilenameChars(str(itemName) + "-" + ebayItemId)

def convertSuperSizeToMax(url):

	if(url.count("_3") > 0):
		return url.replace("_3", "_57")
	elif (url.count("_12") > 0):
		return url.replace("_12", "_57")
	else:
		logging.warn("There is no alternative for url:" + url)
		return url

def processLargePicture(item):
	try:
		bigURL = item['pictureURLSuperSize']['value']
		#there is a common pattern of larger images having $_57 as a markup 

		bigFilename =  getBaseFileName(item)+"-med.jpg"
		pprint.pprint("BigURL: " + bigURL)
		storePicture(item['title']['value'], bigURL, bigFilename)

		biggestURL = convertSuperSizeToMax(bigURL)
		pprint.pprint("BiggestURL: " + biggestURL)
		biggestFilename =  getBaseFileName(item)+"-large.jpg"
		storePicture(item['title']['value'], biggestURL, biggestFilename)
	except:
		logging.warn("Could not process large item")
	 	print "Could not process large image"

def processItem(item):
	
	imageURL = item['galleryURL']['value']
	ebayItemId =item['itemId']['value']
	itemName =item['title']['value']

	logging.info(pprint.pformat(item))
	pprint.pprint("ItemID:" + ebayItemId )	
	pprint.pprint("Title:" + itemName )	
	pprint.pprint("Gallery URL:" + imageURL)	

	storePicture(itemName, imageURL, getBaseFileName(item)+"-gallery.jpg")
	processLargePicture(item)


api = shopping(appid=EBAY_APP_ID, debug=True)



logging.info("Search Tearms: " + ebaySearchTerms )


# api.execute('findItemsAdvanced', 
# 		     {'keywords': ebaySearchTerms,
# 		     'outputSelector':['PictureURLSuperSize']})


api.execute('horseshit', 
 		     {'ItemId': '321403054026'})

output = api.response_dict();
pprint.pprint(output)  

# count = output['searchResult']['count']['value']
# numberOfItems = int(count)
# logging.info("Number of items" + count )

# if(numberOfItems > 0):
# 	items = output['searchResult']['item']
# 	logging.info(pprint.pformat(items))
# 	if(numberOfItems > 1):
# 		logging.info("Multiple items:" + count )
# 		for item in items:
# 			processItem(item)
# 	else:
# 		#single item
# 		logging.info("Single item:" + count )
# 		processItem(items)	
# else:
# 	print "No items for search " + ebaySearchTerms
# 	logging.info("No items:" + count )			

