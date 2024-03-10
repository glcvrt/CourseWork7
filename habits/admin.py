from django.contrib import admin

from habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    """ Отражение привычек в админке """

    list_display = ('name', 'habit_is_public', 'user',)
    list_filter = ('name',)
    search_fields = ('name',)
