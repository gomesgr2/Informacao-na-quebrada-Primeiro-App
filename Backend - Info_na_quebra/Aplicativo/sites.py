import requests
from bs4 import BeautifulSoup as bs
import mysql.connector


def arruma_aspas(name) :
    "Transforma todas as aspas duplas em aspas simples"
    new_name = ''
    for char in name :
        if char == '"' :
            char = ''
        new_name = new_name + char
    return new_name
def arruma_data(date) :
    new_date = ''
    lst_date = date.split('-')
    for x in lst_date :
        new_date = x + new_date
    return new_date

def main():
    # url padrão
    url = "http://periferiaemmovimento.com.br/"
    
    # Conexão com o banco de dados MySql
    cnx = mysql.connector.connect(user='root', password='gabriel2011',host='127.0.0.1',database='aplicativo')
    
    # Fazendo uma request 
    r = requests.get(url)
    soup= bs(r.text, "html.parser")
    
    # Adicionando em uma lista os post que estavam na página principal
    lst_url = soup.find_all(class_="ap-item-post")
    
    # Loop em cada url dos posts
    for news in lst_url :
        # Definindo a rota
        route = news.find('a')['href']
        
        # Condição que considera somente as url vindas do site
        if str(route)[0] == '/' :
            
            # Definido a url da page de notícia
            url_route = url+ f'{route}'
            
            # Conferindo se a url já foi adicionada ao banco
            cursor = cnx.cursor()
            cursor.execute(f'select * from `aplicativo`.`site` where `url` = "{url_route}"')
            if cursor.fetchall() == [] :
                
                #Realizando a request na page
                r_2 = requests.get(url_route)
                soup_2 = bs(r_2.text, "html.parser")
                
                #Armazenando os valores que queremos
                titulo = soup_2.find(class_ = "eb-entry-title reset-heading featured-item")
                descricao = soup_2.find(class_ = "entry-introtext")
                data = soup_2.find(class_ = "eb-meta-date")['content']
                autor = soup_2.find(class_ = "eb-meta-author").find('span').find('span')
                
                
            
                
                #Adicionando em um dicionário
                dic =  { "titulo" : titulo, "descricao" : descricao, "autor" : autor}
                
                # Arrumando os valores
                for obj in dic.keys() :
                    if dic[obj] == None :
                        dic[obj] = "Nenhum valor encontrado"
                    else :
                        dic[obj] = dic[obj].get_text()
        
                dic["descricao"]  = arruma_aspas(dic["descricao"])
                data = arruma_data(str(data))
                
            
        
        
                # Adicionando ao banco de dados
                cursor = cnx.cursor()
                cursor.execute(f'INSERT INTO `aplicativo`.`site` (`titulo`, `url`, `autor`,`data`,`descricao`,`tipo`) VALUES("{dic["titulo"]}","{url_route}","{dic["autor"]}","{data}","{dic["descricao"]}","Site");') 
                print('Done')      
    
    cnx.commit()

if __name__ == '__main__':
    main()

        




