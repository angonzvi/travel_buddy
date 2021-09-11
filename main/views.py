from django.contrib import messages
from django.shortcuts import redirect, render
import bcrypt
from .decorators import login_required
from .models import User, Trips
import datetime

@login_required
def index(request):
    user_session = request.session['user']
    user = User.objects.get(email=user_session['email'])
    all_trips = Trips.objects.all().order_by('-start_date')
    inHere = [travel.id for travel in user.viajes.all()]
    notHere = [travel for travel in Trips.objects.all() if travel.id not in inHere]
    data = {
        'trips': user.viajes.all().order_by('start_date'),
        'other_trips': notHere,
    }
    return render(request, 'index.html', data)

@login_required
def add(request):
    return render(request, 'add.html')

@login_required
def add_travel(request):
    if request.method == "POST":
        errors = Trips.objects.validate(request.POST)
        if len(errors) > 0:
            for llave, msge_error in errors.items():
                messages.error(request, msge_error)
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            user = User.objects.get(id = int(request.session['user']['id']))
            trip = Trips.objects.create(destination = request.POST['destination'],
                                        start_date = datetime.datetime.strptime(request.POST['start_date'], "%Y-%m-%d").date(),
                                        end_date = datetime.datetime.strptime(request.POST['end_date'], "%Y-%m-%d").date(),
                                        description = request.POST['description_plan'])
            user.viajes_creados.add(trip)
            user.viajes.add(trip)
            messages.success(request, 'Viaje Creado!')
            return redirect('/')
    else:
        return redirect(request.META.get('HTTP_REFERER'))

@login_required
def destination(request, trip_id):
    trip = Trips.objects.get(id = int(trip_id))
    travellers = trip.user.all().exclude(id = trip.owner_user.id)

    context = {
        'trip' : trip,
        'travellers' : travellers
    }
    return render(request, 'trips.html', context)

@login_required
def delete(request, trip_id):
    trip = Trips.objects.get(id = trip_id)
    trip.delete()
    messages.error(request, 'Viaje Eliminado!')
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def cancel(request, trip_id):
    current_user = User.objects.get(id = int(request.session['user']['id']))
    trip = Trips.objects.get(id = trip_id)
    current_user.viajes.remove(trip)
    messages.warning(request, 'Viaje Cancelado!')
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def join_trip(request, trip_id):
    user = User.objects.get(id = int(request.session['user']['id']))
    travel = Trips.objects.get(id=int(trip_id))
    travel.user.add(user)
    messages.success(request, 'Ya eres parte de este viaje')
    return redirect(request.META.get('HTTP_REFERER'))
