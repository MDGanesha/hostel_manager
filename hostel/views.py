from django.shortcuts import render, get_object_or_404,redirect
from .models import Room, RoomAllocation
from .forms import Allocation
from django.contrib.auth.models import User
def index(request):
    rooms = Room.objects.all()
    roomcount = rooms.count()
    context = {'rooms': rooms,'roomcount':roomcount}
    return render(request, 'hostel/index.html', context)

def addRoom(request):
    if(request.method == "POST"):
        room_number = request.POST.get('room_number')
        capacity = request.POST.get('capacity')
        room = Room(room_number = int(room_number),capacity = int(capacity))
        room.save()
        return redirect('hostel:index')
    return render(request,'hostel/addroom.html')
def allocation_view(request, pk):
    # Fetch all allocations for the room and the room object itself
    allocations = RoomAllocation.objects.filter(room=pk)
    room = get_object_or_404(Room, room_number=pk)

    # Count the number of allocations
    allocations_count = allocations.count()

    # Update the 'occupied' status based on the number of allocations
    room.occupied = allocations_count >= 8
    room.save()
    
    # Debug prints (if needed for development)
    print(f"Allocations count: {allocations_count}")
    print(f"Room Number: {room.room_number}")
    print(f"Room Occupied: {room.occupied}")

    # Prepare context for the template
    context = {
        'allocations': allocations,
        'room': room,
        'allocationscount': allocations_count,
        'room_number': pk,
    }

    # Render the template with the context
    return render(request, 'hostel/allocation.html', context)


def delete(request, pk):
    allocated = get_object_or_404(RoomAllocation, pk=pk)
    allocated.delete()
    # Redirect to the 'index' page or wherever the allocations are listed
    return redirect('hostel:index')  # Or 'hostel:allocations' if that's correct


def update(request, pk):
    slot = get_object_or_404(RoomAllocation, pk = pk)
    form = Allocation(instance=slot)
    if(request.method == 'POST'):
        form = Allocation(request.POST,instance=slot)
        form.save()
        return redirect('hostel:index')
    return render(request,'hostel/update.html',{'form':form})


def add(request):
    q = request.GET.get('q')
    room = get_object_or_404(Room, pk=q)  # Ensure room exists
    users = User.objects.all()  # Fetch all users
    allocationRoom = RoomAllocation.objects.filter(room = room)
    if request.method == 'POST':
        username = request.POST.get('user')  # Get the username from the hidden input
        user = get_object_or_404(User, username=username)  # Ensure user exists

        allocation = RoomAllocation(user=user, room=room)  # Create allocation
        allocation.save()  # Save to database
        if(allocationRoom.count()== room.capacity):
            room.occupied = True
            room.save()
        return redirect('hostel:index')  # Redirect after successful allocation

    context = {'users': users, 'room': room}
    return render(request, 'hostel/add.html', context)

def deleteRoom(request,pk):
    room = Room.objects.get(pk = pk)
    room.delete()
    return redirect("hostel:index")