from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib import messages

from .models import Game, Challenge, EventGame, Promotion
from .forms import GameForm, ChallengeForm, PromotionForm

from trend.decorators import admin_only


# Listing Games
@admin_only
def index(request):
    games = Game.objects.all()
    context = {
        'games': games
    }
    return render(request, 'game/games.html', context)

# Single Game Info
def single(request, id):
    game = get_object_or_404(Game, pk=id)
    promotions = Promotion.objects.filter(game=game)
    print(promotions)
    context = {
        'game': game,
        'promotions': promotions
    }
    return render(request, 'game/game_details.html', context)   

# Create Game
@admin_only
def create_game(request):
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES)
        if form.is_valid():
            game = form.save()
            if game.category == 'Event':
                eventgame = EventGame.objects.create(game=game)
                game.eventgame.save()
                messages.success(request, f"Gioco creato con successo!")
            return redirect('game:index')
    else:
        form = GameForm()
    context = {
        'form': form
    }
    return render(request, 'game/create_game.html', context)

# Edit Game
@admin_only
def edit_game(request, id):
    game = get_object_or_404(Game, pk=id)
    categ = game.category
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES, instance=game)
        if form.is_valid():
            new_game = form.save()
            messages.success(request, f"Gioco aggiornato con successo!")
            if categ == 'Classic' and new_game.category == 'Event':
                eventgame, created = EventGame.objects.get_or_create(game=new_game)
                eventgame.save()

            elif categ == 'Event' and new_game.category == 'Classic':
                new_game.min_players = 0
                new_game.save()
                if EventGame.objects.filter(game=new_game).exists():
                    EventGame.objects.get(game=new_game).delete()

            if new_game.category == 'Event' and request.POST.get('id_num_players'):
                game.eventgame.num_players = request.POST.get('id_num_players')
                game.eventgame.save()
            
            return redirect('game:index')

    else:
        form = GameForm(instance=game)
    context = {
        'form': form,
        'game': game
    }
    return render(request, 'game/edit_game.html', context)

# Delete Game
@admin_only
def delete_game(request, id):
    game = get_object_or_404(Game, pk=id)
    if request.method == 'POST':
        game.delete()
        messages.success(request, f"Gioco eliminato con successo!")
        return redirect('game:index')
    context = {
        'game': game
    }
    return render(request, 'game/delete_game.html', context)





# Listing Categories
@admin_only
def category(request):
    if 'game' in str(request.get_full_path):
        print('True')
    else:
        print('False')
    categories = GameCategory.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'game/index.html', context)



# Get Single Game Challenges
@admin_only
def challenge(request, id):
    game = get_object_or_404(Game, pk=id)
    get_challenges = Challenge.objects.filter(game=game.id)
    if game and not get_challenges:
        challenges = None
    else:
        challenges = get_list_or_404(Challenge, game=game.id)
    context = {
        'challenges': challenges,
        'game': game
    }
    return render(request, 'game/games_challenge.html', context)


# Get single challenge detail
@admin_only
def single_challenge(request, id):
    challenge = get_object_or_404(Challenge, pk=id)
    context = {
        'challenge': challenge
    }
    return render(request, 'game/single_challenge.html', context)

# Create Challenge
@admin_only
def create_challenge(request, id):
    game = get_object_or_404(Game, pk=id)
    if request.method == 'POST':
        form = ChallengeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f"sfida creata con successo!")
            return redirect('game:index')
    else:
        form = ChallengeForm()
    context = {
        'form': form,
        'game': game
    }
    return render(request, 'game/create_game_challenge.html', context)


# Edit Challenge
@admin_only
def edit_challenge(request, id):
    challenge = get_object_or_404(Challenge, pk=id)
    if request.method == 'POST':
        form = ChallengeForm(request.POST, request.FILES, instance=challenge)
        if form.is_valid():
            form.save()
            messages.success(request, f"sfida aggiornata con successo!")
            return redirect('game:index')
    else:
        form = ChallengeForm(instance=challenge)
    context = {
        'form': form
    }
    return render(request, 'game/edit_game_challenge.html', context)

# Delete Challenge
@admin_only
def delete_challenge(request, id):
    challenge = get_object_or_404(Challenge, pk=id)
    if request.method == 'POST':
        challenge.delete()
        messages.success(request, f"sfida eliminata correttamente!")
        return redirect('game:index')
    context = {
        'challenge': challenge
    }
    return render(request, 'game/delete_challenge.html', context)




# Promotions
@admin_only
def create_promotion(request, id):
    game = get_object_or_404(Game, pk=id)
    if request.method == 'POST':
        form = PromotionForm(request.POST, request.FILES)
        if form.is_valid():
            promotion = form.save(commit=False)
            promotion.game = game
            promotion.save()
            messages.success(request, f"Gioco creato con successo!")
            return redirect('game:single', game.id)
    else:
        form = PromotionForm()
    context = {
        'form': form
    }
    return render(request, 'game/create_promotion.html', context)



# Delete Game
@admin_only
def delete_promotion(request, id):
    promotion = get_object_or_404(Promotion, pk=id)
    game = promotion.game
    if request.method == 'POST':
        promotion.delete()
        messages.success(request, f"Gioco eliminato con successo!")
        return redirect('game:single', game.id)
    context = {
        'promotion': promotion
    }
    return render(request, 'game/delete_promotion.html', context)
    


# Edit Game
@admin_only
def edit_promotion(request, id):
    promotion = get_object_or_404(Promotion, pk=id)
    if request.method == 'POST':
        form = PromotionForm(request.POST, request.FILES, instance=promotion)
        if form.is_valid():
            form.save()
            return redirect('game:single', promotion.game.id)

    else:
        form = PromotionForm(instance=promotion)
    context = {
        'form': form,
        'promotion': promotion
    }
    return render(request, 'game/edit_promotion.html', context)
