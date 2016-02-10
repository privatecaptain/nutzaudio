import time
import slate
from Tkinter import *
from tkFileDialog import *

fileName = raw_input('Enter file name : ')

f = open(fileName,'rb')

t1 = time.time()
doc = slate.PDF(f)

print time.time() - t1

def get_info(page):
	info = {}
	page = remove_ship(page)
	ship_to = page.find('Ship To')
	bill_to = page.find('Bill To')
	shipped_via = page.find('Shipped Via')
	item_desc = page.find('Item Description')
	name = page[bill_to:ship_to]
	address = page[ship_to:item_desc]
	return {
		'name' : name.strip(),
		'address' : address.strip()
	}


def remove_ship(page):
	a = page.find('Shipped Via')
	b = page.find('STANDARD')
	return page[:a] + page[b+8:]
