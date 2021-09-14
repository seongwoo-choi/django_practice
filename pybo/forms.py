from django import forms
from pybo.models import Question, Answer


# 모델 폼을 생성 => 말 그대로 모델과 연결된 폼이며, 모델 폼 객체를 저장하면 연결된 모델의 데이터를 저장할 수 있다.
# 장고 모델 폼은 내부 클래스로 반드시 Meta 클래스를 가져야 한다!
class QuestionForm(forms.ModelForm):
    # Meta 클래스에는 모델 폼이 사용할 모델과 모델의 필드들을 적어야 한다.
    class Meta:
        model = Question
        fields = ['subject', 'content']
        # widgets 속성을 이용하면 필드에 클래스 네임을 붙여줄 수 있다.
        # widgets = {
        #     'subject': forms.TextInput(attrs={'class': 'form-control'}),
        #     'content': forms.Textarea(attrs={'class': 'form-control', 'rows': '10'})
        # }
        # field 에 입력된 값을 한글로 바꾸기 위해 labels 속성을 사용했다.
        labels = {
            'subject': '제목',
            'content': '내용',
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content': '답변내용',
        }