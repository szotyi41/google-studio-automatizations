import re 

def get_element_by_inner_text(elements, innerText, regex=False):

	foundElement = False
	
	for element in elements:
		currentElementText = element.get_attribute('innerText')

		# By regex
		if (regex == True and re.search(innerText, currentElementText)):
			foundElement = element
			break

		# By text
		if currentElementText.strip() == innerText:
			foundElement = element
			break

	print('Element found: ', foundElement.get_attribute('innerText'))

	return foundElement