import tkinter.messagebox as msgbox
import requests

# 서버거랑 유저가 입력한 아이디와 패스워드가 일치하는지
# con: 서버와 연결해주는 커넥터

# 서버와 연결해주는 커넥터 반환
# 구현 해야됨

########## createAddr Class ##########

# 구현 해야됨
def idCheckOk(email):
  url = "localhost:3000/api/user/login"

  payload='email=a%40a.aa&password=1234'
  headers = {}

  response = requests.request("POST", url, headers=headers, data=payload)

  print(response.text)
  if True:
    return True
  else:
    return False

# 구현 해야됨
def JoinOk(email, password, name):
  if True:
    return True
  else:
    return True

########## login Class ##########

# 구현 해야됨
def LoginOk(email, password):
  return True

########## Home Class ##########

def user_delete(user):
  email = user.getEmail
  password = user.getPassword()

  return isDelteUser(email, password)
  # 서버에서 유저를 삭제함

# 구현 해야됨
def isDelteUser(email, password):
  return True

def get_user_history(user):
  email = user.getEmail()

  # history 리스트 안에 [{"title": "test document title","page": 2,"state": "인쇄중","submit_at": "2023-02-23T15:44:04.000Z"}, {"title": "test document title","page": 3,"state":"인쇄중","submit_at": "2023-02-23T15:42:55.000Z"}] 형식으로 저장(튜플들을 저장)
  history=[]
  
  return history
