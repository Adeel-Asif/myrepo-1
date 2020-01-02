from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name='home_page'),
  
    path('<int:id>/', views.home,name='home_page'),

    path('signin_request/', views.signin_request, name='signin_request'),
    path('logout_request/', views.logout_request, name='logout_request'),

    path('add_agent/', views.add_agent, name='add_agent_page'),
    path('add_user/', views.add_user,name='add_user_page'),

    path('agents/', views.agents, name='agents_page'),

    path('delete_entry/', views.delete_entry, name='delete_entry'),
    path('agents/delete_agent/', views.delete_agent, name='delete_agent'),

    path('search_home/', views.search_home, name='search_home'),    
    path('agents/search_agent/', views.search_agent, name='search_agent'),
]

#<int:id>/