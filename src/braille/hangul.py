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
    return True if (ord('가') <= ord(letter) and ord(letter) <= ord('힣')) else False
def isSpace(letter):
    return True if letter == ' ' else False

# 한글 음절 분리
def Syllabification(letter, _cho = True, _jung = True, _jong = True):

    if len(letter) > 1:
        print("ERR: Syllabification()은 한글자만 입력 받음")
        return []
    if (not (isHangul(letter) or isSpace(letter))):
        print(f"ERR: <{letter}>은 한글 문자가 아님")
        return []

    syllables = []  # 분리된 음절이 들어갈 리스트
    offset = ord(letter) - ord('가') # index 계산을 위한 offset 설정

    if letter == ' ':   # 공백일 경우
        return [letter]

    # 음절 분리
    ## 초성
    chosung = cho[offset // (len(jung) * len(jong))]
    # 초성의 ㅇ은 생략
    if chosung != "ㅇ": syllables.append(brailleDB.han_cho_dict[chosung])

    ## 중성
    jungsung = jung[(offset // len(jong)) % len(jung)]
    syllables.append(brailleDB.han_jung_dict[jungsung])
    ## 종성
    jongsung = jong[offset % len(jong)] # 종성이 있는지 없는지 확인
    if jongsung is not None: syllables.append(brailleDB.han_jong_dict[jongsung])

    return "".join(syllables)