import time
import slate
import progressbar

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
	page = remove_ship(page)
	ship_to = page.find('Ship To')
	bill_to = page.find('Bill To')
	order_id = page.find('Order ID')
	item_number = page.find('Item Number')
	item_desc = page.find('Item Description')
	if ship_to < bill_to:
		name = page[bill_to:item_desc]
		address = page[ship_to:bill_to]
	else:
		name = page[bill_to:ship_to]
		address = page[ship_to:item_desc]
	ref_num = page[order_id:item_number]
	# Clean strings
	name = name.replace('Bill To','')
	address = address.replace('Ship To','')
	ref_num = ref_num.replace('Order ID','')
	return {
		'name' : name.strip(),
		'address' : address.strip(),
		'ref_num' : ref_num.strip()
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


csv_name = raw_input('Enter csv name : ')

w = open(csv_name+'.csv','w')

for i in info:
	t = i['ref_num']+','+i['name']+';\n'
	w.write(t)

w.close()

raw_input('Press enter to exit.')

