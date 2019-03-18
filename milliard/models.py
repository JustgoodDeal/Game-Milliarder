from django.db import models

class Question(models.Model):
    level = models.IntegerField(default=1)
    question_text = models.TextField(max_length=200, unique=True)
    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, related_name = 'variants', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=100)
    def __str__(self):
        return self.choice_text
    
    class Meta:
        unique_together = ('question', 'choice_text')

class CorrectAnswer(models.Model):
    question = models.OneToOneField(Question, related_name = 'correct_answer', on_delete=models.CASCADE)
    correct_answer_text = models.CharField(max_length=100)
    def __str__(self):
        return self.correct_answer_text

class Player(models.Model):
    name = models.CharField(max_length=50)
    count_correct_answers = models.IntegerField(default=0, blank=True)
    money_won = models.IntegerField(default=0, blank=True)
    fifty_fifty = models.IntegerField(default=1, blank=True)
    help_people = models.IntegerField(default=1, blank=True)
    call_friend = models.IntegerField(default=1, blank=True)
    def __str__(self):
        return self.name
    