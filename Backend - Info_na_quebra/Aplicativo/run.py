# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 10:32:16 2020

@author: User
"""

from news_app import app 
from waitress import serve

app.run(debug = True)