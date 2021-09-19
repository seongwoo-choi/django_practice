from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from pybo.forms import AnswerForm
from pybo.models import Question, Answer


# 아래 어노테이션을 통해 로그인이 되어 있는지를 우선 검사하여 오류를 방지한다.
# 만약 로그아웃 상태에서 @login_required 어노테이션이 적용된 함수가 호출되면 자동으로 로그인 화면으로 이동하게 했다.
@login_required(login_url='common:login')
def answer_create(request, question_id):
    """
    pybo 답변 등록
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            # 이동할 페이지의 별칭, URL에 전달해야 하는 값을 입력
            return redirect('pybo:detail', question_id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)

    # request.POST.get('content') => POST 형식으로 전송된 form 데이터 항목 중 name 이 content 인 값을 의미한다.
    # Question 모델을 통해 Answer 모델을 생성하기 위해 answer_get.create 를 사용했다.
    # question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())


@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    """
    pybo 답변 수정
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, "수정 권한이 없습니다.")
        return redirect('pybo:detail', question_id=answer.question.id)

    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('pybo:detail', question_id=answer.question.id)

    else:
        form = AnswerForm()
    context = {"answer": answer, "form": form}
    return render(request, 'pybo/answer_form.html', context)


@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    """
    pybo 답변 삭제
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다.')
    else:
        answer.delete()
    return redirect('pybo:detail', question_id=answer.question.id)