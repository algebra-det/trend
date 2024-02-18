from django.shortcuts import render, redirect
from django.contrib import messages

from core.models import Reward, Privacy, Conditions, Credits
from account.models import MyUser
from product.models import Product
from game.models import Game, Challenge

from core.forms import RewardForm, CustomPasswordResetForm, PrivacyForm, ConditionsForm, CreditsForm

from django.contrib.auth import authenticate, login, logout

from trend.decorators import admin_only

import geocoder
from .haversine import distance

def loginview(request):
    if request.POST:
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None and user.is_admin:
            login(request, user)
            return redirect('core:index')
        else:
            messages.error(request, f"Le credenziali non corrispondono a nessun utente!")
            return redirect('core:login')
    return render(request, 'core/login.html')


def logoutview(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('core:login')

def nearest_location(request):
    users = MyUser.objects.all()[:5]
    products = Product.objects.all().order_by('-basket')[:5]
    game = Game.objects.all().first()
    d_lat = float(game.location_latitude)
    d_lon = float(game.location_longitude)
    print(d_lat, d_lon)
    print('***********************************************')
    ip = request.META.get('REMOTE_ADDR')
    g = geocoder.ip('45.115.253.178')
    s_lat = g.latlng[0]
    s_lon = g.latlng[1]
    print(s_lat, s_lon)

    # Calculating distance using Haversine 
    dis = distance(d_lat, d_lon, s_lat, s_lon)
    print(dis)

    context = {
        'users': users,
        'products': products
    }
    return render(request, 'core/index.html', context)


@admin_only
def index(request):
    users = MyUser.objects.filter(is_admin=False).count()
    games = Game.objects.all().count()
    challenges = Challenge.objects.all().count()
    reward = Reward.objects.all()
    if reward:
        reward = reward.first()
    else:
        reward = Reward.objects.create(welcome=100, per_post=5)

    context = {
        'users': users,
        'games': games,
        'challenges': challenges,
        'reward': reward
    }
    return render(request, 'core/dashboard.html', context)


def reward(request):
    reward = Reward.objects.all().first()
    if request.POST:
        form = RewardForm(request.POST, instance=reward)
        if form.is_valid():
            form.save()
            messages.success(request, f"i punti premio sono stati aggiornati con successo!")
            return redirect('core:index')
    else:
        form = RewardForm(instance=reward)

    context = {
        'form': form,
        'reward': reward
    }
    return render(request, 'core/reward.html', context)


def settings(request):
    privacy = Privacy.objects.all().first()
    conditions = Conditions.objects.all().first()
    initial_credits = Credits.objects.all().first()
    context = {
        'privacy': privacy,
        'conditions': conditions,
        'credits': initial_credits
    }
    return render(request, 'core/settings.html', context)


def privacy_edit(request):
    privacy = Privacy.objects.all().first()
    print(privacy)
    if request.POST:
        form = PrivacyForm(request.POST, instance=privacy)
        if form.is_valid():
            form.save()
            messages.success(request, f"La Privacy Policy è stata aggiornata!")
            return redirect('core:settings')
    else:
        form = PrivacyForm(instance=privacy)

    context = {
        'form': form,
        'privacy': privacy
    }
    return render(request, 'core/privacy.html', context)


def conditions_edit(request):
    conditions = Conditions.objects.all().first()
    if request.POST:
        form = ConditionsForm(request.POST, instance=conditions)
        if form.is_valid():
            form.save()
            messages.success(request, f"Le condizioni sono state aggiornate!")
            return redirect('core:settings')
    else:
        form = ConditionsForm(instance=conditions)

    context = {
        'form': form,
        'conditions': conditions
    }
    return render(request, 'core/conditions.html', context)


def credits_edit(request):
    initial_credits = Credits.objects.all().first()
    if request.POST:
        form = CreditsForm(request.POST, instance=initial_credits)
        if form.is_valid():
            form.save()
            messages.success(request, f"I crediti sono stati aggiornati!")
            return redirect('core:settings')
    else:
        form = CreditsForm(instance=initial_credits)

    context = {
        'form': form,
        'credits': initial_credits
    }
    return render(request, 'core/credits.html', context)


# 404 and 500 Handlers

def handle404(request, exception):
    return render(request, 'core/404.html', status=404)

def handle500(request, *args, **argv):
    return render(request, 'core/404.html', status=500)
