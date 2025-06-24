# from django.shortcuts import render, redirect, get_object_or_404
# from rest_framework.decorators import api_view, permission_classes
# from .models import Message
# from django.contrib.auth.decorators import login_required
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.permissions import IsAuthenticated

# @login_required
def chat_room(request, room_name):
    return
#     search_query = request.GET.get('search', '')
#     users = User.objects.exclude(id=request.user.id)
#     chats = Message.objects.filter(
#         (Q(sender=request.user) & Q(receiver_username=room_name)) |
#         (Q(receiver=request.user) & Q(sender=room_name)) 
#         )
#     if search_query:
#        chats = chats.filter(Q(content_icontains=search_query))
#        chats = chats.order_by('timestamp')
#        user_last_messages = []
#        for user in users:
#         last_message = Message.objects.filter(
#           (Q(sender=request.user) & Q(receiver=user)) |
#           (Q(receiver = request.user) & Q(sender=user))
#           ).order_by('-timestamp').first
#         user_last_messages.append({
#            'user': user,
#            'last_message': last_message
#         })

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def HomeView(request):
#     if request.method == "POST":
#         room_name = request.POST["room"]
#         room, _ = Room.objects.get_or_create(room_name__iexact=room_name)
#         return redirect("room", room_name=room.room_name)
#     return render(request, "home.html")

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def RoomView(request, room_name):
#     room = get_object_or_404(Room, room_name__iexact=room_name)
#     messages = Message.objects.filter(room=room)
#     context = {
#         "messages": messages,
#         "room_name": room.room_name,
#         "user": request.user  # Pass actual user object
#     }
#     return render(request, "room.html", context)

# def HomeView(request):
#     if request.method == "POST":
#         username = request.POST["username"]
#         room = request.POST["room"]
#         try:
#             existing_room = PrivateRoom.objects.get(room_name__icontains = room)
#         except PrivateRoom.DoesNotExist:
#             r = PrivateRoom.objects.create(room_name = room)
#         return redirect("room", room_name=room, username=username)
#     return render(request, "home.html")

# def RoomView(request, room_name, username):
#     existing_room = PrivateRoom.objects.get(room_name__icontains=room_name)
#     get_messages = Message.objects.filter(room=existing_room)
#     context = {
#         "messages": get_messages,
#         "user": username,
#         "room_name": room_name
#     }
#     return render(request, "room.html", context)
    
# ---------------------------------------------------------------------
# from . models import Message
# from django.contrib.auth import get_user_model
# from django.db.models import Q

# # Create your views here.

# def chat_room(request, room_name):
#     search_query = request.GET.get('search', '')
#     users = User.objects.exclude(id=request.user.id)
#     chats = Message.objects.filter(
#         (Q(sender=request.user) & Q(receiver_username=room_name)) |
#         (Q(receiver=request.user) & Q(sender=room_name)) 
#     )

#     if search_query:
#         chats = chats.filter(Q(content_icontains=search_query))

#     chats = chats.order_by('timestamp')
#     user_last_messages = []

#     for user in users:
#         last_message = Message.objects.filter(
#             (Q(sender=request.user) & Q(receiver=user)) |
#             (Q(receiver = request.user) & Q(sender=user))
#         ).order_by('-timestamp').first

#         user_last_messages.append({
#             'user': user,
#             'last_message': last_message
#         })

    


