import requests
from bs4 import BeautifulSoup
import pandas as pd 

list_notices =[]

response = requests.get('https://g1.globo.com/')

content = response.content

site = BeautifulSoup(content,'html.parser')

#HTML da notícia

notices = site.findAll('div',attrs={'class': 'feed-post-body'})

for notice in notices:
    #Titulo
    title = notice.find('a', attrs={'class': 'feed-post-link'})
    #Tempo de postagem
    post_time = notice.find('div', attrs={'class': 'feed-post-metadata'})
    list_notices.append([title.text, title['href'],post_time.text])
news = pd.DataFrame(list_notices, columns=['Título','Link','Tempo de postagem'])