import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin

def continue_crawl(search_history, target_url, max_steps=25) :
	flag = True
	if search_history[-1] == target_url :
		print("We've found the target article!")
		flag = False
	elif len(search_history) > max_steps :
		print("The search has gone on suspiciously long, aborting search!")
		flag = False
	elif search_history[-1] in search_history[:-1] :
		print("We've arrived at an article we've already seen, aborting search!")
		flag = False
	return flag

def find_first_link(url) :
	html = requests.get(url).text
	soup = BeautifulSoup(html, 'html.parser')

	# This div contains the article's body
    # (June 2017 Note: Body nested in two div tags)
	content_div = soup.find(id="mw-content-text").find(class_="mw-parser-output")

	# stores the first link found in the article, if the article contains no
    # links this value will remain None
	first_relative_link = None

	# Find all the direct children of content_div that are paragraphs
	for element in content_div.find_all('p', recursive=False):
		# Find the first anchor tag that's a direct child of a paragraph.
        # It's important to only look at direct children, because other types
        # of link, e.g. footnotes and pronunciation, could come before the
        # first link to an article. Those other link types aren't direct
        # children though, they're in divs of various classes.
		if element.find('a', recursive=False):
			first_relative_link = element.find('a', recursive=False).get('href')
			break;

	if not first_relative_link:
		return

	# Build a full url from the relative article_link url
	first_relative_link = urljoin('https://en.wikipedia.org/', first_relative_link)

	return first_relative_link


start_url = "https://en.wikipedia.org/wiki/Special:Random"
target_url = "https://en.wikipedia.org/wiki/Philosophy"
article_chain = [start_url]
while continue_crawl(article_chain, target_url) :
	print(article_chain[-1])
	first_link = find_first_link(article_chain[-1])
	if not first_link :
		print("We've arrived at an article with no links, aborting search!")
		break
	article_chain.append(first_link)
	time.sleep(2) # Slow things down so as to not hammer Wikipedia's servers



