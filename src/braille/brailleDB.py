
# 한글 점자
# 초성
han_cho_dict = {
    'ㄱ': '⠈',
    'ㄲ': '⠠⠈',
    'ㄴ': '⠉',
    'ㄷ': '⠊',
    'ㄸ': '⠠⠊',
    'ㄹ': '⠐',
    'ㅁ': '⠑',
    'ㅂ': '⠘',
    'ㅃ': '⠠⠘',
    'ㅅ': '⠠',
    'ㅆ': '⠠⠠',
    'ㅇ': '⠛',   # 사용되지 않음
    'ㅈ': '⠨',
    'ㅉ': '⠠⠨',
    'ㅊ': '⠰',
    'ㅋ': '⠋',
    'ㅌ': '⠓',
    'ㅍ': '⠙',
    'ㅎ': '⠚',
    '된소리': '⠠',
}
# 중성
han_jung_dict = {
    'ㅏ': '⠣',
    'ㅑ': '⠜',
    'ㅓ': '⠎',
    'ㅕ': '⠱',
    'ㅗ': '⠥',
    'ㅛ': '⠬',
    'ㅜ': '⠍',
    'ㅠ': '⠩',
    'ㅡ': '⠪',
    'ㅣ': '⠕',
    'ㅐ': '⠗',
    'ㅒ': '⠜⠗',
    'ㅔ': '⠝',
    'ㅖ': '⠌',
    'ㅘ': '⠧',
    'ㅙ': '⠧⠗',
    'ㅚ': '⠽',
    'ㅝ': '⠏',
    'ㅞ': '⠏⠗',
    'ㅟ': '⠍⠗',
    'ㅢ': '⠺',
}
# 종성
han_jong_dict = {
    'ㄱ': '⠁',
    'ㄲ': '⠁⠁',
    'ㄴ': '⠒',
    'ㄷ': '⠔',
    'ㄹ': '⠂',
    'ㅁ': '⠢',
    'ㅂ': '⠃',
    'ㅅ': '⠄',
    'ㅆ': '⠌',
    'ㅇ': '⠶',
    'ㅈ': '⠅',
    'ㅊ': '⠆',
    'ㅋ': '⠖',
    'ㅌ': '⠦',
    'ㅍ': '⠲',
    'ㅎ': '⠴',
    'ㄳ': '⠁⠄',
    'ㄵ': '⠒⠅',
    'ㄶ': '⠒⠴',
    'ㄺ': '⠂⠁',
    'ㄻ': '⠂⠢',
    'ㄼ': '⠂⠃',
    'ㄽ': '⠂⠄',
    'ㄾ': '⠂⠦',
    'ㄿ': '⠂⠲',
    'ㅀ': '⠂⠴',
    'ㅄ': '⠃⠄',
}
han_jong_double = ['ㄳ', 'ㄵ', 'ㄶ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅄ', 'ㄲ', 'ㅆ']
han_jong_separate = {
    'ㄳ': ['ㄱ', 'ㅅ'],
    'ㄵ': ['ㄴ', 'ㅈ'],
    'ㄶ': ['ㄴ', 'ㅎ'],
    'ㄺ': ['ㄹ', 'ㄱ'],
    'ㄻ': ['ㄹ', 'ㅁ'],
    'ㄼ': ['ㄹ', 'ㅂ'],
    'ㄽ': ['ㄹ', 'ㅅ'],
    'ㄾ': ['ㄹ', 'ㅌ'],
    'ㄿ': ['ㄹ', 'ㅍ'],
    'ㅀ': ['ㄹ', 'ㅎ'],
    'ㅄ': ['ㅂ', 'ㅅ'],
    'ㄲ': ['ㄱ', 'ㄱ'],
    'ㅆ': ['ㅅ', 'ㅅ'],
}
# 약자
abb_char_dict = {
    'ㄱ': '⠫',
    'ㄲ': '⠠⠫',
    'ㄴ': '⠉',
    'ㄷ': '⠊',
    'ㄸ': '⠠⠊',
    'ㅁ': '⠑',
    'ㅂ': '⠘',
    'ㅃ': '⠠⠘',
    'ㅅ': '⠇',
    'ㅆ': '⠠⠇',
    'ㅇ': '⠣',
    'ㅈ': '⠨',
    'ㅉ': '⠠⠨',
    'ㅋ': '⠋',
    'ㅌ': '⠓',
    'ㅍ': '⠙',
    'ㅎ': '⠚',
    '것': '⠸⠎',
    '껏': '⠠⠸⠎',
    '억': '⠹',
    '언': '⠾',
    '얼': '⠞',
    '연': '⠡',
    '열': '⠳',
    '영': '⠻',
    '옥': '⠭',
    '온': '⠷',
    '옹': '⠿',
    '운': '⠛',
    '울': '⠯',
    '은': '⠵',
    '을': '⠮',
    '인': '⠟',
}
# 약어
abb_word_dict = {
    '그래서': '⠁⠎',
    '그러나': '⠁⠉',
    '그러면': '⠁⠒',
    '그러므로': '⠁⠢',
    '그런데': '⠁⠝',
    '그리고': '⠁⠥',
    '그리하여': '⠁⠱',
}

# 영어 점자
eng_start = '⠴'     # 로마자 시작
eng_end = '⠲'       # 로마자 끝
eng_upper = '⠠'         # 대문자 기호표
eng_word_upper = '⠠⠠'    # 대문자 단어표
eng_str_upper = '⠠⠠⠠'    # 대문자 구절표
eng_end_upper = '⠠⠄'    # 대문자 종료표
eng_dict = {
    'a': '⠁', 'b': '⠃', 'c': '⠉', 'd': '⠙', 'e': '⠑',
    'f': '⠋', 'g': '⠛', 'h': '⠓', 'i': '⠊', 'j': '⠚',
    'k': '⠅', 'l': '⠇', 'm': '⠍', 'n': '⠝', 'o': '⠕',
    'p': '⠏', 'q': '⠟', 'r': '⠗', 's': '⠎', 't': '⠞',
    'u': '⠥', 'v': '⠧', 'w': '⠺', 'x': '⠭', 'y': '⠽',
    'z': '⠵',
    # 대문자는 아래 점자에 대문자 기호표를 붙여 사용함
    'A': '⠁', 'B': '⠃', 'C': '⠉', 'D': '⠙', 'E': '⠑',
    'F': '⠋', 'G': '⠛', 'H': '⠓', 'I': '⠊', 'J': '⠚',
    'K': '⠅', 'L': '⠇', 'M': '⠍', 'N': '⠝', 'O': '⠕',
    'P': '⠏', 'Q': '⠟', 'R': '⠗', 'S': '⠎', 'T': '⠞',
    'U': '⠥', 'V': '⠧', 'W': '⠺', 'X': '⠭', 'Y': '⠽',
    'Z': '⠵',
    
    # 한글 점자의 규정이 없는 특수문자는 로마자로 분류하여 점역함
    '@': '⠈⠁',
    '#': '⠸⠹',
    '^': '⠈⠢',
    '&': '⠈⠯',

    # 로마자 사이에 있는 특수문자는 통일영어점자 규정을 따름
    ',': '⠂',
    ':': '⠒',
    ';': '⠆',
    '~': '⠈⠔',
    '–': '⠠⠤',    # 줄표
    '’': '⠠⠴',  # 닫는 작은 따옴표
    '(': '⠐⠣',
    ')': '⠐⠜',
    '{': '⠸⠣',
    '}': '⠸⠜',
    '[': '⠨⠣',
    ']': '⠨⠜',
    '<': '⠈⠣',
    '>': '⠈⠜',
    '〈': '⠈⠣',
    '〉': '⠈⠜',
    '*': '⠐⠔',

}
# 숫자 점자
num_start = '⠼'     # 수표
num_dict = {
    '0': '⠚', '1': '⠁', '2': '⠃', '3': '⠉', '4': '⠙',
    '5': '⠑', '6': '⠋', '7': '⠛', '8': '⠓', '9': '⠊',
    '+': '⠢', '-': '⠔', '×': '⠡', '÷': '⠌⠌', '=': '⠒⠒',
}

mark_dict = {
    '.': '⠲',
    '?': '⠦',
    '!': '⠖',
    ',': '⠐',
    # ',': '⠂',   # 숫자 쉼표   # mark.py에서 처리
    '·': '⠐⠆',
    ':': '⠐⠂',
    ';': '⠰⠆',
    '/': '⠸⠌',
    '“': '⠦',   # 여는 큰 따옴표
    '”': '⠴',   # 닫는 큰 따옴표
    '‘': '⠠⠦',  # 여는 작은 따옴표
    '’': '⠴⠄',  # 닫는 작은 따옴표
    'ʼ': '⠄',  # 아포스트로피
    '(': '⠦⠄',
    ')': '⠠⠴',
    '{': '⠦⠂',
    '}': '⠐⠴',
    '[': '⠦⠆',
    ']': '⠰⠴',
    '《': '⠰⠦',
    '『': '⠰⠦',
    '》': '⠴⠆',
    '』': '⠴⠆',
    '「': '⠐⠦',
    '」': '⠴⠂',
    '<': '⠐⠦',
    '>': '⠴⠂',
    '〈': '⠐⠦',
    '〉': '⠴⠂',

    '‐': '⠤',   # 붙임표(hyphen)  변환 필요
    '–': '⠤',  # 줄표(dash)  변환 필요
    '―': '⠤⠤',  # 긴 줄표(Horizontal bar)
    '~': '⠤⠤',
    '…': '⠠⠠⠠',

    '*': '⠔⠔',
    '※': '⠔⠔',
    'ː': '⠠⠄',  # 긴 소리표(ː)

    '￦': '⠈⠺',
    '￠': '⠈⠉',
    '$': '⠈⠙',
    '￡': '⠈⠇',
    '￥': '⠈⠽',
    '€': '⠈⠑',

    '+': '⠢',
    '−': '⠔',   # 빼기(minus) 연산기호 변환 필요
    '×': '⠡',
    '÷': '⠌⠌',
    '=': '⠒⠒',
    '±': '⠢⠔',

    '→': '⠒⠕',
    '←': '⠪⠒',
    '↔': '⠪⠒⠕',
    
    # 글머리 기호
    '•': '⠶',
    '○': '⠶',

    # 단위 부호를 적을 때는 로마자기호(단위 표)(⠴)를 적고 시작한다.
    '%': '⠴⠏',  # 퍼센트
    '‰': '⠴⠏⠍',  # 천분율
    '°': '⠴⠙',  # 도
    '′': '⠴⠤',  # 분
    '″': '⠴⠤⠤',  # 초
    'Å': '⠴⠡',  # 옹스트롬

}