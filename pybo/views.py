from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import timezone

from .models import Question


# Create your views here.

def index(request):
    """
    pybo 출력 목록
    """
    question_list = Question.objects.order_by('-create_date')
    context = {'question_list': question_list}
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    """
    pybo 내용 출력
    """
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)

def answer_create(request, question_id):
    """
    pybo 답변 등록
    """
    question = get_object_or_404(Question, pk=question_id)
    # request.POST.get('content') => POST 형식으로 전송된 form 데이터 항목 중 name 이 content 인 값을 의미한다.
    # Question 모델을 통해 Answer 모델을 생성하기 위해 answer_get.create 를 사용했다.
    question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
    # 이동할 페이지의 별칭, URL에 전달해야 하는 값을 입력
    return redirect('pybo:detail', question_id)
