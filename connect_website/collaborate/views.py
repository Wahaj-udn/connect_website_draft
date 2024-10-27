from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, IdeaForm, UserProfileForm
from .models import Idea, UserProfile


def home(request):
    return render(request, 'collaborate/index.html')


@login_required
def collaborate(request):
    ideas = Idea.objects.all()
    filter_keyword = request.GET.get('filter', '')

    if filter_keyword:
        ideas = ideas.filter(title__icontains=filter_keyword)

    if request.method == 'POST':
        form = IdeaForm(request.POST, request.FILES)
        if form.is_valid():
            idea = form.save(commit=False)
            idea.user = request.user
            idea.save()
            return redirect('collaborate')
    else:
        form = IdeaForm()

    return render(request, 'collaborate/collaborate.html', {
        'form': form,
        'ideas': ideas,
        'filter': filter_keyword
    })


@login_required
def share_idea(request):
    if request.method == 'POST':
        form = IdeaForm(request.POST, request.FILES)
        if form.is_valid():
            idea = form.save(commit=False)  # Create an Idea object but don't save to the database yet
            idea.user = request.user  # Assign the currently logged-in user
            idea.save()  # Now save it
            return redirect('contribute')  # Redirect to your contribution page or success page
    else:
        form = IdeaForm()

    return render(request, 'collaborate\idea.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('collaborate')
        else:
            messages.error(request, "Registration failed. Please try again.")
    else:
        form = UserRegistrationForm()
    return render(request, 'collaborate/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('collaborate')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'collaborate/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def profile(request):
    profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'collaborate/profile.html', {'form': form})


@login_required
def contribute(request):
    ideas = Idea.objects.all()
    return render(request, 'collaborate/contribute.html', {'ideas': ideas})


def projects(request):
    return render(request, 'collaborate/projects.html')


def placeholder_view(request):
    return HttpResponse("<h1>Page Coming Soon!</h1>")


def thankyou(request):
    return render(request, 'collaborate/thankyou.html')
