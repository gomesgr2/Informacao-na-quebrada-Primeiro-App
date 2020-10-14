import mysql.connector
from flask import Flask, request
from flask_restful import Api, Resource
from flask_cors import CORS
app = Flask(__name__) 
api = Api(app)
CORS(app)
def query_mysql_podcast(json) :
    lst_colunas = ["id", "url","name","tipo","duracao","url_audio","ativo","descricao","data_lancamento"]
    l_json = []
    data_lancamento = json['data_lancamento'] 
    duracao = json['duracao']
    #Conexão ao banco de dados
    cnx = mysql.connector.connect(user='root', password='gabriel2011',host='127.0.0.1',database='aplicativo')
    #Executando a query
    cursor = cnx.cursor()
    cursor.execute(f'select * from `aplicativo`.`podcasts` where (`data_lancamento` BETWEEN DATE_SUB(NOW(), INTERVAL {data_lancamento} DAY)  AND NOW()) and `duracao`< {duracao} * 60000')
    result = cursor.fetchall()
    for episode in result :
        dic = {}
        for j in range(len(episode)) :
            # Evitando erros no json
            if lst_colunas[j] == "duracao" :
                duracao_corrigida = int(episode[j])/60000
                dic[lst_colunas[j]] = f'{duracao_corrigida}' + ' ' + 'minutos'
            elif lst_colunas[j] == "data_lancamento" :
                data = str(episode[j])
                dic[lst_colunas[j]] = data
            else :
                dic[lst_colunas[j]] = episode[j]

       
        l_json = l_json + [dic]
    # Retornando a resposta da consulta
    return l_json  

def query_mysql_sites(json) :
    lst_results = []
    data_lancamento = json['data_lancamento'] 
    #Conexão ao banco de dados
    cnx = mysql.connector.connect(user='root', password='gabriel2011',host='127.0.0.1',database='aplicativo')
    #Executando a query
    cursor = cnx.cursor()
    cursor.execute(f'select `url` from `aplicativo`.`site` where (`data` BETWEEN DATE_SUB(NOW(), INTERVAL {data_lancamento} DAY)  AND NOW())')
    result = cursor.fetchall()
    for x in result :
        lst_results = lst_results + [{"url" :x[0] }]
    return lst_results





class Podcast(Resource):
    def get (self,name):
        pass
    def post(self):
        json_data = request.get_json(force = True) 
        Result = query_mysql_podcast(json_data)
        return { "Status" : 200,
                    "Result" :
                     Result } 
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
                     Result } 
    def delete(self):
        pass


api.add_resource(Podcast, '/Podcast')
api.add_resource(Sites, '/Sites')

if __name__ == '__main__':
    app.run(debug = False)