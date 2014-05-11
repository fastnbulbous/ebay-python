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

set_config_file("ebay.apikey")
result = GetSingleItem('321403054026')
print result

result2 = findItemsAdvanced(keywords="star rubies")
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
print result2


# root = objectify.fromstring(result)
# ack = root.ack.text

