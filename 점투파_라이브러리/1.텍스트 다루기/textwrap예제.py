# textwrap.shorten()은 문자열을 원하는 길이에 맞게 줄여 표시할때 사용하는 함수
import textwrap
import time
print(textwrap.shorten("Life is too short, you need python", width=15))
print()

# 축약표시를 변경할려면 매개변수 placeholder추가하기
print(textwrap.shorten("Life is too short, you need python", width=15, placeholder='...'))
print()

# twxtwrap.wrap()은 긴 문자열을 원하는 길이로 줄 바꿈할 때 사용하는 함수
# 단어 단위로 문자열을 잘라 단어가 끊어지지 않음
# width 길이만큼 자르고 이를 리스트로 반환 --> 출력시에는 join사용
# fill을 사용하면 한번에 할 수 있음

long_text = "Life is too short, you need python" * 10
test = textwrap.wrap(long_text, width=70)
print(test)
print()
print('\n'.join(test))
print()
result = textwrap.fill(long_text, width=70)
print(result)
print(time.time())
print(time.time()+3600)