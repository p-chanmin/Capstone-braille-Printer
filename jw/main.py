from LoginClass import Login
from HomeClass import Home
from CreateUserClass import CreateUser
from UserClass import User

from StateClass import State
import StateClass

import serverFunction

con = serverFunction.getConnect()

while True:
  # 로그인  UI 상태 //  로그인 성공, 회원가입, 둘다 아님
  login = Login(con)
  # 성공인 상황 / 회원가입 해야하는 상황 / 아무것도 아닌 상황
  stateInstance = login.start()
  
  if stateInstance.state == StateClass.State.LOGINOK: # 로그인 성공
    user = User(stateInstance.id, stateInstance.password, con)
    print("로구인 성공")
    home = Home(user)
    home.start()
    break
  elif stateInstance.state== StateClass.State.CREATEUSER: # 회원가입 ㄱㄱ
    creatU = CreateUser(con)
    creatU.start()
  else:
    print("뭔가 잘못됨")
    break 

