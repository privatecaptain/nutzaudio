import time
import slate
from Tkinter import *
from tkFileDialog import *

fileName = raw_input('Enter file name : ')

f = open(fileName,'rb')

t1 = time.time()
doc = slate.PDF(f)

print time.time() - t1, 'secs..'

def get_info(page):
	info = {}
	page = remove_ship(page)
	ship_to = page.find('Ship To')
	bill_to = page.find('Bill To')
	item_desc = page.find('Item Description')

	if ship_to < bill_to:
		name = page[bill_to:item_desc]
		address = page[ship_to:bill_to]
	else:

		name = page[bill_to:ship_to]
		address = page[ship_to:item_desc]
	
	# Clean strings
	name = name.replace('Bill To','')
	address = address.replace('Ship To','')
	return {
		'name' : name.strip(),
		'address' : address.strip()
	}


def remove_ship(page):
	page = page.replace('Shipped Via','')
	page = page.replace('STANDARD','')
	return page

info = []

for idx,e in enumerate(doc):
	temp = get_info(e)
	temp['id'] = idx
	if temp['name'] != '' and temp['address'] != '':
		info.append(temp)

