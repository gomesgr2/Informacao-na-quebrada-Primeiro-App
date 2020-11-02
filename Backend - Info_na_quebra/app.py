import mysql.connector
from flask import Flask, request
from flask_restful import Api, Resource
from flask_cors import CORS
import robo_spotify
import sites
import datetime
app = Flask(__name__) 
api = Api(app)
CORS(app)
robo_spotify.main()
sites.main()


def organiza_data(lista) :
    for json in lista :
        if json['data_lancamento'] == 0 :
            json['data_lancamento'] = 'Hoje'     
        elif json['data_lancamento'] == 1:
            json['data_lancamento'] = 'há ' + str(json['data_lancamento']) + ' dia atrás'
           
        else :
            json['data_lancamento'] = 'há ' + str(json['data_lancamento']) + ' dias atrás'
        
            
            
    
    return lista


def query_mysql_podcast(json) :
    lst_colunas = ["id", "url","name","tipo","duracao","url_audio","ativo","descricao","data_lancamento","autores", "imagens"]
    l_json = []
    data_lancamento = json['data_lancamento'] 
    duracao = json['duracao']
    autor = json['autor']
    print(autor)
    #Conexão ao banco de dados
    cnx = mysql.connector.connect(user='root', password='gabriel2011',host='127.0.0.1',database='aplicativo')
    #Executando a query
    cursor = cnx.cursor()
    if autor == "Todos" :
        cursor.execute(f'select * from `aplicativo`.`podcasts` where (`data_lancamento` BETWEEN DATE_SUB(NOW(), INTERVAL {data_lancamento} DAY)  AND NOW()) and `duracao`< {duracao} * 60000')
        result = cursor.fetchall()
    else :
        cursor.execute(f'select * from `aplicativo`.`podcasts` where (`data_lancamento` BETWEEN DATE_SUB(NOW(), INTERVAL {data_lancamento} DAY)  AND NOW()) and `duracao`< {duracao} * 60000 and `autores` = "{autor}"')
        result = cursor.fetchall()
    for episode in result :
            dic = {}
            for j in range(len(episode)) : 
                # Evitando erros no json
                if lst_colunas[j] == "duracao" :
                    duracao_corrigida = int(episode[j])/60000
                    dic[lst_colunas[j]] = f'{duracao_corrigida}' + ' ' + 'minutos'
                elif lst_colunas[j] == "data_lancamento" :
                    diference = abs(episode[j] - datetime.date.today()).days
                    dic[lst_colunas[j]] = diference
                else :
                    dic[lst_colunas[j]] = episode[j]
            l_json = l_json + [dic]
   
    
    l_json = sorted(l_json, key = lambda k : k['data_lancamento'])
    l_json = organiza_data(l_json)
    
    # Retornando a resposta da consulta
    return l_json  
def query_mysql_sites(json) :
    lst_results = []
    data_lancamento = json['data_lancamento'] 
    #Conexão ao banco de dados
    cnx = mysql.connector.connect(user='root', password='gabriel2011',host='127.0.0.1',database='aplicativo')
    #Executando a query
    cursor = cnx.cursor()
    cursor.execute(f'select `url`,`autor` from `aplicativo`.`site` where (`data` BETWEEN DATE_SUB(NOW(), INTERVAL {data_lancamento} DAY)  AND NOW())')
    result = cursor.fetchall()
    for x in result :
        lst_results = lst_results + [{"url" :x[0], "autor" : x[1] }]
    return lst_results


def add_sugestion(json):
    "Adiciona sugestão de veículos de noticias em uma tabela mysql"
    name = json['name']
    url = json['url']
    tipo = json['tipo']
    descricao = json['descricao']
    cnx = mysql.connector.connect(user='root', password='gabriel2011',host='127.0.0.1',database='aplicativo')
    cursor = cnx.cursor()
    cursor.execute(f'INSERT INTO `aplicativo`.`sugestoes` (`name`, `url`, `tipo`, `descricao`) VALUES ("{name}", "{url}", "{tipo}", "{descricao}")')
    cnx.commit()
    return "Adicionado com sucesso"

def query_mysql_podcast_autor(autor) :        
    lst_key = ['id','nome','url', 'autor', 'descricao','total_ep','imagem']
    cnx = mysql.connector.connect(user='root', password='gabriel2011',host='127.0.0.1',database='aplicativo')
    cursor = cnx.cursor()
    cursor.execute(f'select * from `aplicativo`.`info_podcats` where `nome` = "{autor}"')
    result = cursor.fetchall()
    print(result)
    dados_pod = dict()
    for i in range(len(lst_key)) :
        dados_pod[lst_key[i]] = result[0][i]
    dados_pod['Resultado'] = 'True'
    return dados_pod
    

class Podcast(Resource):
    def get (self,name):
        pass
    def post(self):
        json_data = request.get_json(force = True) 
        Result = query_mysql_podcast(json_data)
        if json_data['autor'] != "Todos" :
            Autor_dados = query_mysql_podcast_autor(json_data['autor'])
            return { "Status" : 200,"Result" :Result,"Autor" :Autor_dados}
        return  {"Status" : 200,"Result" :Result,"Autor" : {"Resultado" : "False"} }
                     
            
    def delete(self):
        pass

class Sites(Resource):
    def get (self):
        pass
    def post(self):
        json_data = request.get_json(force = True) 
        Result = query_mysql_sites(json_data)
        return { "Status" : 200,
                    "Result" :
                     Result, 
                     } 
    def delete(self):
        pass


    

class Sugestoes(Resource):
    def get (self):
        pass
    def post(self):
        json_data = request.get_json(force = True) 
        Result = add_sugestion(json_data)
        return { "Status" : 200,
                    "Result" :
                     Result } 
    def delete(self):
        pass




api.add_resource(Podcast, '/Podcast')
api.add_resource(Sites, '/Sites')
api.add_resource(Sugestoes, '/Sugestoes')


if __name__ == '__main__':
    app.run(debug = False)