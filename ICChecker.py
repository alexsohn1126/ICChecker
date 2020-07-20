import requests
from typing import List, Tuple
from bs4 import BeautifulSoup as bs
import re


class IC:
	"""
	A general interest check related to keyboards.

	=== Public Attributes ===
	page:
		Beautiful soup object for the IC
	gbDate:
		Group Buy Date (if available)
	picURL:
		URL for the first picture included in the post
	"""

	def __init__(self, url: str) -> None:
		self.page = bs(requests.get(url).content, 'html.parser')
		self.gbDate = None
		self.picURL = ''
		self.price = None

	def _isolate_text(self) -> str:
		first_post = self.page.find(class_="inner")
		first_post_text = first_post.get_text()
		return first_post_text

	def find_details(self):
		post_text = self._isolate_text()

		# find Groupbuy date
		for month in ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'June',
					 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'):
			match_month_date = re.search(month + '[1-3][0-9]|[1-9]', post_text)
			match_date_month = re.search('([1-3][0-9]|[1-9]) ', post_text)


class KeyboardIC(IC):
	def __init__(self, url: str):
		IC.__init__(self, url)
		self.keyboardName = None
		self.keyboardSize = None
		self.keyboardMount = None


class KeycapIC(IC):
	def __init__(self, url: str):
		IC.__init__(self, url)
		self.profile = None

	def find_details(self):
		pass

