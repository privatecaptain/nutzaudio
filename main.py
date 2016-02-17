import time
import slate
import re
from unidecode import unidecode

while True:
	try:
		fileName = raw_input('Enter file name : ')
		f = open(fileName,'rb')
		lang = raw_input('Enter "en" for English or "nl" for Dutch : ')
		print 'Loading file...'
		break
	except IOError,e:
		print 'File not found, try again!'



t1 = time.time()
doc = slate.PDF(f)



print time.time() - t1, 'secs..'
def get_points(lang,page):
	points = {}
	if lang == 'nl':
		points['ship_to'] = 'Verzenden\nnaar'
		points['bill_to'] = 'Factureren aan'
		points['order_id'] = 'Ordernummer'
		points['order_date'] = 'Besteldatum'
		points['item_number'] = 'Productnummer'
		points['item_desc']  = 'Productomschrijving'
		points['vevo'] = 'Vervoerder'
		points['standard'] = 'STANDARD'

	elif lang == 'en':
		points['ship_to'] = 'Ship To'
		points['bill_to'] = 'Bill To'
		points['order_id'] = 'Order ID'
		points['order_date'] = 'Order Date'
		points['item_number'] = 'Item Number'
		points['item_desc']  = 'Item Description'

	for i in points:
		points[i] = page.find(points[i])

	return points

def get_info(page,lang):
	info = {}
	items = get_items(page)
	color = get_color(page)
	weight = str(items*100)
	page = remove_ship(page,lang)
	points = get_points(lang,page)

	for key,val in points.items():
		exec(key + '=val')

	if lang == 'nl':
		name = get_from_header(page,'Factureren aan')
		date = get_from_header(page,'Besteldatum')
		address = get_from_header(page,'Verzenden\nnaar')
		ref_num = get_from_header(page,'Ordernummer')
		
		if 'Ordernummer' in address:
			address = get_from_header(page,'STANDARD')

	else:	
		if ship_to < bill_to:
			name = page[bill_to:item_desc]
			address = page[ship_to:bill_to]
		else:
			name = page[bill_to:ship_to]
			address = page[ship_to:item_desc]
		date = page[order_date:order_id]
		ref_num = page[order_id:item_number]
	# Clean strings
	if lang == 'en':
		name = name.replace('Bill To','')
		address = address.replace('Ship To','')
		ref_num = ref_num.replace('Order ID','')
		date = date.replace('Order Date','')

	address = address.strip()
	# print address

	info = {
		'name' : name.strip(),
		'ref_num' : ref_num.strip(),
		'date' : date.strip(),
		'items' : items,
		'weight' : weight,
		'color' : color
	}
	if address != '':	
		info.update(parse_address(address))
	for i in info:
		if type(info[i]) == unicode:
			info[i] = info[i].replace('\n',' ')
			info[i] = unidecode(info[i])
	info = remove_junk(info)
	return info

def remove_junk(info):
	for i in info:
		a = info[i]
		b = u''
		if type(a) == unicode or type(a) == str:
			for j in a:
				if j.isalnum() or j == ' ':
					b += j
			info[i] = b
	return info

def remove_ship(page,lang):
	if lang == 'en':
		page = page.replace('Shipped Via','')
		page = page.replace('STANDARD','')
	
	return page.decode('utf-8')


def parse_address(address):
	try:
		address = address.split('\n')
		address = address[::-1]
		zip_code = address[0]
		country_code = address[1]
		city = address[2]
		street = ' '.join(address[3:-1])
	except:
		street = ''
		city = ''
		country_code = ''
		zip_code = ''
	return {
		'street' : street,
		'city': city,
		'country_code' : country_code,
		'zip_code' :zip_code
	}

def export(info):

	for i in info:
		for j in range(i['items']):
			line = '"IG1","1",'
			line += '"' + i['color'] + '",'
			line += '"' + i['name'] + '",'
			line += '"' + i['street'] + '",'
			line += '"' + i['city'] + '",'
			line += '"' + i['country_code'] + '",'
			line += '"' + i['zip_code'] + '",'
			line += '"1",'
			line += '"100",'
			line += '"' + i['date'] + '"\n'
			w.write(line)

def get_items(page):
	ids = re.findall(r'\b[\d]{9}\b',page)
	return len(ids) - 1

def get_color(page):
	trans = {'Rood' : 'Red',
			 'Groen' : 'Green',
			 'Oranje' : 'Orange',
			 'Geel' : 'Yellow',
			 'Rouge' : 'Red',
			 'Vert' : 'Green',
			 'Jaune' : 'Yellow',
			 'Fraise' : 'Strawberry',
			 'Pomme' : 'Apple',
			 'Orange' : 'Orange',
			 'Banana' : 'Banana'


			}
	colors = re.findall('- [a-zA-Z]+',page)
	if colors:
		color = colors[0]
		for i in colors:		
			i = i.replace('-','')
			i = i.replace(' ','')
			
			if i in trans.keys():
				color = i
				break
		if color in trans.keys():
			return trans[color]
		else:
			print color
			return color
	return ''


def get_from_header(page,header):
	start = page.find(header)
	page = page[start:]
	start = page.find('\n\n') + 2
	page = page[start:]
	end = page.find('\n\n')
	return page[:end]


info = []
for idx,e in enumerate(doc):
	temp = get_info(e,lang)
	temp['id'] = idx
	if temp['name'] != '':
		info.append(temp)


csv_name = raw_input('Enter csv name : ')

w = open(csv_name+'.csv','w')

export(info)
w.close()

raw_input('Press enter to exit.')

