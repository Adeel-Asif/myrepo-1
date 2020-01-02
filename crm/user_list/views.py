
from django.http import HttpResponse

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm ,AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
import json
from .forms import PostForm, SignUpForm
from django.utils import timezone
from .models import Post

from django.contrib.auth.models import User
from django.db.models import Q
import os
from django.core import serializers
from django.http import JsonResponse

dirpath = os.getcwd()
print("current directory is : " + dirpath)

html_vars={}

with open("user_list/var/html_names.json") as json_file:
	html_vars = json.load(json_file)


def home(request,id=1):
	#print(id)
	if request.user.is_authenticated:

		limit=3
		jump=id*limit
		if (jump-limit<=0):
			number=1
		else:
			number=id-1

		

		start=jump-limit
		end=jump
		#print(start)
		#print(end)
		try:
			if request.user.is_superuser:
				data=Post.objects.filter().order_by('-id')[start:end]
			else:
				data=Post.objects.filter(agent=request.user.id).order_by('-id')[start:end]
		except e:
			print(e)
			if request.user.is_superuser:
				data=Post.objects.filter().order_by('-id')[start-limit:end-limit]
			else:
				data=Post.objects.filter(agent=request.user.id).order_by('-id')[start-limit:end-limit]

			print("asasasas")	

			id=id-1
			number=id-1			

		page_id= {
		'next_id': id+1,
		'pre_id':number
		}	 
		
		print(id+1)
		print(number)

		return render(request,'home.html',{'html_vars':html_vars,'objectlist': data,'page_id':page_id})
	else:
		return redirect('signin_request')
		
def add_user(request):
	if request.user.is_authenticated:

	    if request.method == "POST":
	        form = PostForm(request.POST)
	        if form.is_valid():
	            post = form.save(commit=False)
	            post.agent = request.user
	            post.published_date = timezone.now()
	            post.save()
	            messages.info(request, "User added successfully!")
	            return redirect('add_user_page')
	    else:
	        form = PostForm()
	    return render(request, 'add_user.html', { 'form': form,'html_vars':html_vars})	
	else:
		return redirect('signin_request')
	    
			

def delete_entry(request):
	
	if request.user.is_superuser:

		if request.method == "POST":
			
			employee_id= request.POST['id']
			
			Post.objects.filter(id=employee_id).delete()

			return redirect('/')


def add_agent(request):
	"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'header/signup.html', {'form': form,'html_vars':html_vars,'auth_login':'true'})
	"""
	if request.user.is_authenticated:
		if request.method == 'POST':
			form = SignUpForm(request.POST)
			if form.is_valid():
				user=form.save()
				user.refresh_from_db()  # load the profile instance created by the signal
				user.profile.birth_date = form.cleaned_data.get('birth_date')
				user.profile.number = form.cleaned_data.get('number')
				user.save()
				return redirect('add_agent_page')
		else:
			form = SignUpForm()
		return render(request, 'header/signup.html', {'form': form,'html_vars':html_vars,'auth_login':'true'})


def logout_request(request):
	logout(request)
	messages.info(request, "Logged out successfully!")
	return redirect('/')

def signin_request(request):
	if request.user.is_authenticated:
		return redirect('/')
	if request.method == 'POST':
		form = AuthenticationForm(request=request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, "you are now logged in as {username}")
				return redirect('/')
			else:
				messages.error(request, "Invalid username or password.")
		else:
			messages.error(request, "Invalid username or password.")

	form = AuthenticationForm()
	return render(request = request,template_name = "header/signin.html",context={"form":form,'html_vars':html_vars})


def agents(request):
	if request.user.is_authenticated:
		if request.user.is_superuser:

			context= {
			'title': html_vars['title']
			}
			data=User.objects.filter()

			return render(request,'agents.html',{'html_vars':html_vars,'agent_list': data})

	else:
		return redirect('signin_request')


def delete_agent(request):
	if request.user.is_superuser:

		if request.method == "POST":
			
			agent_id= request.POST['id']
			
			User.objects.filter(id=agent_id).delete()
			print("hello")
			return redirect('agents_page')

def search_home(request):
	
	print("asasasas")
	if request.user.is_authenticated:
	
		print("123456")
		if request.method == "POST":
			
			search_word= request.POST['search_word']
			#print(search_word)
			if search_word=="":
				return
			result=Post.objects.filter(Q(first_name__contains=search_word) | Q(middle_name__contains=search_word) | 
				Q(last_name__contains=search_word)  | Q(customer_email__contains=search_word), 
				agent=request.user.id ).values()
			
			print(result[0]['id'])

			print("found")
			
			return JsonResponse(list(result),safe=False)
			#data = serializers.serialize('json', result)
			
			return HttpResponse(result)
	"""
	if request.user.is_authenticated:
		if request.method == "POST":
			search_word= request.POST['search_word']
			
			data=Post.objects.filter(Q(first_name__contains=search_word) | Q(middle_name=search_word) | 
				Q(last_name=search_word)  | Q(customer_email=search_word) ).values()

			return redirect('/',{'html_vars':html_vars,'objectlist': data})
	"""



def search_agent(request):
	if request.user.is_authenticated:
	
		if request.method == "POST":
			
			search_word= request.POST['search_word']
			
			if search_word=="":
				return
			result=User.objects.filter(Q(first_name__contains=search_word) | Q(username__contains=search_word) | 
				Q(last_name=search_word)  | Q(email__contains=search_word) ).values()
			
			
			return JsonResponse(list(result),safe=False)