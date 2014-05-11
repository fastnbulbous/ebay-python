from ebaysdk import finding, shopping
import json
import pprint
import urllib
import pyimgur
import re
import logging
logging.basicConfig(filename='ebay-shopping.log',level=logging.DEBUG)

from ebay.finding import (getSearchKeywordsRecommendation, findItemsByKeywords, 
                          findItemsByCategory, findItemsAdvanced, 
                          findItemsByProduct, findItemsIneBayStores, 
                          getHistograms)

from lxml import objectify
from ebay.utils import set_config_file

from ebay.shopping import *

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
	ebayItemId = "".join(item['itemId'])
	itemName = "".join(item['title'])
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
	# try:
			bigURL = "".join(item['pictureURLSuperSize'])
			#there is a common pattern of larger images having $_57 as a markup 

			bigFilename =  getBaseFileName(item)+"-med.jpg"
			pprint.pprint("BigURL: " + bigURL)
			storePicture("".join(item['title']), bigURL, bigFilename)

			biggestURL = convertSuperSizeToMax(bigURL)
			pprint.pprint("BiggestURL: " + biggestURL)
			biggestFilename =  getBaseFileName(item)+"-large.jpg"
			storePicture("".join(item['title']), biggestURL, biggestFilename)
	# except:
	# 	logging.warn("Could not process large item")
	#  	print "Could not process large image"

def processItem(item):
	pprint.pprint(item)
	imageURL = "".join(item['galleryURL'])
	ebayItemId ="".join(item['itemId'])
	itemName ="".join(item['title'])

	logging.info(pprint.pformat(item))
	pprint.pprint("ItemID:" + ebayItemId) 
	pprint.pprint("Title:" + itemName) 	
	pprint.pprint("Gallery URL:" + imageURL)

	storePicture(itemName, imageURL, getBaseFileName(item)+"-gallery.jpg")
	processLargePicture(item)


set_config_file("ebay.apikey")
result = GetSingleItem('321403054026')
print result

outputSelector =["PictureURLSuperSize"]
result2 = findItemsAdvanced(keywords="star rubies rubies", outputSelector=outputSelector)
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

findItemsAdvancedResponse = json.loads(result2)['findItemsAdvancedResponse']

for response in findItemsAdvancedResponse:
	for searchResult in response['searchResult']:

		count = searchResult['@count']
		numberOfItems = int(count)
		print("Number of items: " + count )

		if(numberOfItems > 0):
			items = searchResult['item']
			logging.info(pprint.pformat(items))
			
			if(numberOfItems > 0):
				logging.info("Multiple items:" + count )
				for item in items:
					processItem(item)
			else:
				#single item
				logging.info("Single item:" + count )
				processItem(items)	
		else:
			print "No items for search " + ebaySearchTerms
			logging.info("No items:" + count )	



# root = objectify.fromstring(result)
# ack = root.ack.text

