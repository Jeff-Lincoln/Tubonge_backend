# main_app/views.py
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CallRoom

@api_view(['POST'])
def create_room(request):
    """
    Creates a new room for the video call.
    The room_name is passed in the POST request.
    """
    room_name = request.data.get('room_name')

    # Check if room name is provided
    if not room_name:
        return Response({"error": "Room name is required."}, status=400)

    # Check if room already exists or create a new room
    room, created = CallRoom.objects.get_or_create(name=room_name)

    if created:
        return Response({"message": "Room created successfully", "room_name": room.name}, status=201)
    else:
        return Response({"message": "Room already exists", "room_name": room.name}, status=200)

@api_view(['POST'])
def join_room(request):
    """
    Joins an existing room. The room_name is passed in the POST request.
    """
    room_name = request.data.get('room_name')

    # Check if room name is provided
    if not room_name:
        return Response({"error": "Room name is required."}, status=400)

    # Get the room if it exists, otherwise return 404
    room = get_object_or_404(CallRoom, name=room_name)

    # Increment participant count (can be used to limit participants)
    room.participants_count += 1
    room.save()

    return Response({
        "message": f"Joined room {room_name}",
        "participants_count": room.participants_count
    }, status=200)

@api_view(['POST'])
def end_call(request):
    """
    Ends the call for the participant and decrements the participant count.
    If no participants are left, the room can be deleted.
    """
    room_name = request.data.get('room_name')

    # Check if room name is provided
    if not room_name:
        return Response({"error": "Room name is required."}, status=400)

    # Get the room
    room = get_object_or_404(CallRoom, name=room_name)

    # Decrease participant count
    room.participants_count -= 1
    room.save()

    # Optional: delete the room if no one is left
    if room.participants_count <= 0:
        room.delete()
        return Response({"message": f"Room {room_name} deleted as no participants are left."}, status=204)

    return Response({
        "message": f"Left room {room_name}",
        "participants_count": room.participants_count
    }, status=200)

@api_view(['GET'])
def get_room_info(request, room_name):
    """
    Retrieves information about the room, such as the participant count.
    """
    room = get_object_or_404(CallRoom, name=room_name)

    return Response({
        'room_name': room.name,
        'participants_count': room.participants_count,
        'created_at': room.created_at
    }, status=200)
