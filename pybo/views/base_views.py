from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404

from pybo.models import Question

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
    kw = request.GET.get('kw', '')
    so = request.GET.get('so', 'recent')


    # annotate 함수를 사용하면 임시로 필드를 추가해 줄 수 있다.
    # 그래서 num_voter 라는 필드를 속성으로 추가해 준 것이다.
    if so == 'recommend':
        question_list = Question.objects.annotate(
            num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = Question.objects.annotate(
            num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:
        question_list = Question.objects.order_by('-create_date')


    # Question 데이터들을 create_date 열의 내림차순으로 정렬하여 조회한다.
    # question_list = Question.objects.order_by('-create_date')

    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |
            Q(content__icontains=kw) |
            Q(author__username__icontains=kw) |
            Q(answer__author__username__icontains=kw)
        ).distinct()


    # 페이징 처리
    # 페이지당 10개 씩 보여주기
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj, 'page': page, 'kw': kw}

    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    """
    pybo 내용 출력
    """
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)