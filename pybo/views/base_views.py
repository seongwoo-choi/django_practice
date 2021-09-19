from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from pybo.models import Question
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

    # Question 데이터들을 create_date 열의 내림차순으로 정렬하여 조회한다.
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