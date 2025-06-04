from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Player, GameSession, Score

class PlayerAdmin(UserAdmin):
    list_display = ('username', 'date_joined', 'total_games', 'best_score', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Stats', {'fields': ('total_games', 'best_score')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_admin', 'groups', 'user_permissions')}),
    )

@admin.register(GameSession)
class GameSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'player', 'target', 'attempts', 'completed')
    list_filter = ('completed', 'player')

@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ('player', 'attempts', 'created_at')
    list_filter = ('player',)

admin.site.register(Player, PlayerAdmin)