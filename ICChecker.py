import requests
from typing import List
from bs4 import BeautifulSoup as bs
import json
import re

class InterestCheck:
	"""
	A general interest check related to keyboards.

	=== Public Attributes ===
	page:
		Beautiful soup object for the IC
	gbDate:
		Group Buy Date (if available)
	picsURL:
		URL for the pictures included in the post
	"""

	def __init__(self, url: str) -> None:
		self.url = url
		self.post = bs(requests.get(url).content,
						'html.parser').find(class_="inner")
		self.pics_url = [img.get('src') for img in self.post.find_all('img')]
		self.gbDate = None
		self.price = None

	def export_to_json(self) -> None:
		ic_info_json = open('interest_check.json', 'a')
		ic_info_dict = {
			'url': self.url,
			'pics_url': self.pics_url,
			'gbDate': None,
			'price': None
		}
		json.dump(ic_info_dict, ic_info_json, indent = 4)
		ic_info_json.close()

	def _isolate_text(self) -> str:
		first_post_text = self.post.get_text()
		return first_post_text

	# def find_details(self):
	# 	post_text = self._isolate_text()

	# 	# find Groupbuy date
	# 	for month in ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'June',
	# 				 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'):
	# 		match_month_date = re.search(month + '[1-3][0-9]|[1-9]', post_text)
	# 		match_date_month = re.search('([1-3][0-9]|[1-9]) ', post_text)


class KeyboardIC(InterestCheck):
	def __init__(self, url: str):
		IC.__init__(self, url)
		self.keyboardName = None
		self.keyboardSize = None
		self.keyboardMount = None


class KeycapIC(InterestCheck):
	def __init__(self, url: str):
		IC.__init__(self, url)
		self.profile = None

	def find_details(self):
		pass

def get_posts(url: str) -> List[str]:
	ic_list_page = bs(requests.get(url).content, 'html.parser')
	ic_list_links = []
	# search for a html tag with 6 or 5 digits followed by .0, and has no class
	# link with 36672 is the rules for IC section, thus ignored.
	for ic in ic_list_page.find_all(href = re.compile(
									'(?!36672)(\d{6}|\d{5})\.0$'),
									class_= False):
		ic_list_links.append(ic.get('href'))
	return ic_list_links


if __name__ == "__main__":
	ic_first_list = get_posts('https://geekhack.org/index.php?board=132.0')
	for ic in ic_first_list:
		print(ic)
	# KIC = InterestCheck('https://geekhack.org/index.php?topic=105440.0')
	# for picURL in KIC.pics_url:
	# 	print(picURL)
	# KIC.export_to_json()
