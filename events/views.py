from django.shortcuts import render, redirect, HttpResponse
from datetime import date, timedelta
from django.db.models import Q, Count
from events.models import Event, Category
from events.forms import EventModelForm, CategoryModelForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.contrib.auth.models import User
from users.views import is_admin
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.

def is_adminOrManager(user):
    return (user.groups.filter(name='Admin').exists() or 
            user.groups.filter(name='Organizer').exists()
    )

def organizer_view(request):
    is_organizer = request.user.groups.filter(name='Organizer').exists()
    return render(request,'loged_nav.html', {'is_organizer': is_organizer})

@login_required
def event_list(request):
    type = request.GET.get('type', 'ongoing')
    # print(type)
    # getting event count:
    counts = Event.objects.aggregate(
        total_participants = Count("rsvp_participants", distinct=True),
        total_event = Count('id', distinct=True),
        upcoming_event = Count('id', distinct=True, filter=Q(date__gt=date.today())),
        completed_event = Count('id', distinct=True, filter=Q(date__lt=date.today())),
        on_going_event = Count('id', distinct=True ,filter=Q(date=date.today()))
    )

    # Retriving data:
    base_query = Event.objects.select_related("category").prefetch_related("rsvp_participants")
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


@user_passes_test(is_adminOrManager, login_url='no-permission')
def participants_list(request):
    rsvp_users = User.objects.filter(rsvp_events__isnull=False).distinct()

    return render(request, 'events/participants.html', {'users': rsvp_users})


@login_required
def event_details(request, event_id):
    event = Event.objects.prefetch_related('rsvp_participants').get(id=event_id)


    return render(request, 'events/event_details.html', {'event': event})

@login_required
def events_by_category(request):
    categories = Category.objects.prefetch_related('events')
    return render(request, 'events/events_by_category.html', { 'categories': categories})


@user_passes_test(is_adminOrManager, login_url='no-permission')
def create_category(request):
    if request.method == 'POST':
        cat_form = CategoryModelForm(request.POST)
        if cat_form.is_valid():
            cat_form.save()
            messages.success(request, 'Category created succesfully')
            return redirect('events-by-category')
        else:
            messages.error(request, 'Something went wrong')
    else:
        cat_form = CategoryModelForm()
        

    return render(request, 'events/create_category.html', {'cat_form': cat_form})

@user_passes_test(is_admin, login_url='no-permission')
def update_category(request, category_id):
    category = Category.objects.get(id=category_id)

    if request.method == 'POST':
        category_form = CategoryModelForm(request.POST, instance=category)

        if category_form.is_valid():
            category_form.save()
            messages.success(request, f'{category.name} Updated Succesfully')
            return redirect('events-by-category')
        else:
            messages.error(request, 'Something went wrong')
    else:
        category_form = CategoryModelForm(instance=category)
        
    return render(request, 'events/update_category.html', {'category_form': category_form})

@login_required
@user_passes_test(is_adminOrManager, login_url='no-permission')
def category_details(request, cat_id):
    category = Category.objects.prefetch_related('events').get(id=cat_id)

    return render(request, 'events/category_details.html', {'category': category})



@user_passes_test(is_admin, login_url='no-permission')
def delete_category(request,cat_id):
    category = Category.objects.get(id=cat_id)

    if request.method == 'POST':
        cat_name = category.name
        category.delete()
        messages.success(request, f'{cat_name} deleted succesfully')
        return redirect('events-by-category')
    
    return render(request, 'events/delete_category.html', {'category':category})

@user_passes_test(is_adminOrManager, login_url='no-permission')
def create_event(request):

    if request.method == 'POST':
        event_form = EventModelForm(request.POST, request.FILES)
        
        if event_form.is_valid():
            event_form.save()
            messages.success(request, 'Event Created Succesfully')
            return redirect('event-list')
        else:
            messages.error(request, 'Something went wrong')

    else:
        event_form = EventModelForm()
        

           
    context = {
        'event_form': event_form,
    }
    
    return render(request, 'events/create_event.html', context)

@user_passes_test(is_adminOrManager, login_url='no-permission')
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
            return redirect('event-list')
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

@user_passes_test(is_adminOrManager, login_url='no-permission')
def delete_event(request, event_id):
    event = Event.objects.get(id=event_id)

    if request.method == 'POST':
        event_name = event.name
        event.delete()
        messages.success(request, f'{event_name} deleted succesfully')
        return redirect('event-list')
    
    return render(request, 'events/delete_event.html', {'event':event})

def rsvp_event(request, event_id):
    event = Event.objects.get(id = event_id)
    user = request.user

    if user in event.rsvp_participants.all():
        messages.info(request, 'You have already joined to this event')
        return redirect("rsvp-dashboard")
    else:
        event.rsvp_participants.add(user)
        messages.success(request, 'RSVP successful ! A confirmation email sent')
    return redirect("rsvp-dashboard")

def rsvp_activation_mail(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('sign-in')
        else:
            return HttpResponse('Invalid id or token')
    except User.DoesNotExist:
        return HttpResponse('User not found')

@user_passes_test(is_adminOrManager, login_url='no-permission')
def organizer_dashboard(request):
    categories = Category.objects.prefetch_related('events__rsvp_participants')
    events = Event.objects.select_related('category').prefetch_related('rsvp_participants')

    context={
        'categories': categories,
        'events': events
    }
    return render(request, 'organizer/organizer_dashboard.html', context)
    

    

def navbar(request):
    return render(request, "navbar.html")