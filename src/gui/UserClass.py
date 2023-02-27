
# _: protected  
# __: private


class User:
  def __init__(self, token, email, password):
    self.__email = email
    self.__password = password
    self.__token = token
  def setEmail(self, email):
    self.__email = email
    
  def setPassword(self, id):
    self.__password = id

  def setToken(self, token):
    self.__token = token

  def getEmail(self):
    return self.__email
  
  def getPassword(self):
    return self.__password

  def getToken(self):
    return self.__token
  
  
