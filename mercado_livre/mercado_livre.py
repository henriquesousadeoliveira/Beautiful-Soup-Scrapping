import requests
from bs4 import BeautifulSoup
import pandas as pd

# Entrada do URL e nome do produto
url_essence = 'https://lista.mercadolivre.com.br/'
product_name = input('Qual produto você deseja? ')

# Faz o request
response = requests.get(url_essence + product_name)

# Transforma em objeto do BeautifulSoup
site = BeautifulSoup(response.text, 'html.parser')

# Encontra todas as ocorrências do produto
products = site.findAll('div', attrs={'class': 'ui-search-result__wrapper'})

list_products = []

for product in products:
    # Extrai título, link e preço, somente se o produto for encontrado
    title = product.find('h2', attrs={'class': 'ui-search-item__title'})
    link = product.find('a', attrs={'class': 'ui-search-link'})
    real = product.find('span', attrs={'class': 'andes-money-amount__fraction'})
    centavos = product.find('span', attrs={'class': 'andes-money-amount__cents andes-money-amount__cents--superscript-24'})
    
    # Se o título, link e real forem encontrados, adiciona-os à lista
    if title and link and real:
        centavos_text = centavos.text if centavos else '00'
        preco = real.text + ',' + centavos_text
        list_products.append({
            'Título': title.text,
            'Link': link['href'],
            'Preço': preco
        })
    else:
        print("Não foi possível encontrar todas as informações do produto.")

# Se houver produtos, salva-os em um arquivo Excel
if list_products:
    products_dataframe = pd.DataFrame(list_products)
    products_dataframe.to_excel('produtos.xlsx', index=False)
    print("Os produtos foram salvos em 'produtos.xlsx'.")
else:
    print("Nenhum produto encontrado.")

