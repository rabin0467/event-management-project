from django.shortcuts import render, redirect
from datetime import date, timedelta
from django.db.models import Q, Count
from events.models import Event, Category, Participant
from events.forms import EventModelForm, CategoryModelForm, ParticipantModelForm
from django.contrib import messages

# Create your views here.

def event_list(request):
    type = request.GET.get('type', 'ongoing')
    # print(type)
    # getting event count:
    counts = Event.objects.aggregate(
        total_participants = Count("participants", distinct=True),
        total_event = Count('id', distinct=True),
        upcoming_event = Count('id', distinct=True, filter=Q(date__gt=date.today())),
        completed_event = Count('id', distinct=True, filter=Q(date__lt=date.today())),
        on_going_event = Count('id', distinct=True ,filter=Q(date=date.today()))
    )

    # Retriving data:
    base_query = Event.objects.select_related("category").prefetch_related("participants")
    if type=="upcoming":
        events = base_query.filter(date__gt=date.today())
    elif type == "completed":
        events= base_query.filter(date__lt=date.today())
    elif type == "ongoing":
        events = base_query.filter(date = date.today())
    elif type == "all":
        events = base_query.all()

    categories = Category.objects.all()
    query = request.GET.get('query')
    if query:
        events = base_query.filter(Q(name__icontains=query) | Q(location__icontains=query))

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        events = base_query.filter(date__gt=start_date,date__lt=end_date)
    
    context = {
        'counts': counts,
        'events': events,
        'type': type,
        'categories': categories,
        'query': query,
        'start_date': start_date,
        'end_date': end_date

    }

    return render(request, "events/event_list.html", context)

def participants_list(request):
    participants = Participant.objects.all().prefetch_related('events')
    

    return render(request, 'events/participants.html', {'participants': participants})

def event_details(request, event_id):
    event = Event.objects.prefetch_related('participants').get(id=event_id)


    return render(request, 'events/event_details.html', {'event': event})

def events_by_category(request, category_id):
    category = Category.objects.get(id = category_id)
    events = Event.objects.filter(category= category)
    # print('Category:', category)
    # print('events:', events)
    return render(request, 'events/events_by_category.html', {'events': events, 'category': category})

def create_category(request):
    if request.method == 'POST':
        cat_form = CategoryModelForm(request.POST)
        if cat_form.is_valid():
            cat_form.save()
            messages.success(request, 'Category created succesfully')
        else:
            messages.error(request, 'Something went wrong')
    else:
        cat_form = CategoryModelForm()
        

    return render(request, 'events/create_category.html', {'cat_form': cat_form})


def create_event(request):

    if request.method == 'POST':
        event_form = EventModelForm(request.POST)
        
        if event_form.is_valid():
            event_form.save()
            messages.success(request, 'Event Created Succesfully')
        else:
            messages.error(request, 'Something went wrong')

    else:
        event_form = EventModelForm()
        

           
    context = {
        'event_form': event_form,
    }
    
    return render(request, 'events/create_event.html', context)

def add_participant(request):
    if request.method == 'POST':
        parti_form = ParticipantModelForm(request.POST)
        if parti_form.is_valid():
            parti_form.save()
            messages.success(request, 'Participant added succesfully')
        else:
            messages.error(request, 'Something went wrong')
    else:
        parti_form = ParticipantModelForm()
        

    return render(request, 'events/add_participant.html', {'parti_form': parti_form})

def update_event(request, event_id):
    event = Event.objects.get(id=event_id)
    category = event.category

    if request.method == 'POST':
        event_form = EventModelForm(request.POST, instance=event)
        category_form = CategoryModelForm(request.POST, instance=category)

        if event_form.is_valid() and category_form.is_valid():
            category_form.save()
            event_form.save()
            messages.success(request, 'Event Updated Succesfully')
        else:
            messages.error(request, 'Something went wrong')
    else:
        event_form = EventModelForm(instance=event)
        category_form = CategoryModelForm(instance=category)
        

    context = {
        'event':event,
        'event_form': event_form,
        'category_form': category_form
    }
    return render(request, 'events/update_event.html', context)

def delete_event(request, event_id):
    event = Event.objects.get(id=event_id)

    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event Deleted Succesfully')
        return redirect('event-list')
    else:
        event.delete()
        messages.success(request, 'Event Deleted Succesfully')
        return redirect('event-list')
    

def navbar(request):
    return render(request, "navbar.html")