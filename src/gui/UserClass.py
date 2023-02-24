
# _: protected  
# __: private


class User:
  def __init__(self, id, password):
    self.__id = id
    self.__password = password

  def setId(self, id):
    self.__id = id
    
  def setPassword(self, id):
    self.__password = id
    
  def setCon(self, con):
    self.__con = con
      
  def getId(self):
    return self.__id
  
  def getPassword(self):
    return self.__password
  
  def getCon(self):
    return self.__con
      

  
  
