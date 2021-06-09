from django.shortcuts import render


def index(request):
    return render(request, 'notifications/index.html', {})


def room(request, room_name):
    return render(request, 'notifications/room.html', {
        'room_name': room_name
    })
