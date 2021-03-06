from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from pybo.forms import QuestionForm
from pybo.models import Question


@login_required(login_url='common:login')
def question_create(request):
    """
    pybo 질문 등록
    """

    # URL 요청을 POST, GET 요청 방식에 빠라 다르게 처리했다.
    # 질문 등록하기 버튼을 누르면 /pybo/question/create/ 가 GET 방식으로 요청되어 질문 등록 화면이 나타난다.
    # 질문 등록 화면에서 입력값을 채우고 <저장하기> 버튼을 클릭하면 /pybo/question/create/ 가 POST 방식으로 요청되어 데이터가 저장된다.

    if request.method == 'POST':
        # 화면에서 전달받은 데이터로 폼의 값이 채워지도록 객체를 생성했다.(subject, content 값을 가진 객체가 form 에 저장된다.)
        form = QuestionForm(request.POST)
        # form.is_valid 함수는 POST 요청으로 받은 form 이 유효한지 검사한다.
        if form.is_valid():
            # form 으로 Question 모델 데이터를 저장하기 위한 코드이며 commit=False 는 임시 저장을 의미한다 => 실제 데이터는 아직 저장되지 않은 상태를 말한다.
            # 임시 저장을 하는 이유는 폼으로 질문 데이터를 저장할 경우 Question 모델의 create_date 에 값이 설정되지 않아 오류가 발생하기 때문이다.
            # form 에는 subject, content 필드만 존재하고 create_date 필드는 없다.
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    # POST 요청을 제외한 나머지 요청 처리
    else:
        # QuestionForm 은 질문을 등록하기 위해 사용하는 장고의 폼
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:url')
def question_modify(request, question_id):
    """
    pybo 질문 수정
    """
    question = get_object_or_404(Question, pk=question_id)

    # 로그인한 유저와 질문을 등록한 유저가 같지 않을 때
    if request.user != question.author:
        messages.error(request, '수정권환이 없습니다.')
        return redirect('pybo:detail', question_id=question.id)

    # question_form.html 에서 저장하기 버튼이 클릭이 되면 question = get_object_or_404(Question, pk=question_id), request.method == 'POST' 내부 함수가 실행되면서
    # pybo:detail 로 redirect 된다.
    if request.method == "POST":
        # form 에는 QuestioForm 의 필드값들 subject, content 의 값들이 실려서 저장되는데 그 값들은 POST 로 입력받은 값들이다.
        # instance 매개변수에 question 을 지정하면 기존 값을 폼에 채울 수 있다.
        # 그래서 form 에는 기존 값 question + POST 로 입력받은 content, subject 값이 추가된 값이다!!!!!
        form = QuestionForm(request.POST, instance=question)
        print(3)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()
            # question.author = request.user
            question.save()
            print(question.content, question.subject, question.author, question.modify_date, question.create_date)
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = QuestionForm()

    # question/modify/question_id 진입 시 => POST 요청이 아니기 때문에 question=get_object_or_404(Question, pk=question_id), form=QuestionForm() 실행되고
    # context 에 빈 form 이 실려서 pybo/question_form.html 로 렌더가 된다.
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_delete(request, question_id):
    """
    pybo 질문삭제
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')