# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 10:24:35 2020

@author: User
"""
from flask import request, Blueprint
from flask_restful import Resource
from service import Podcasts, Site, OrgaoPublico, Sugestao
import pycep_correios
from news_app import api

main = Blueprint('main', __name__)

class Podcast(Resource):
    def get (self,name):
        pass
    def post(self):
        # Atribuindo o json recebido no método POST a variável json_data  
        json_data = request.get_json(force = True) 

        # Definindo o Objeto Podcast
        podcast = Podcasts(json_data['data_lancamento'], json_data['duracao'], json_data['autor'])

        # Realiza pesquisa de episódio no banco de dados
        Result = podcast.pesquisa_episodio()
        
        # Verificando se possui autor especifíco
        if json_data['autor'] != "Todos" :
            Autor_dados = podcast.pesquisa_autor()

            return { "Result" :Result,"Autor" :Autor_dados, 'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': 'https://localhost:4200',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'}}
        return  {"Status" : 200,"Result" :Result,"Autor" : {"Resultado" : "False"} }
                     
            
    def delete(self):
        pass

class Sites(Resource):
    def get (self):
        pass
    def post(self):
        json_data = request.get_json(force = True) 

        # Definindo Objeto site
        site = Site(json_data['data_lancamento'])

        # Pesquisando os sites baseado nas datas de lançamento
        Result = site.pesquisa_site()



        return {'statusCode': 200,
                    "Result" :
                     Result,    'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': 'https://localhost:4200',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'}
                     } 
    def delete(self):
        pass


    

class Sugestoes(Resource):
    def get (self):
        pass
    def post(self):
        json_data = request.get_json(force = True) 
        name = json_data['name']
        url = json_data['url']
        tipo = json_data['tipo']
        descricao = json_data['descricao']
        sugestao = Sugestao(name, url, tipo,descricao)
        sugestao.add_sugestion()
        return { 'statusCode': 200 , 'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': 'https://localhost:4200',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'} } 
    def delete(self):
        pass




class Localizacao(Resource):
    def get (self):
        pass
    def post(self):
        json_data = request.get_json(force = True) 
        cep = OrgaoPublico(json_data["CEP"])
        Result = cep.pesquisa_orgao()
        if cep == '' : 
            return {
            'statusCode': 200 ,
                    "Result" : [], 
                 "Validacao_CEP" : '','headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': 'https://localhost:4200',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'}
            }
        elif not pycep_correios.validate_cep(cep) :
              return {
            'statusCode': 200 ,
                    "Result" : [],
                    "Validacao_CEP" : 'False' ,
                    'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': 'https://localhost:4200',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'}
            }
        Result = OrgaoPublico.pesquisa_orgao(cep)
        return {
            'statusCode': 200 ,
                    "Result" :
                     Result ,"Validacao_CEP" : 'True' ,'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': 'https://localhost:4200',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'}
            }
    def delete(self):
        pass

api.add_resource(Podcast, '/Podcast')
api.add_resource(Sites, '/Sites')
api.add_resource(Sugestoes, '/Sugestoes')
api.add_resource(Localizacao, '/Localizacao')

