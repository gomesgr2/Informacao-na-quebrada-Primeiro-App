# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 18:06:30 2020

@author: User
"""

import requests
import json

json = {"oi": 45}
r = requests.post('http://127.0.0.1:5000/Home', json = json)
print(r.text)