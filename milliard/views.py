from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import View
from django.http import HttpResponseRedirect
from .models import Question, Choice, Player
from .forms import PlayerForm
import random
import numpy
from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

class PlayerCreator(View):
    def get(self, request):
        form = PlayerForm()
        return render (request, 'milliard/create_player_url.html', context={'form':form})
    def post(self,request):
        bound_form = PlayerForm (request.POST)
        if bound_form.is_valid():
            new_name = bound_form.save()
            question = get_object_or_404 (Question, id=random.choice(Question.objects.filter(level=1)).id)                                                       #####
            return HttpResponseRedirect(reverse('question_show_url', kwargs={'player_id':new_name.id,'question_id':question.id,
            'question_text':question.question_text}))
        return render(request, 'milliard/create_player_url.html', context={'form': bound_form})    

class QuestionShow(View):
    def get(self, request, player_id, question_id, question_text):
        question = get_object_or_404 (Question, id=question_id)
        player = get_object_or_404 (Player, id=player_id)
        money = {1:1, 2:2, 3:3, 4:5, 5:10, 6:20, 7:30, 8:50, 9:75, 10:100, 11:200, 12:300, 13:500, 14:750, 15:1000}
        levels = dict()
        numbers = [i for i in range (15,0,-1)]
        for i in range (1,16):
            if i!=15:
                levels[i] = str (money[i]) + ' млн. долларов'
            else:
                levels[i] = '1 миллиард долларов'
        return render(request, 'milliard/question_show.html', context={'question':question, 'player':player, 'levels':levels, 
        'numbers':numbers, })

class AnswerResponder(View):
    def post(self, request, player_id, question_id, question_text):
        question = get_object_or_404(Question, id=question_id)
        player = get_object_or_404 (Player, id=player_id)
        selected_answer = question.variants.get(id=request.POST['variant'])
        money = {1:1, 2:2, 3:3, 4:5, 5:10, 6:20, 7:30, 8:50, 9:75, 10:100, 11:200, 12:300, 13:500, 14:750, 15:1000}
        if selected_answer.choice_text == question.correct_answer.correct_answer_text:
            player.count_correct_answers += 1
            player.money_won = money[player.count_correct_answers]
            player.save()
            if player.count_correct_answers ==15:
                return HttpResponseRedirect(reverse('winner_url', args=(player.id,)))
            else:
                random.choice(Question.objects.filter(level=1)).id    
                return HttpResponseRedirect(reverse('question_show_url', args=(player.id, 
                random.choice(Question.objects.filter(level=player.count_correct_answers+1)).id, question.question_text)))
        else:
            answers = {1:0, 2:0, 3:0, 4:0, 6:5, 7:5, 8:5, 9:5, 11:10, 12:10, 13:10, 14:10}
            player.count_correct_answers = answers.get(player.count_correct_answers, player.count_correct_answers)
            player.money_won = money.get(player.count_correct_answers, player.count_correct_answers)
            player.save()
            return HttpResponseRedirect(reverse('game_over_url', args=(player.id, question.id)))

def start_page (request):
    return render(request,'milliard/start_page.html')

def game_over (request, player_id, question_id):
    question = get_object_or_404(Question, id=question_id)
    player = get_object_or_404 (Player, id=player_id)
    gamers = list(Player.objects.all().order_by('money_won'))
    gamers = gamers[len(gamers):-6:-1]   
    return render(request,'milliard/game_over_url.html', context={'player':player, 'question':question, 'gamers':gamers})

def winner (request, player_id):
    player = get_object_or_404 (Player, id=player_id)
    gamers = list(Player.objects.all().order_by('money_won'))
    gamers = gamers[len(gamers):-6:-1]  
    return render(request,'milliard/winner_url.html', context={'player':player, 'gamers':gamers})

def takemoney (request, player_id):
    player = get_object_or_404 (Player, id=player_id)
    gamers = list(Player.objects.all().order_by('money_won'))
    gamers = gamers[len(gamers):-6:-1] 
    return render(request,'milliard/take_money_url.html', context={'player':player, 'gamers':gamers})

def fifty_fifty (request, player_id, question_id, question_text):
    question = get_object_or_404(Question, id=question_id)
    two_variants = []
    false_answers = []
    for i in question.variants.all():
        if i.choice_text != question.correct_answer.correct_answer_text:
            false_answers.append(i)
        else:
            true_answer = i
    false_answer = random.choice(false_answers)
    for i in question.variants.all():
        if i == true_answer or i == false_answer:
            two_variants.append (i)
        else:
            two_variants.append ('empty')
    player = get_object_or_404 (Player, id=player_id)
    player.fifty_fifty = 0
    player.save()
    money = {1:1, 2:2, 3:3, 4:5, 5:10, 6:20, 7:30, 8:50, 9:75, 10:100, 11:200, 12:300, 13:500, 14:750, 15:1000}
    levels = dict()
    numbers = [i for i in range (15,0,-1)]
    for i in range (1,16):
        if i!=15:
            levels[i] = str (money[i]) + ' млн. долларов'
        else:
            levels[i] = '1 миллиард долларов'
    return render(request,'milliard/fifty_fifty_url.html', context={'question':question, 'player':player, 'two_variants':two_variants, 
    'levels':levels, 'numbers':numbers, 'true_answer':true_answer, 'false_answer':false_answer})

def help_people (request, player_id, question_id, question_text):
    question = get_object_or_404(Question, id=question_id)
    player = get_object_or_404 (Player, id=player_id)
    player.help_people = 0
    player.save()
    false_answers = []
    for i in question.variants.all():
        if i.choice_text != question.correct_answer.correct_answer_text:
            false_answers.append(i)
        else:
            true_variant = i
    vote_percent = {0:[50,90], 1:[45,85], 2:[40,80], 3:[35,75], 4:[30,70], 5:[20,60], 6:[15,55], 7:[10,50], 8:[10,45],
    9:[10,40], 10:[10,35], 11:[10,30], 12:[10,30], 13:[10,30], 14:[10,30]}
    vote_range = vote_percent[player.count_correct_answers]
    votes = dict()
    votes[true_variant] = random.randint (vote_range[0],vote_range[1])
    avaliable_percents = 100 - votes[true_variant]
    for i in range(3):
        if i != 2:
            votes[false_answers[i]] = random.randint (0,avaliable_percents)
            avaliable_percents = avaliable_percents - votes[false_answers[i]]
        else:
            votes[false_answers[i]] = avaliable_percents
    money = {1:1, 2:2, 3:3, 4:5, 5:10, 6:20, 7:30, 8:50, 9:75, 10:100, 11:200, 12:300, 13:500, 14:750, 15:1000}
    levels = dict()
    numbers = [i for i in range (15,0,-1)]
    for i in range (1,16):
        if i!=15:
            levels[i] = str (money[i]) + ' млн. долларов'
        else:
            levels[i] = '1 миллиард долларов'
    return render(request,'milliard/help_people_url.html', context={'votes': votes, 'question':question, 'player':player,
    'levels':levels, 'numbers':numbers})

class CallFriendCreator(View):
    def get(self, request, player_id, question_id, question_text):
        question = get_object_or_404(Question, id=question_id)
        player = get_object_or_404 (Player, id=player_id)
        player.call_friend = 0
        player.save()
        form = PlayerForm()
        money = {1:1, 2:2, 3:3, 4:5, 5:10, 6:20, 7:30, 8:50, 9:75, 10:100, 11:200, 12:300, 13:500, 14:750, 15:1000}
        levels = dict()
        numbers = [i for i in range (15,0,-1)]
        for i in range (1,16):
            if i!=15:
                levels[i] = str (money[i]) + ' млн. долларов'
            else:
                levels[i] = '1 миллиард долларов'
        return render (request, 'milliard/call_friend_url.html', context={'form':form, 'question':question, 'player':player,
        'levels':levels, 'numbers':numbers})
    def post(self, request, player_id, question_id, question_text):
        question = get_object_or_404(Question, id=question_id)
        player = get_object_or_404 (Player, id=player_id)
        bound_form = PlayerForm (request.POST) 
        money = {1:1, 2:2, 3:3, 4:5, 5:10, 6:20, 7:30, 8:50, 9:75, 10:100, 11:200, 12:300, 13:500, 14:750, 15:1000}
        levels = dict()
        numbers = [i for i in range (15,0,-1)]
        for i in range (1,16):
            if i!=15:
                levels[i] = str (money[i]) + ' млн. долларов'
            else:
                levels[i] = '1 миллиард долларов'       
        if bound_form.is_valid():
            return HttpResponseRedirect(reverse('call_friend_after_url', kwargs={'friendname':bound_form.cleaned_data['name'], 'player_id':player.id,
            'question_id':question.id, 'question_text':question.question_text}))
        return render(request, 'milliard/call_friend_url.html', context={'form': bound_form, 'question':question, 'player':player,
        'levels':levels, 'numbers':numbers})

def call_friend_after(request, friendname, player_id, question_id, question_text):
    question = get_object_or_404(Question, id=question_id)
    player = get_object_or_404 (Player, id=player_id)
    false_answers = []
    for i in question.variants.all():
        if i.choice_text != question.correct_answer.correct_answer_text:
            false_answers.append(i)
        else:
            true_variant = i
    chances_for_answers = {0:0.9, 1:0.8, 2:0.8, 3:0.7, 4:0.7, 5:0.6, 6:0.6, 7:0.5, 8:0.4, 9:0.4, 10:0.3, 11:0.2, 12:0.2, 13:0.1, 14:0.1}
    chance_for_true_answer = chances_for_answers[player.count_correct_answers]
    friend_decision = numpy.random.choice ([true_variant,random.choice(false_answers)],p=[chance_for_true_answer, 1-chance_for_true_answer])
    money = {1:1, 2:2, 3:3, 4:5, 5:10, 6:20, 7:30, 8:50, 9:75, 10:100, 11:200, 12:300, 13:500, 14:750, 15:1000}
    levels = dict()
    numbers = [i for i in range (15,0,-1)]
    for i in range (1,16):
        if i!=15:
            levels[i] = str (money[i]) + ' млн. долларов'
        else:
            levels[i] = '1 миллиард долларов'    
    return render(request,'milliard/call_friend_after_url.html', context={'friend_decision':friend_decision,'question':question,
    'player':player, 'friendname':friendname, 'levels':levels, 'numbers':numbers})

def fifty_help_people (request, player_id, question_id, question_text, true_answer_id, false_answer_id):
    question = get_object_or_404(Question, id=question_id)
    player = get_object_or_404 (Player, id=player_id)
    player.help_people = 0
    player.save()
    true_answer = get_object_or_404 (Choice, id=true_answer_id)
    false_answer = get_object_or_404 (Choice, id=false_answer_id)
    vote_percent = {0:[40,100], 1:[40,95], 2:[40,90], 3:[35,85], 4:[30,80], 5:[20,70], 6:[15,65], 7:[10,60], 8:[10,55],
    9:[10,50], 10:[10,45], 11:[10,40], 12:[10,40], 13:[10,40], 14:[10,40]}
    vote_range = vote_percent[player.count_correct_answers]
    votes = dict()
    votes[true_answer] = random.randint (vote_range[0],vote_range[1])
    votes[false_answer] = 100 - votes[true_answer]
    money = {1:1, 2:2, 3:3, 4:5, 5:10, 6:20, 7:30, 8:50, 9:75, 10:100, 11:200, 12:300, 13:500, 14:750, 15:1000}
    levels = dict()
    numbers = [i for i in range (15,0,-1)]
    for i in range (1,16):
        if i!=15:
            levels[i] = str (money[i]) + ' млн. долларов'
        else:
            levels[i] = '1 миллиард долларов'
    return render(request,'milliard/fifty_help_people.html', context={'votes': votes, 'question':question, 'player':player,
    'levels':levels, 'numbers':numbers, 'true_answer':true_answer, 'false_answer':false_answer})

class fifty_CallFriendCreator(View):
    def get(self, request, player_id, question_id, question_text, true_answer_id, false_answer_id):
        question = get_object_or_404(Question, id=question_id)
        true_answer = get_object_or_404 (Choice, id=true_answer_id)
        false_answer = get_object_or_404 (Choice, id=false_answer_id)
        player = get_object_or_404 (Player, id=player_id)
        player.call_friend = 0
        player.save()
        form = PlayerForm()
        money = {1:1, 2:2, 3:3, 4:5, 5:10, 6:20, 7:30, 8:50, 9:75, 10:100, 11:200, 12:300, 13:500, 14:750, 15:1000}
        levels = dict()
        numbers = [i for i in range (15,0,-1)]
        for i in range (1,16):
            if i!=15:
                levels[i] = str (money[i]) + ' млн. долларов'
            else:
                levels[i] = '1 миллиард долларов'
        return render (request, 'milliard/fifty_call_friend.html', context={'form':form, 'question':question, 'player':player,
        'levels':levels, 'numbers':numbers, 'true_answer':true_answer, 'false_answer':false_answer})
    def post(self, request, player_id, question_id, question_text, true_answer_id, false_answer_id):
        question = get_object_or_404(Question, id=question_id)
        true_answer = get_object_or_404 (Choice, id=true_answer_id)
        false_answer = get_object_or_404 (Choice, id=false_answer_id)
        player = get_object_or_404 (Player, id=player_id)
        bound_form = PlayerForm (request.POST) 
        money = {1:1, 2:2, 3:3, 4:5, 5:10, 6:20, 7:30, 8:50, 9:75, 10:100, 11:200, 12:300, 13:500, 14:750, 15:1000}
        levels = dict()
        numbers = [i for i in range (15,0,-1)]
        for i in range (1,16):
            if i!=15:
                levels[i] = str (money[i]) + ' млн. долларов'
            else:
                levels[i] = '1 миллиард долларов'       
        if bound_form.is_valid():
            return HttpResponseRedirect(reverse('fifty_call_friend_after_url', kwargs={'friendname':bound_form.cleaned_data['name'], 'player_id':player.id,
            'question_id':question.id, 'question_text':question.question_text, 'true_answer_id':true_answer.id, 'false_answer_id':false_answer.id}))
        return render(request, 'milliard/fifty_call_friend.html', context={'form': bound_form, 'question':question, 'player':player,
        'levels':levels, 'numbers':numbers, 'true_answer':true_answer, 'false_answer':false_answer})

def fifty_call_friend_after(request, friendname, player_id, question_id, question_text, true_answer_id, false_answer_id):
    question = get_object_or_404(Question, id=question_id)
    player = get_object_or_404 (Player, id=player_id)
    true_answer = get_object_or_404 (Choice, id=true_answer_id)
    false_answer = get_object_or_404 (Choice, id=false_answer_id)
    answers = dict()
    answers[true_answer] = true_answer.choice_text
    answers[false_answer] = false_answer.choice_text
    chances_for_answers = {0:0.9, 1:0.8, 2:0.8, 3:0.7, 4:0.7, 5:0.6, 6:0.6, 7:0.5, 8:0.4, 9:0.4, 10:0.4, 11:0.4, 12:0.4, 13:0.4, 14:0.4}
    chance_for_true_answer = chances_for_answers[player.count_correct_answers]
    friend_decision = numpy.random.choice ([true_answer, false_answer],p=[chance_for_true_answer, 1-chance_for_true_answer])
    money = {1:1, 2:2, 3:3, 4:5, 5:10, 6:20, 7:30, 8:50, 9:75, 10:100, 11:200, 12:300, 13:500, 14:750, 15:1000}
    levels = dict()
    numbers = [i for i in range (15,0,-1)]
    for i in range (1,16):
        if i!=15:
            levels[i] = str (money[i]) + ' млн. долларов'
        else:
            levels[i] = '1 миллиард долларов'    
    return render(request,'milliard/fifty_call_friend_after.html', context={'friend_decision':friend_decision,'question':question,
    'player':player, 'friendname':friendname, 'levels':levels, 'numbers':numbers, 'true_answer':true_answer, 'false_answer':false_answer,
    'answers':answers})

