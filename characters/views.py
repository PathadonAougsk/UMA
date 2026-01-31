from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from .models import character


def playable(request):
    tmp_dict = {}
    for char in character.objects.all():
        tmp_dict[char.pk] = char.name

    return JsonResponse(tmp_dict)
