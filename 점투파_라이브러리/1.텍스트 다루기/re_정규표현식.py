# 만약 여러 줄로 이루어져 있는 글에서 특정한 부분을 바꾸려고 한다면 정규표현식을 사용하자
# 주민번호 뒷자리를 *로 바꾼다고 생각하자

data = """
홍길동의 주민 등록 번호는 900905-1049118 입니다.
그리고 고길동의 주민 등록 번호는 700905-1059119 입니다.
그렇다면 누가 형님일까요?
"""

result = []
for line in data.split("\n"):
    word_result = []
    for word in line.split(" "):
        if len(word) == 14 and word[:6].isdigit() and word[7:].isdigit():
            word = word[:6] + "-" + "*******"
        word_result.append(word)
    result.append(" ".join(word_result))
print("\n".join(result))

# 정규표현식을 사용한다면 간단해진다
import re
# 숫자6자리 + 붙임표(-) + 숫자 7자리 (단, 숫자6자리는 괄호를 이용해 그룹지정)
pat = re.compile("(\d{6})[-]\d{7}")
#g<1>이 정규표현식과 일치하는 문자열 중 첫 번째 그룹을 의미
print(pat.sub("\g<1>-*******", data))