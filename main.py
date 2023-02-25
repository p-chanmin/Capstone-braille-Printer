from src.gui import serverFunction, StateClass
from src.gui.CreateUserClass import CreateUser
from src.gui.HomeClass import Home
from src.gui.LoginClass import Login
from src.gui.UserClass import User
from src.gui.SpecialCharacterUIClass import BrailleCharInfo


while True:
  # 로그인  UI 상태 //  로그인 성공,eInstance.password, con)
  login = Login()
  # 성공인 상황 / 회원가입 해야하는 상황 / 아무것도 아닌 상황
  stateInstance = login.start()

  if stateInstance.state == StateClass.State.LOGINOK: # 로그인 성공
    user = User(stateInstance.id, stateInstance.password)
    home = Home(user)
    
    # homeUI에서 로그아웃을 누르면 다시 if문을 빠져나가서 wile 무한루프로 들어감
    # homeUI에서 회원탈퇴를 누르면 다시 if문을 빠져나가서 wile 무한루프로 들어감
    
    # homeUI에서 종료를 누르면 그 자리에서 프로그램이 종료되서 여기로 안옴
    home.start()
    
  elif stateInstance.state == StateClass.State.CREATEUSER: # 회원가입 ㄱㄱ
    creatU = CreateUser()
    creatU.start()
  else:
    print("뭔가 잘못됨")
    break 

