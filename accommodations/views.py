from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.contrib import messages
from django.db.models import Q, Sum
from .models import Accommodation, SiteContent, Location, LandlordProfile, StudentProfile, AccommodationImage
from .forms import (AccommodationForm, RoleSelectionForm,
                   StudentRegistrationForm, LandlordRegistrationForm,
                   AccommodationWithImagesForm)
from accommodations import models
from django.utils import timezone

def is_landlord(user):
    return user.groups.filter(name='Landlords').exists() or user.is_superuser

def register_role_selection(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RoleSelectionForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data['role']
            if role == 'student':
                return redirect('register_student')
            else:
                return redirect('register_landlord')
    else:
        form = RoleSelectionForm()

    return render(request, 'auth/role_selection.html', {'form': form})

def register_student(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Create student profile
            StudentProfile.objects.create(
                user=user,
                phone_number=form.cleaned_data.get('phone_number', ''),
                university=form.cleaned_data.get('university', '')
            )

            # Add to Students group
            student_group, created = Group.objects.get_or_create(name='Students')
            user.groups.add(student_group)

            # Auto-login and redirect
            login(request, user)
            messages.success(request,
                'Student account created successfully! Start browsing accommodations.'
            )
            return redirect('accommodation_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = StudentRegistrationForm()

    return render(request, 'auth/register_student.html', {'form': form})

def register_landlord(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LandlordRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Create landlord profile
            LandlordProfile.objects.create(
                user=user,
                phone_number=form.cleaned_data.get('phone_number', ''),
                company_name=form.cleaned_data.get('company_name', '')
            )

            # Add to Landlords group
            landlord_group, created = Group.objects.get_or_create(name='Landlords')
            user.groups.add(landlord_group)

            # Auto-login and redirect
            login(request, user)
            messages.success(request,
                'Landlord account created successfully! You can now list your accommodations. '
                'Note: All listings require admin approval before being publicly visible.'
            )
            return redirect('landlord_dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LandlordRegistrationForm()

    return render(request, 'auth/register_landlord.html', {'form': form})



def register(request):
    return redirect('register_role_selection')

def landing_page(request):
    featured_accommodations = Accommodation.objects.filter(
        is_approved=True,
        is_featured=True,
        available_rooms__gt=0
    )[:4]

    return render(request, 'landing.html', {
        'featured_accommodations': featured_accommodations
    })

def accommodation_list(request):
    accommodations = Accommodation.objects.filter(is_approved=True, available_rooms__gt=0)

    # Filters
    search_query = request.GET.get('search', '')
    room_type = request.GET.get('room_type', '')
    location_id = request.GET.get('location', '')
    price_range = request.GET.get('price_range', '')

    if search_query:
        accommodations = accommodations.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    if room_type:
        accommodations = accommodations.filter(room_type=room_type)

    if location_id:
        accommodations = accommodations.filter(location_id=location_id)

    if price_range:
        if price_range == '0-300':
            accommodations = accommodations.filter(price__lte=300)
        elif price_range == '300-500':
            accommodations = accommodations.filter(price__range=(300, 500))
        elif price_range == '500-700':
            accommodations = accommodations.filter(price__range=(500, 700))
        elif price_range == '700+':
            accommodations = accommodations.filter(price__gte=700)

    locations = Location.objects.all()

    return render(request, 'accommodations/list.html', {
        'accommodations': accommodations,
        'locations': locations,
        'search_query': search_query,
        'selected_room_type': room_type,
        'selected_location': location_id,
        'selected_price_range': price_range,
    })

def accommodation_detail(request, pk):
    accommodation = get_object_or_404(Accommodation, pk=pk, is_approved=True)

     # Check if the accommodation is approved OR if the user is the landlord
    if not accommodation.is_approved and request.user != accommodation.landlord:
        messages.error(request, 'This accommodation is not available.')
        return redirect('accommodation_list')

    return render(request, 'accommodations/detail.html', {
        'accommodation': accommodation
    })


@login_required
def accommodation_preview(request, pk):
    """Preview accommodation for landlords (even if not approved)"""
    accommodation = get_object_or_404(Accommodation, pk=pk, landlord=request.user)

    return render(request, 'accommodations/detail.html', {
        'accommodation': accommodation,
        'is_preview': True
    })



@login_required
@user_passes_test(is_landlord, login_url='/admin/login/')
def landlord_dashboard(request):
    # Check if user is a landlord
    if not request.user.groups.filter(name='Landlords').exists():
        messages.error(request, 'You need a landlord account to access the dashboard.')
        return redirect('accommodation_list')

    accommodations = Accommodation.objects.filter(landlord=request.user)

    # Calculate proper stats
    total_listings = accommodations.count()
    approved_listings = accommodations.filter(is_approved=True).count()
    pending_listings = accommodations.filter(is_approved=False).count()

    # Calculate total available rooms manually
    approved_accommodations = accommodations.filter(is_approved=True)
    available_rooms = 0
    for accommodation in approved_accommodations:
        available_rooms += accommodation.available_rooms

    return render(request, 'accommodations/landlord_dashboard.html', {
        'accommodations': accommodations,
        'total_listings': total_listings,
        'approved_listings': approved_listings,
        'pending_listings': pending_listings,
        'available_rooms': available_rooms,
    })




@login_required
@user_passes_test(is_landlord, login_url='/admin/login/')
def accommodation_create(request):
    # Check if user is a landlord
    if not request.user.groups.filter(name='Landlords').exists():
        messages.error(request, 'You need a landlord account to list accommodations.')
        return redirect('accommodation_list')

    if request.method == 'POST':
        form = AccommodationWithImagesForm(request.POST, request.FILES)
        if form.is_valid():
            # Create accommodation
            accommodation = Accommodation(
                landlord=request.user,
                description=form.cleaned_data['description'],
                room_type=form.cleaned_data['room_type'],
                price=form.cleaned_data['price'],
                location=form.cleaned_data['location'],
                available_rooms=form.cleaned_data['available_rooms']
            )
            accommodation.save()

            # Handle image uploads
            images = []
            for i in range(1, 6):
                image_field = f'image_{i}'
                if image_field in request.FILES:
                    is_primary = (i == 1)  # First image is primary
                    accommodation_image = AccommodationImage(
                        accommodation=accommodation,
                        image=request.FILES[image_field],
                        is_primary=is_primary
                    )
                    accommodation_image.save()
                    images.append(accommodation_image)

            messages.success(request, 'Accommodation created successfully! It will be visible after approval.')
            return redirect('landlord_dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AccommodationWithImagesForm()

    return render(request, 'accommodations/accommodation_form.html', {
        'form': form,
        'title': 'Add New Accommodation'
    })

@login_required
def accommodation_update(request, pk):
    accommodation = get_object_or_404(Accommodation, pk=pk, landlord=request.user)

    if request.method == 'POST':
        form = AccommodationForm(request.POST, instance=accommodation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Accommodation updated successfully!')
            return redirect('landlord_dashboard')
    else:
        form = AccommodationForm(instance=accommodation)

    return render(request, 'accommodations/accommodation_form.html', {
        'form': form,
        'title': 'Edit Accommodation',
        'accommodation': accommodation
    })

@login_required
def accommodation_delete(request, pk):
    accommodation = get_object_or_404(Accommodation, pk=pk, landlord=request.user)
    if request.method == 'POST':
        accommodation.delete()
        messages.success(request, 'Accommodation deleted successfully!')
        return redirect('landlord_dashboard')

    return render(request, 'accommodations/accommodation_confirm_delete.html', {
        'accommodation': accommodation
    })



@login_required
def landlord_profile_update(request):
    """Update landlord profile including phone number"""
    if not request.user.groups.filter(name='Landlords').exists():
        messages.error(request, 'You need a landlord account to access this page.')
        return redirect('accommodation_list')

    landlord_profile = getattr(request.user, 'landlordprofile', None)

    if request.method == 'POST':
        phone_number = request.POST.get('phone_number', '')
        company_name = request.POST.get('company_name', '')

        # Validate phone number (basic validation)
        if phone_number and len(phone_number) < 10:
            messages.error(request, 'Please enter a valid phone number.')
        else:
            # Update or create landlord profile
            if landlord_profile:
                landlord_profile.phone_number = phone_number
                landlord_profile.company_name = company_name
                landlord_profile.save()
            else:
                LandlordProfile.objects.create(
                    user=request.user,
                    phone_number=phone_number,
                    company_name=company_name
                )

            messages.success(request, 'Profile updated successfully!')
            return redirect('landlord_dashboard')

    return render(request, 'accommodations/landlord_profile_update.html', {
        'landlord_profile': landlord_profile
    })


def terms_and_conditions(request):
    content = get_object_or_404(SiteContent, content_type='terms', is_active=True)
    return render(request, 'accommodations/site_content.html', {
        'content': content,
        'title': content.title
    })

def privacy_policy(request):
    content = get_object_or_404(SiteContent, content_type='privacy', is_active=True)
    return render(request, 'accommodations/site_content.html', {
        'content': content,
        'title': content.title
    })

def about_us(request):
    content = get_object_or_404(SiteContent, content_type='about', is_active=True)
    return render(request, 'accommodations/site_content.html', {
        'content': content,
        'title': content.title
    })

def safety_guidelines(request):
    content = get_object_or_404(SiteContent, content_type='safety', is_active=True)
    return render(request, 'accommodations/site_content.html', {
        'content': content,
        'title': content.title
    })