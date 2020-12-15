# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 11:40:44 2020

@author: User
"""
import robo_spotify
import sites
from threading import Timer,Thread,Event




class perpetualTimer():

   def __init__(self,t,hFunction):
      self.t=t
      self.hFunction = hFunction
      self.thread = Timer(self.t,self.handle_function)

   def handle_function(self):
      self.hFunction()
      self.thread = Timer(self.t,self.handle_function)
      self.thread.start()

   def start(self):
      self.thread.start()

   def cancel(self):
      self.thread.cancel()

def spotify():
    robo_spotify.main()
    
def site() :
    sites.main()
 
def main() :
    t = perpetualTimer(3600,spotify)
    t.start()
    t = perpetualTimer(3600,site)
    t.start()


if __name__ == '__main__' :
    main()