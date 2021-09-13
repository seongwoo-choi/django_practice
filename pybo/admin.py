from django.contrib import admin
from .models import Question
# Register your models here.


# 장고 어드민 검색 기능 추가
class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']

admin.site.register(Question, QuestionAdmin)