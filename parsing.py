import csv
from bs4 import BeautifulSoup
import requests
import time

link = 'https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie'

def parse(url):
	try:
		source = requests.get(url).text
	except:
		return

	soup = BeautifulSoup(source, "lxml")

	links = soup.find_all('a', class_='mzr-tc-group-item-href')


	formatted_links = []
	for link in links:
		link_href = link.get('href')
		link_href = 'https://health-diet.ru' + link_href
		formatted_links.append(link_href)
		title = link.text

		src = requests.get(link_href).text
		soup = BeautifulSoup(src, "lxml")
		info = soup.find('table').find_all('tr')

		with open(f'data/{title}.csv', 'w') as file:
			writer = csv.writer(file, lineterminator="\n")
			for item in info:
				try:
					name = item.find_all('td')[0].text
					calories = item.find_all('td')[1].text
					proteins = item.find_all('td')[2].text
					fats = item.find_all('td')[3].text
					carbohydrates = item.find_all('td')[4].text
					writer.writerow((name, 'калории:' + calories, 'белки:' + proteins, 'жиры:' + fats, 'углеводы:' + carbohydrates))
				except:
					time.sleep(3)
					print(f'файл {title} скопирован!')
					pass

def main():
	parse(link)

if __name__ == "__main__":
	main()
