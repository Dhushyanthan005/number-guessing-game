import random
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import GameSession, Score

@login_required
def home(request):
    return render(request, 'game/home.html', {
        'player': request.user,
        'best_score': request.user.best_score
    })

@login_required
def new_game(request):
    target = random.randint(1, 100)
    game = GameSession.objects.create(
        player=request.user,
        target=target
    )
    request.user.total_games += 1
    request.user.save()
    return redirect('guess', game_id=game.id)

@login_required
def guess_view(request, game_id):
    try:
        game = GameSession.objects.get(id=game_id, player=request.user)
    except GameSession.DoesNotExist:
        messages.error(request, "Game not found")
        return redirect('home')
    
    if game.completed:
        messages.info(request, "This game is already completed")
        return redirect('home')
    
    context = {
        'game': game,
        'player': request.user
    }
    
    if request.method == 'POST':
        try:
            user_guess = int(request.POST.get('guess'))
            game.attempts += 1
            game.save()
            
            if user_guess == game.target:
                # Game completed
                game.completed = True
                game.save()
                
                # Save score
                Score.objects.create(
                    player=request.user,
                    attempts=game.attempts
                )
                
                # Update best score if needed
                if game.attempts < request.user.best_score:
                    request.user.best_score = game.attempts
                    request.user.save()
                
                messages.success(
                    request, 
                    f'🎉 Correct! It took you {game.attempts} attempts.'
                )
                return redirect('home')
            elif user_guess < game.target:
                messages.warning(request, '⬆️ Too low! Try a higher number.')
            else:
                messages.warning(request, '⬇️ Too high! Try a lower number.')
                
        except (TypeError, ValueError):
            messages.error(request, '⚠️ Please enter a valid number!')
    
    return render(request, 'game/game.html', context)

@login_required
def leaderboard(request):
    top_scores = Score.objects.select_related('player').order_by('attempts')[:10]
    return render(request, 'game/leaderboard.html', {
        'scores': top_scores,
        'player': request.user
    })