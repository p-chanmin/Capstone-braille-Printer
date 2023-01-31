import brailleDB

# 초성에 올 수 있는 자음
cho = [
    'ㄱ','ㄲ','ㄴ','ㄷ','ㄸ','ㄹ','ㅁ','ㅂ','ㅃ','ㅅ','ㅆ','ㅇ','ㅈ','ㅉ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ'
]
# 중성에 올 수 있는 모음
jung = [
    'ㅏ','ㅐ','ㅑ','ㅒ','ㅓ','ㅔ','ㅕ','ㅖ','ㅗ','ㅘ','ㅙ','ㅚ','ㅛ','ㅜ','ㅝ','ㅞ','ㅟ','ㅠ','ㅡ','ㅢ','ㅣ'
]
# 종성에 올 수 있는 자음
jong = [
    None, 'ㄱ','ㄲ','ㄳ','ㄴ','ㄵ','ㄶ','ㄷ','ㄹ','ㄺ','ㄻ','ㄼ','ㄽ','ㄾ','ㄿ','ㅀ','ㅁ','ㅂ','ㅄ','ㅅ','ㅆ','ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ'
]

def isHangul(letter):
    """
    입력된 한글 문자 1개가 한글인지 판별
        :param letter: 한글 문자 1개
        :return: 한글이면 true, 아니면 false
    """
    return True if (ord('가') <= ord(letter) and ord(letter) <= ord('힣')) else False

def isSpace(letter):
    """
    입력된 문자가 공백인지 판별
        :param letter: 입력된 문자
        :return: 공백이면 true, 아니면 false
    """
    return True if letter == ' ' else False


# 한글 음절 분리
def Syllabification(letter, _cho = True, _jung = True, _jong = True):
    """
    한글을 음절 분리하고, 약어를 반영하여 점자로 번역
        :param letter: 입력된 한글 문자 1개
        :param _cho: 초성 여부
        :param _jung: 중성 여부
        :param _jong: 종성 여부
        :return: 입력된 한글 문자 1개에 매치되는 점자
    """

    if len(letter) > 1:
        print("ERR: Syllabification()은 한글자만 입력 받음")
        return []
    if (not (isHangul(letter) or isSpace(letter))):
        print(f"ERR: <{letter}>은 한글 문자가 아님")
        return []

    syllables = []  # 분리된 음절이 들어갈 리스트
    tran = [] # 번역된 점자가 들어갈 리스트
    offset = ord(letter) - ord('가') # index 계산을 위한 offset 설정

    if letter == ' ':   # 공백일 경우
        return ' '

    # 음절 분리
    ## 초성
    chosung = cho[offset // (len(jung) * len(jong))]
    syllables.append(chosung)
    ## 중성
    jungsung = jung[(offset // len(jong)) % len(jung)]
    syllables.append(jungsung)
    ## 종성
    jongsung = jong[offset % len(jong)] # 종성이 있는지 없는지 확인
    if jongsung is not None:
        if jongsung in brailleDB.han_jong_double:
            syllables += brailleDB.han_jong_separate[jongsung]
        else:
            syllables.append(jongsung)

    # 초성,중성,종성으로 하는 약자인지 확인 (것)
    if(chosung in "ㄱㄲ" and jungsung == 'ㅓ' and jongsung == "ㅅ"):
        if (chosung == 'ㄱ'): tran.append(brailleDB.abb_char_dict['것'])
        else: tran.append(brailleDB.abb_char_dict['껏'])
        syllables = syllables[3:] # 초성, 중성, 종성 제거, 나머지 있을 수 없음, 빈 리스트
    # 초성과 중성으로 하는 약자인지 확인 (가까나다따마바빠사싸아자짜카타파하)
    elif(jungsung == 'ㅏ' and chosung in "ㄱㄲㄴㄷㄸㅁㅂㅃㅅㅆㅇㅈㅉㅋㅌㅍㅎ"):
        tran.append(brailleDB.abb_char_dict[chosung])
        syllables = syllables[2:]  # 초성, 중성 제거, 나머지 있을 수 있음, 나머지 모두 종성
        for s in syllables:
            tran.append(brailleDB.han_jong_dict[s])
    # 중성과 종성으로 하는 약자인지 확인
    # 억,언,얼
    elif(jungsung == 'ㅓ' and (jongsung is not None) and syllables[2] in "ㄱㄴㄹ"):
        if(chosung != 'ㅇ'): tran.append(brailleDB.han_cho_dict[chosung]) # 초성이 ㅇ이 아니면 먼저 삽입
        if(syllables[2] == 'ㄱ'): tran.append(brailleDB.abb_char_dict['억'])
        elif (syllables[2] == 'ㄴ'): tran.append(brailleDB.abb_char_dict['언'])
        elif (syllables[2] == 'ㄹ'): tran.append(brailleDB.abb_char_dict['얼'])
        syllables = syllables[3:]  # 초성, 중성, 종성 제거, 나머지 있을 수 있음, 나머지 모두 종성
        for s in syllables:
            tran.append(brailleDB.han_jong_dict[s])
    # 연,열,영
    elif(jungsung == 'ㅕ' and (jongsung is not None) and syllables[2] in "ㄴㄹㅇ"):
        if(chosung != 'ㅇ'): tran.append(brailleDB.han_cho_dict[chosung]) # 초성이 ㅇ이 아니면 먼저 삽입
        if (syllables[2] == 'ㄴ'): tran.append(brailleDB.abb_char_dict['연'])
        elif (syllables[2] == 'ㄹ'): tran.append(brailleDB.abb_char_dict['열'])
        elif (syllables[2] == 'ㅇ'): tran.append(brailleDB.abb_char_dict['영'])
        syllables = syllables[3:]  # 초성, 중성, 종성 제거, 나머지 있을 수 있음, 나머지 모두 종성
        for s in syllables:
            tran.append(brailleDB.han_jong_dict[s])
    # 옥,온,옹
    elif(jungsung == 'ㅗ' and (jongsung is not None) and syllables[2] in "ㄱㄴㅇ"):
        if(chosung != 'ㅇ'): tran.append(brailleDB.han_cho_dict[chosung]) # 초성이 ㅇ이 아니면 먼저 삽입
        if (syllables[2] == 'ㄱ'): tran.append(brailleDB.abb_char_dict['옥'])
        elif (syllables[2] == 'ㄴ'): tran.append(brailleDB.abb_char_dict['온'])
        elif (syllables[2] == 'ㅇ'): tran.append(brailleDB.abb_char_dict['옹'])
        syllables = syllables[3:]  # 초성, 중성, 종성 제거, 나머지 있을 수 있음, 나머지 모두 종성
        for s in syllables:
            tran.append(brailleDB.han_jong_dict[s])
    # 운,울
    elif(jungsung == 'ㅜ' and (jongsung is not None) and syllables[2] in "ㄴㄹ"):
        if(chosung != 'ㅇ'): tran.append(brailleDB.han_cho_dict[chosung]) # 초성이 ㅇ이 아니면 먼저 삽입
        if (syllables[2] == 'ㄴ'): tran.append(brailleDB.abb_char_dict['운'])
        elif (syllables[2] == 'ㄹ'): tran.append(brailleDB.abb_char_dict['울'])
        syllables = syllables[3:]  # 초성, 중성, 종성 제거, 나머지 있을 수 있음, 나머지 모두 종성
        for s in syllables:
            tran.append(brailleDB.han_jong_dict[s])
    # 은,을
    elif(jungsung == 'ㅡ' and (jongsung is not None) and syllables[2] in "ㄴㄹ"):
        if(chosung != 'ㅇ'): tran.append(brailleDB.han_cho_dict[chosung]) # 초성이 ㅇ이 아니면 먼저 삽입
        if (syllables[2] == 'ㄴ'): tran.append(brailleDB.abb_char_dict['은'])
        elif (syllables[2] == 'ㄹ'): tran.append(brailleDB.abb_char_dict['을'])
        syllables = syllables[3:]  # 초성, 중성, 종성 제거, 나머지 있을 수 있음, 나머지 모두 종성
        for s in syllables:
            tran.append(brailleDB.han_jong_dict[s])
    # 인
    elif(jungsung == 'ㅣ' and (jongsung is not None) and syllables[2] in "ㄴ"):
        if(chosung != 'ㅇ'): tran.append(brailleDB.han_cho_dict[chosung]) # 초성이 ㅇ이 아니면 먼저 삽입
        if (syllables[2] == 'ㄴ'): tran.append(brailleDB.abb_char_dict['인'])
        syllables = syllables[3:]  # 초성, 중성, 종성 제거, 나머지 있을 수 있음, 나머지 모두 종성
        for s in syllables:
            tran.append(brailleDB.han_jong_dict[s])
    # 약자가 반영이 없는 경우
    else:
        # 초성의 ㅇ은 생략
        if(chosung != 'ㅇ'): tran.append(brailleDB.han_cho_dict[chosung])
        tran.append(brailleDB.han_jung_dict[jungsung])
        # 종성이 있는지 확인
        if jongsung is not None: tran.append(brailleDB.han_jong_dict[jongsung])

    return "".join(tran)