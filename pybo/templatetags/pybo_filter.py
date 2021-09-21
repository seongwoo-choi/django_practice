from django import template
import markdown
from django.utils.safestring import mark_safe

register = template.Library()

# 아래 어노테이션을 적용하면 템플릿에서 해당 함수를 필터로 사용할 수 있게 된다.
@register.filter
def sub(value, arg):
    return value - arg



# mark 함수는 markdown 모듈과 mark_safe 함수를 이용하여 문자열을 HTML 코드로 변환하여 반환한다.
# 이 과정을 거치면 마크다운 문법에 맞도록 HTML 이 만들어진다.
# 그리고 markdown 모듈에 nl2br(줄바꿈 문자), fenced_code(마크다운의 소스 코드 표현) 확장 도구를 설정했다.
# 마크다운 확장 기능은 python-markdown.github.io/extensions/ 에서 확인 가능하다.
@register.filter()
def mark(value):
    extensions = ["nl2br", "fenced_code"]
    return mark_safe(markdown.markdown(value, extensions=extensions))