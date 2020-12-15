# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 10:41:45 2020

@author: User
"""
import datetime
import mysql.connector
import pycep_correios
from geopy.geocoders import Nominatim
from geopy.distance import geodesic



class Podcasts() :
    def __init__(self, data_lancamento, duracao, autor):
        self.data_lancamento = data_lancamento
        self.duracao = duracao
        self.autor = autor

    def pesquisa_episodio(self) :
        """ Realiza uma query no banco de dados baseado na duração, data de lançamento e autores """
        
        cnx = mysql.connector.connect(user='root', password='gabriel2011',host='127.0.0.1',database='aplicativo')
        cursor = cnx.cursor()
        lst_colunas = ["id", "url","name","tipo","duracao","url_audio","ativo","descricao","data_lancamento","autores", "imagens"]
        l_json = []
        if self.autor == "Todos" :
            cursor.execute(f'select * from `aplicativo`.`podcasts` where (`data_lancamento` BETWEEN DATE_SUB(NOW(), INTERVAL {self.data_lancamento} DAY)  AND NOW()) and `duracao`< {self.duracao} * 60000')
            result = cursor.fetchall()
        else :
            cursor.execute(f'select * from `aplicativo`.`podcasts` where (`data_lancamento` BETWEEN DATE_SUB(NOW(), INTERVAL {self.data_lancamento} DAY)  AND NOW()) and `duracao`< {self.duracao} * 60000 and `autores` = "{self.autor}"')
            result = cursor.fetchall()
        for episode in result :
                dic = {}
                for j in range(len(episode)) : 
                    # Evitando erros no json
                    if lst_colunas[j] == "duracao" :
                        duracao_corrigida = int(episode[j])/60000
                        dic[lst_colunas[j]] = f'{duracao_corrigida}' + ' ' + 'minutos'
                    elif lst_colunas[j] == "data_lancamento":
                        diference = abs(episode[j] - datetime.date.today()).days
                        dic[lst_colunas[j]] = diference
                    else :
                        dic[lst_colunas[j]] = episode[j]
                l_json = l_json + [dic]
    
        
        l_json = sorted(l_json, key = lambda k : k['data_lancamento'])
        l_json = Podcasts.organiza_data(l_json)
        
        cnx.close()
        
        # Retornando a resposta da consulta
        return l_json  
    def pesquisa_autor(self) : 
        """ Pesquisa os dados como (descrição, foto ..) do podcast baseado no autor """
        cnx = mysql.connector.connect(user='root', password='gabriel2011',host='127.0.0.1',database='aplicativo')
        cursor = cnx.cursor()
        lst_key = ['id','nome','url', 'autor', 'descricao','total_ep','imagem']
        cursor.execute(f'select * from `aplicativo`.`info_podcats` where `nome` = "{self.autor}"')
        result = cursor.fetchall()
        dados_pod = dict()
        for i in range(len(lst_key)) :
            dados_pod[lst_key[i]] = result[0][i]
        dados_pod['Resultado'] = 'True'
        cnx.close()
        return dados_pod
    
    
    def organiza_data(lista) :
        for json in lista :
            if json['data_lancamento'] == 0 :
                json['data_lancamento'] = 'Hoje'     
            elif json['data_lancamento'] == 1:
                json['data_lancamento'] = 'há ' + str(json['data_lancamento']) + ' dia atrás'
            
            else :
                json['data_lancamento'] = 'há ' + str(json['data_lancamento']) + ' dias atrás'
        
        return lista




class Site():
    def __init__(self, data_lancamento, duracao, autor):
        self.data_lancamento = data_lancamento

    def pesquisa_sites(self) :
        cnx = mysql.connector.connect(user='root', password='',host='127.0.0.1',database='aplicativo' )
        cursor = cnx.cursor()
        lst_results = []
        cursor.execute(f'select `url`,`autor` from `aplicativo`.`site` where (`data` BETWEEN DATE_SUB(NOW(), INTERVAL {self.data_lancamento} DAY)  AND NOW())')
        result = cursor.fetchall()
        for x in result :
            lst_results = lst_results + [{"url" :x[0], "autor" : x[1] }]
        cnx.close()
        return lst_results

class OrgaoPublico():
    def __init__(self,cep):
        self.cep = cep
    def pesquisa_orgao(self):
        cnx = mysql.connector.connect(user='root', password='',host='127.0.0.1',database='aplicativo')
        cursor = cnx.cursor()
        categorias = ['Serviços de saúde','Lazer e Cultura', 'Transporte', 'CRAS', 'Bancos', 'Base Comunitária']
        lst_json = []
        endereco = pycep_correios.get_address_from_cep(str(self.cep))
        geolocator = Nominatim(user_agent="gabriel_gomes")
        location = geolocator.geocode(endereco['logradouro']  + ',' + endereco['bairro'] + ',' + endereco['cidade'] + ',' + endereco['uf']  )
        if location == None : 
            location =  geolocator.geocode(endereco['logradouro'] + ',' + endereco['cidade'] )
        tupl_endereco = (location.latitude, location.longitude)
        for categoria in categorias :
            cursor.execute(f'SELECT * FROM `aplicativo`.`orgao_publico` where `categoria` = "{categoria}"')
            json = {}
            result = cursor.fetchall()
            i =0 
            for tupl in result :
                if i ==0 :
                    distance_menor = geodesic(tupl_endereco, (tupl[2], tupl[1]))
                    tpl_menor = 0
                else : 
                    distance = geodesic(tupl_endereco, (tupl[2], tupl[1]))
                    if distance_menor > distance :
                        distance_menor = distance
                        tpl_menor = i
                i = i+1
            json["nome"] = result[tpl_menor][0]
            json["categoria"] = result[tpl_menor][3]
            json["imagem"] = "../assets/imagens/procure/" + str(result[tpl_menor][3]) + ".png"
            json["url_local"] = "https://www.google.com/maps/place/" + f"{result[tpl_menor][0]}"
            json["endereco"] = result[tpl_menor][4]
            json["distancia"] = str(distance_menor)
            endereco1 = result[tpl_menor][4]
            json["rota"] = route(endereco, endereco1 )
            lst_json.append(json)
            print(lst_json)
        cnx.close()
        return lst_json

    def route(self, endereco,endereco1) :
        padrao = "https://www.google.com/maps/dir/"
        rua = endereco['logradouro']
        
        bairro = endereco['bairro']

        cidade = endereco['cidade']
        
        uf = endereco['uf']

        url = padrao + rua + ' ' + bairro + ' '+ cidade + uf + '/' + endereco1
        return url
            
class Sugestao():
    def __init__(self, name,url,tipo,descricao):
        self.name = name
        self.url = url
        self.tipo = tipo
        self.descricao = descricao


    def add_sugestion(self):
        cnx = mysql.connector.connect(user='root', password='',host='127.0.0.1',database='aplicativo')
        cursor = cnx.cursor()
        cursor.execute(f'INSERT INTO `aplicativo`.`sugestoes` (`name`, `url`, `tipo`, `descricao`) VALUES ("{self.name}", "{self.url}", "{self.tipo}", "{self.descricao}")')
        cnx.commit()
        cnx.close()
        return "Adicionado com sucesso"
        
        
        
        
        
        
        
        
    
    
    
    
    
    
    
    
    
    
    