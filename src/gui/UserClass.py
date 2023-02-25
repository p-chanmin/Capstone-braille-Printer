
# _: protected  
# __: private


class User:
  def __init__(self, email, password):
    self.__email = email
    self.__password = password

  def setEmail(self, email):
    self.__email = email
    
  def setPassword(self, id):
    self.__password = id
      
  def getEmail(self):
    return self.__email
  
  def getPassword(self):
    return self.__password


  
  
