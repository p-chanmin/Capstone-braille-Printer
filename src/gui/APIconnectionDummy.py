import requests
import json
ENDPOINT = "http://43.200.80.26:3000"

token = None
tokens = []

  #############회원가입 완료#############

url = f'{ENDPOINT}/api/user/register'
print(url)
headers = {}
email = "a"
password = "a"
name = "a"

data ={"email":email, "password":password, "name":name}

response = requests.request("POST", url, headers=headers, data=data)

if response.status_code == 200:
    print(response.text)
    # result_dict = response.json()
    # print(result_dict)
    # print(result_dict['result'])
else:
    print("nono")





  #############LOGIN 완료#############
url = f'{ENDPOINT}/api/user/login'
print(url)

headers = {}
email = "a"
password = "a"
data ={"email":email, "password":password}
response = requests.request("POST", url, headers=headers, data=data)
print(response, response.text)

token = response.text
tokens.append(token)
print(token[1])


############# 유저정보 불러오기 완료#############

url = f'{ENDPOINT}/api/user'
print(url)

headers = {"token":token}
data={}
response = requests.request("GET", url, headers=headers, params=data)
print(response, response.text)
print(response.json())
print(response.json()['id'])



# ############# 회원 탈퇴 완료#############

# url = f'{ENDPOINT}/api/user'
# print(url)
#
# headers = {"token":token}
# data={}
# response = requests.request("DELETE", url, headers=headers, params=data)
# print(response, response.text)


# # ############# 인쇄 문서 기룩 제출 완료#############

url = f'{ENDPOINT}/api/print'
print(url)

headers = {"token":token}

title="주간 축구"
page = 203

data={"title":title, "page":page}
response = requests.request("POST", url, headers=headers, data=data)
print(response, response.text)

# ############# 인쇄 문서 기록 확인 #############

# url = f'{ENDPOINT}/api/print'
# print(url)
#
# headers = {"token":token}
# data={}
# response = requests.request("GET", url, headers=headers, params=data)
# print(response, response.text)
# print(response.json()['result'])
# print(len(response.json()['result']))


# # ############# 인쇄 문서 기록 상태 변경 확인 #############
#
# url = f'{ENDPOINT}/api/print'
# print(url)
#
# headers = {"token":token}
#
# id =15
# state="인쇄 완료"
#
# data={"id":id, "state":state}
# response = requests.request("PUT", url, headers=headers, data=data)
# print(response, response.text)
#
# # ############# 인쇄 문서 기록 삭제 확인 #############
#
# url = f'{ENDPOINT}/api/print'
# print(url)
#
# headers = {"token":token}
#
# id =15
#
# data={"id":id}
# response = requests.request("DELETE", url, headers=headers, data=data)
# print(response, response.text)