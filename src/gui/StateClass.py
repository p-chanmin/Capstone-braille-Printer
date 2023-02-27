class State:
  LOGINOK = 1010
  CREATEUSER = 2020
  OTHER = 3030
  
  def __init__(self, state, token = None, id=None, password=None):
    self.state = state
    self.token = token
    self.id = id
    self.password = password
  