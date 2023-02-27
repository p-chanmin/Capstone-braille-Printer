import tkinter.messagebox as msgbox
import requests

ENDPOINT = "http://43.200.80.26:3000"

########## createAddr Class ##########

def JoinOk(tmp_email, tmp_password, tmp_name):
  url = f'{ENDPOINT}/api/user/register'

  headers = {}
  email = tmp_email
  password = tmp_password
  name = tmp_name

  data = {"email": email, "password": password, "name": name}

  response = requests.request("POST", url, headers=headers, data=data)

  if response.status_code == 200:
    if response.text == '{"result":"이미 가입된 이메일입니다."}':
      return False
    else:
      return True
  else:
    return False

########## login Class ##########

# 구현 해야됨
def LoginOk(tmp_email, tmp_password):
  url = f'{ENDPOINT}/api/user/login'

  headers = {}
  email = tmp_email
  password = tmp_password
  data = {"email": email, "password": password}
  response = requests.request("POST", url, headers=headers, data=data)

  token = response.text

  if response.status_code == 200:
    if response.text == '{"result":"fail"}':
      return (False, token)
    else:
      return (True, token)
  else:
    return (False, token)

########## Home Class ##########

def get_user_info(user):
  url = f'{ENDPOINT}/api/user'

  token = user.getToken()

  headers = {"token": token}
  data = {}
  response = requests.request("GET", url, headers=headers, params=data)

  u_info= None
  if response.status_code == 200:
    # dict 형태 key{result, id, email, name}
    u_info = response.json()
  return u_info

def user_delete(user):
  url = f'{ENDPOINT}/api/user'

  token = user.getToken()
  headers = {"token":token}
  data={}
  response = requests.request("DELETE", url, headers=headers, params=data)

  if response.status_code == 200:
    return True
  return False

# 구현 해야됨
def isDelteUser(email, password):
  return True

def submit_print_document(user, tmp_title, tmp_page):
  url = f'{ENDPOINT}/api/print'

  token = user.getToken()
  headers = {"token":token}

  title= tmp_title
  page = tmp_page

  data={"title":title, "page":page}
  response = requests.request("POST", url, headers=headers, data=data)

  if response.status_code == 200:
    return True

  return False

def get_print_documents(user):
  url = f'{ENDPOINT}/api/print'

  token = user.getToken()

  headers = {"token": token}
  data = {}

  response = requests.request("GET", url, headers=headers, params=data)

  # history 리스트 안에 [{"title": "test document title","page": 2,"state": "인쇄중","submit_at": "2023-02-23T15:44:04.000Z"}, {"title": "test document title","page": 3,"state":"인쇄중","submit_at": "2023-02-23T15:42:55.000Z"}] 형식으로 저장(튜플들을 저장)

  if response.status_code == 200:
    print(response.json())
    history = response.json()['result']
  return history

def alter_print_document(user, tmp_id, tmp_state):
  url = f'{ENDPOINT}/api/print'

  token = user.getToken()
  headers = {"token":token}

  id = tmp_id
  state= tmp_state
  data={"id":id, "state":state}

  response = requests.request("PUT", url, headers=headers, data=data)
  if response.status_code == 200:
    return True
  return False

def delete_print_document(user, tmp_id):
  url = f'{ENDPOINT}/api/print'

  token = user.getToken()
  headers = {"token":token}

  id = tmp_id
  data={"id":id}

  response = requests.request("DELETE", url, headers=headers, data=data)
  if response.status_code == 200:
    return True
  return False
