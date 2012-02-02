from xml.dom import minidom

def get_element(node, name):
	return node.getElementsByTagName(name)[0].childNodes[0].data

	
dom = minidom.parse('sample.xml')
books = []

for node in dom.firstChild.getElementsByTagName('book'):
	books.append({
		'author': 		get_element(node, 'author'),
		'title': 		get_element(node, 'title'),
		'genre': 		get_element(node, 'genre'),
		'price': 		get_element(node, 'price'),
		'publish_date':	get_element(node, 'publish_date'),
		'description':	get_element(node, 'description')
	})


for book in books:
	if book['author'] == 'Galos, Mike':
		print book['title']

