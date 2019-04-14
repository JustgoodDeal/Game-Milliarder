from django.contrib import admin
from .models import Question, Choice, CorrectAnswer, Player

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4
   
class CorrectAnswerInline(admin.TabularInline):
    model = CorrectAnswer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline, CorrectAnswerInline]
    list_display = ('question_text', 'level')

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'money_won')

admin.site.register(Question, QuestionAdmin)
admin.site.register(Player, PlayerAdmin)
