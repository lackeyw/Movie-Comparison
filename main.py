import requests
from bs4 import BeautifulSoup

#definitely going to run into problems down the road when it comes to the way imdb sets up their dates

#TODO
#need to handle if they spell something wrong in actor search
#deal with duplicates in search function
#fix search function
#optimize
#create a TV show Object?
#add a gui
#add pictures to gui
#get character names

class Movie:
	def __init__(self, title):
		self.title = title
		self.year = 0

	def get_title(self):
		return self.title
	def get_year(self):
		return self.year

	def set_title(self, title):
		self.title = title
	def set_year(self, year):
		self.year = year
	
	def to_print(self):
		print(self.title.strip('\n') + self.year.strip('\n'))

def clean_date(date_str):
	if date_str == '\n\xa0\n':
		return ' ?'
	else:
		x = date_str.split('/')
		return x[0]

def get_name_link(text_name):
	url = 'https://www.imdb.com/find?q=' + text_name.lower() + '&s=nm&exact=true'
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	nameish = soup.find("td", class_ = 'result_text')
	name_link = nameish.find('a').get('href')
	return name_link

def compare_actors(url_first, url_second):
	first_name = ''
	second_name = ''
	url_part_one = "https://www.imdb.com"
	url = url_part_one + url_first
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	nameish = soup.find('h1', class_ = 'header')
	first_name = nameish.find('span', class_='itemprop').text
	results = soup.find(class_ ='filmo-category-section')
	movie_elems = results.find_all('div', class_="filmo-row")

	first_movies = {}
	second_movies = {}

	for movie_elem in movie_elems:
		if(not("TV Series" in movie_elem.text)):
			title_elem = movie_elem.find('a')
			movie = Movie(title_elem.text)
			date_elem = movie_elem.find('span', class_='year_column')
			movie.set_year(clean_date(date_elem.text))
			first_movies[movie.get_title()] = movie

	url = url_part_one + url_second
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	nameish = soup.find('h1', class_ = 'header')
	second_name = nameish.find('span', class_='itemprop').text
	results = soup.find(class_ ='filmo-category-section')
	movie_elems = results.find_all('div', class_="filmo-row")

	for movie_elem in movie_elems:
		if(not("TV Series" in movie_elem.text)):
			title_elem = movie_elem.find('a')
			movie = Movie(title_elem.text)
			date_elem = movie_elem.find('span', class_='year_column')
			movie.set_year(clean_date(date_elem.text))
			second_movies[movie.get_title()] = movie

	print(first_name + ' and ' + second_name + "\n")

	for i in first_movies.keys():
		if(i in second_movies.keys()):
			first_movies[i].to_print()
	print()

if __name__ == '__main__':

	print("!!!!EXACT NAMES ONLY!!!!!!\n")

	url_this = get_name_link(str(input("First Actor: ")))
	url_that = get_name_link(str(input("Second Actor: ")))
	print()
	compare_actors(url_this, url_that)