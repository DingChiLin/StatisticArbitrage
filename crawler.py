from bs4 import BeautifulSoup
import urllib.request as urllib

url = "http://www.pythonforbeginners.com"

content = urllib.urlopen(url).read()

soup = BeautifulSoup(content)
#print(soup.prettify())
print(soup.title.string)
for a in soup.find_all('a', {'rel':'bookmark'}):
    print(a.text)
