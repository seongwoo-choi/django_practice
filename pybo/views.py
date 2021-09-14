from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import timezone
from .forms import QuestionForm, AnswerForm
from .models import Question
import logging

# 로그 생성
logger = logging.getLogger()

# 로그의 출력 기준 설정
logger.setLevel(logging.INFO)

# log 출력 형식
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# log 출력
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# log를 파일에 출력
file_handler = logging.FileHandler('my.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


# Create your views here.

def index(request):
    """
    pybo 출력 목록
    """

    # 입력 인자
    # request.GET('page', '1') => page 파라미터가 없는 URL 을 위해 기본값으로 1을 지정
    # localhost:8000/pybo/?page=1, page=1 인 값을 page 에 저장
    # 페이지 초기값을 설정해주는 것
    page = request.GET.get('page', '1')

    # 조회
    question_list = Question.objects.order_by('-create_date')

    # 페이징 처리
    # 페이지당 10개 씩 보여주기
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj}

    logger.info(page)
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
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
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
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    # POST 요청을 제외한 나머지 요청 처리
    else:
        # QuestionForm 은 질문을 등록하기 위해 사용하는 장고의 폼
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


