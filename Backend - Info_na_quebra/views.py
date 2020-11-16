# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 10:24:35 2020

@author: User
"""
from flask import request
from flask_restful import Resource
from news_app import api
import service


class Podcast(Resource):
    def get (self,name):
        pass
    def post(self):
        json_data = request.get_json(force = True) 
        Result = service.query_mysql_podcast(json_data)
        if json_data['autor'] != "Todos" :
            Autor_dados = service.query_mysql_podcast_autor(json_data['autor'])
            return { "Status" : 200,"Result" :Result,"Autor" :Autor_dados}
        return  {"Status" : 200,"Result" :Result,"Autor" : {"Resultado" : "False"} }
                     
            
    def delete(self):
        pass

class Sites(Resource):
    def get (self):
        pass
    def post(self):
        json_data = request.get_json(force = True) 
        Result = service.query_mysql_sites(json_data)
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
        Result = service.add_sugestion(json_data)
        return { "Status" : 200,
                    "Result" :
                     Result } 
    def delete(self):
        pass




class Localizacao(Resource):
    def get (self):
        pass
    def post(self):
        json_data = request.get_json(force = True) 
        Result = json_data
        return { "Status" : 200,
                    "Result" :
                     Result } 
    def delete(self):
        pass

api.add_resource(Podcast, '/Podcast')
api.add_resource(Sites, '/Sites')
api.add_resource(Sugestoes, '/Sugestoes')
api.add_resource(Localizacao, '/Localizacao')

