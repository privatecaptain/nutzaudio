import time
import slate
import re

while True:
	try:
		fileName = raw_input('Enter file name : ')
		f = open(fileName,'rb')
		print 'Loading file...'
		break
	except IOError,e:
		print 'File not found, try again!'



t1 = time.time()
doc = slate.PDF(f)



print time.time() - t1, 'secs..'

def get_info(page):
	info = {}
	items = get_items(page)
	weight = str(items*100)
	page = remove_ship(page)
	ship_to = page.find('Ship To')
	bill_to = page.find('Bill To')
	order_id = page.find('Order ID')
	order_date = page.find('Order Date')
	item_number = page.find('Item Number')
	item_desc = page.find('Item Description')
	if ship_to < bill_to:
		name = page[bill_to:item_desc]
		address = page[ship_to:bill_to]
	else:
		name = page[bill_to:ship_to]
		address = page[ship_to:item_desc]
	ref_num = page[order_id:item_number]
	date = page[order_date:order_id]
	# Clean strings
	name = name.replace('Bill To','')
	address = address.replace('Ship To','')
	address = address.strip()
	ref_num = ref_num.replace('Order ID','')
	date = date.replace('Order Date','')
	info = {
		'name' : name.strip(),
		'ref_num' : ref_num.strip(),
		'date' : date.strip(),
		'items' : items,
		'weight' : weight
	}
	if address != '':	
		info.update(parse_address(address))
	for i in info:
		if type(info[i]) == str:
			info[i] = info[i].replace('\n',' ')
	return info


def remove_ship(page):
	page = page.replace('Shipped Via','')
	page = page.replace('STANDARD','')
	return page


def parse_address(address):
	address = address.split('\n')
	address = address[::-1]
	zip_code = address[0]
	country_code = address[1]
	city = address[2]
	street = ' '.join(address[3:-1])
	return {
		'street' : street.decode(errors='ignore'),
		'city': city.decode(errors='ignore'),
		'country_code' : country_code,
		'zip_code' :zip_code
	}

def export(info):

	for i in info:
		line = '"IG1","1",'
		line += '"' + i['ref_num'] + '",'
		line += '"' + i['name'].decode(errors='ignore') + '",'
		line += '"' + i['street'] + '",'
		line += '"' + i['city'] + '",'
		line += '"' + i['country_code'] + '",'
		line += '"' + i['zip_code'] + '",'
		line += '"' + str(i['items']) + '",'
		line += '"' + i['weight'] + '"\n'

		w.write(line)

def get_items(page):
	ids = re.findall('[\d]{9}',page)
	return len(ids) - 1




info = []
for idx,e in enumerate(doc):
	temp = get_info(e)
	temp['id'] = idx
	if temp['name'] != '':
		info.append(temp)


csv_name = raw_input('Enter csv name : ')

w = open(csv_name+'.csv','w')

export(info)
w.close()

raw_input('Press enter to exit.')

