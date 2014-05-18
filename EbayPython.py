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
                          findCompletedItems, getHistograms)

from lxml import objectify
from ebay.utils import set_config_file

from ebay.shopping import *

set_config_file("ebay.apikey")

def stripPictureURL(pictureURL):
	# we normally get a URL from the picture gallery of completed items like: 
	# http://i.ebayimg.com/00/s/MTQ4OFg5NTQ=/z/DdQAAMXQeW5Tbuyw/$_1.JPG?set_id=880000500F we need to strip off the 
	# ? crap and also replace _1 with _57 which is the largest image
	# ie -> http://i.ebayimg.com/00/s/MTQ4OFg5NTQ=/z/DdQAAMXQeW5Tbuyw/$_57.JPG

	#Split the string at the first occurrence of sep, and return a 3-tuple containing the part before the separator, 
	#the separator itself, and the part after the separator. 
	#If the separator is not found, return a 3-tuple containing the string itself, followed by two empty strings.
	stripURL = pictureURL.partition('_1')[0]
	stripURL += "_57.jpg"
	return stripURL

def downloadItemGallery(itemID):
	result = json.loads(GetSingleItem(itemID))
	pprint.pprint(result)

	item = result['Item']
	title = result['Item']['Title']
	pictures = result['Item']['PictureURL']

	#description = result['Item']['Description']

	#pprint.pprint(description)

	count = 1
	for picture in pictures:
		fileName = getBaseFileName(title, itemID) + str(count) + ".jpg"
		storePicture(title, stripPictureURL(picture), fileName)
		count += 1

	return result	

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

def getBaseFileName(itemName, itemID):
	# ebayItemId = "".join(item['itemId'])
	# itemName = "".join(item['title'])
	return removeDisallowedFilenameChars(itemName + "-" + itemID)

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
		bigURL = "".join(item['pictureURLSuperSize'])
		#there is a common pattern of larger images having $_57 as a markup 

		baseFileName = getBaseFileName("".join(item['title']), "".join(item['itemId']))

		bigFilename =  baseFileName+"-med.jpg"
		pprint.pprint("BigURL: " + bigURL)
		storePicture("".join(item['title']), bigURL, bigFilename)

		biggestURL = convertSuperSizeToMax(bigURL)
		pprint.pprint("BiggestURL: " + biggestURL)
		biggestFilename =  baseFileName+"-large.jpg"
		storePicture("".join(item['title']), biggestURL, biggestFilename)
	except KeyError, e:
			keyError = e
			print keyError
	except: #general error
	 	e = sys.exc_info()[0]
	 	print e

def processItem(item):
	try:
		pprint.pprint(item)
		imageURL = "".join(item['galleryURL'])
		ebayItemId ="".join(item['itemId'])
		itemName ="".join(item['title'])

		logging.info(pprint.pformat(item))
		pprint.pprint("ItemID:" + ebayItemId) 
		pprint.pprint("Title:" + itemName) 	
		pprint.pprint("Gallery URL:" + imageURL)

		storePicture(itemName, imageURL, getBaseFileName(itemName, ebayItemId)+"-gallery.jpg")
		#processLargePicture(item)
		downloadItemGallery(ebayItemId)
	except KeyError, e:
			keyError = e
			print keyError
	except: #general error
	 	e = sys.exc_info()[0]
	 	print e

def processSearchResult(searchResult):
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

if  __name__ =='__main__':

	outputSelector =["PictureURLSuperSize"]
	advancedSearchResult = findItemsAdvanced(keywords="dimensions sprewell", outputSelector=outputSelector)


	# findItemsAdvancedResponse = json.loads(advancedSearchResult)['findItemsAdvancedResponse']

	# for response in findItemsAdvancedResponse:
	# 	for searchResult in response['searchResult']:
	# 		processSearchResult(searchResult)

	completedItemsSearchResult = findCompletedItems(keywords="1997 star rubies", outputSelector=outputSelector)

	completedItems = json.loads(completedItemsSearchResult)['findCompletedItemsResponse']
	pprint.pprint(completedItems)

	for completeItem in completedItems:
	 	for searchResult in completeItem['searchResult']:
			processSearchResult(searchResult)


	downloadItemGallery("291140900328")#test getting gallery and price for jordan precious metal, best offer from but it now
	downloadItemGallery("141279661978")# pwcc rodman rubies compete auction
	downloadItemGallery("131107659173")# nowitski 9.5 buy it now ended
	downloadItemGallery("141279662913")# pwcc rodman rubies compete auction
	downloadItemGallery("400566974362")#active listing iversoon hoops
	downloadItemGallery("131172098101")# completed but ended early malone

