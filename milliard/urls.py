from django.urls import path
from milliard import views

urlpatterns = [
path('', views.start_page, name = 'start_page_url'),
path('player/', views.PlayerCreator.as_view(), name = 'create_player_url'),
path('<int:player_id>/<int:question_id>/<str:question_text>/', views.QuestionShow.as_view(), name='question_show_url'),
path('<int:player_id>/<int:question_id>/answerdetails/<str:question_text>/', views.AnswerResponder.as_view(), name='answer'),
path('end/<int:player_id>/<int:question_id>/', views.game_over, name = 'game_over_url'),
path('<int:player_id>/win/', views.winner, name = 'winner_url'),
path('<int:player_id>/take_money/', views.takemoney, name = 'take_money_url'),
path('fifty/<int:player_id>/<int:question_id>/<str:question_text>/', views.fifty_fifty, name = 'fifty_fifty_url'),
path('peoplehelp/<int:player_id>/<int:question_id>/<str:question_text>/', views.help_people, name = 'help_people_url'),
path('callfriend/<int:player_id>/<int:question_id>/<str:question_text>/', views.CallFriend.as_view(), name = 'call_friend_url'),
path('friendhelp/<str:friendname>/<int:player_id>/<int:question_id>/<str:question_text>/', views.call_friend_after, name = 'call_friend_after_url'),
]