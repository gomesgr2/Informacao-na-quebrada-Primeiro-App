# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 10:24:33 2020

@author: User
"""
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from time_consult import main

app = Flask(__name__)
api = Api(app)
CORS(app)
from views import main
