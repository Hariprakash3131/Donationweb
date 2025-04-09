from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from decimal import Decimal, InvalidOperation
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import timedelta
import json
from .forms import SignupForm, DonationForm, ScholarshipForm
from .models import Donation, ScholarshipApplication, Contact

def index(request):
    return render(request, 'index.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')

@login_required
def my_activities(request):
    donations = Donation.objects.filter(user=request.user).order_by('-date')
    total_amount = donations.aggregate(total=Sum('amount'))['total']
    
    # Get user's scholarship applications
    scholarship_applications = ScholarshipApplication.objects.filter(user=request.user).order_by('-date_submitted')
    
    return render(request, 'accounts/my_activities.html', {
        'donations': donations,
        'total_amount': total_amount,
        'scholarship_applications': scholarship_applications
    })

@login_required
def donation_form(request):
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.user = request.user
            donation.save()
            return redirect('payment', donation_id=donation.id)
    else:
        form = DonationForm()
    return render(request, 'accounts/donation.html', {'form': form})

def payment(request, donation_id):
    donation = get_object_or_404(Donation, id=donation_id)
    return render(request, 'accounts/payment.html', {'donation': donation})

def payment_success(request, donation_id):
    donation = get_object_or_404(Donation, id=donation_id)
    amount_param = request.GET.get('amount')
    transaction_id = request.GET.get('transaction_id', 'TXN' + str(donation_id).zfill(10))
    
    if amount_param:
        try:
            donation.amount = Decimal(amount_param)
            donation.save()
        except (InvalidOperation, ValueError):
            messages.error(request, "Invalid amount format provided.")
    
    return render(request, 'accounts/payment_success.html', {
        'donation': donation,
        'amount': donation.amount,
        'transaction_id': transaction_id
    })

@login_required
def scholarship_form(request):
    if request.method == "POST":
        form = ScholarshipForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            messages.success(request, 'Your scholarship application has been submitted successfully!')
            return redirect('success_page')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ScholarshipForm()
    
    return render(request, 'accounts/scholarship_form.html', {'form': form})

def success_page(request):
    return render(request, 'accounts/success_page.html')

def about(request):
    return render(request, 'accounts/about.html')

@login_required
def contact_admin_dashboard(request):
    if not request.user.is_staff:
        messages.error(request, 'Access Denied. Admin privileges required.')
        return redirect('index')
        
    # Get current date
    today = timezone.now().date()
    week_start = today - timedelta(days=today.weekday())
    
    # Get message counts
    total_messages = Contact.objects.count()
    today_messages = Contact.objects.filter(created_at__date=today).count()
    week_messages = Contact.objects.filter(created_at__date__gte=week_start).count()
    
    # Get all messages ordered by newest first
    contact_messages = Contact.objects.all().order_by('-created_at')
    
    context = {
        'total_messages': total_messages,
        'today_messages': today_messages,
        'week_messages': week_messages,
        'messages': contact_messages,
        'section': 'contact_admin'  # For navbar active state
    }
    
    return render(request, 'contact_admin.html', context)

@login_required
@require_POST
def delete_contact_message(request, message_id):
    if not request.user.is_staff:
        return JsonResponse({'status': 'error', 'message': 'Permission denied'}, status=403)
        
    try:
        message = Contact.objects.get(id=message_id)
        message.delete()
        return JsonResponse({'status': 'success'})
    except Contact.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Message not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
        
    messages.success(request, 'Message deleted successfully.')

def contact(request):
    if request.method == 'POST':
        try:
            data = request.POST
            contact = Contact.objects.create(
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                email=data.get('email'),
                subject=data.get('subject'),
                message=data.get('message')
            )
            return JsonResponse({
                'status': 'success',
                'message': 'Thank you for your message! We will get back to you soon.'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': 'An error occurred. Please try again.'
            }, status=400)
    return render(request, 'contact.html')

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        messages.error(request, 'Access Denied. Admin privileges required.')
        return redirect('index')
        
    # Get all donations with total
    donations = Donation.objects.all().order_by('-date')
    total_donations = donations.aggregate(total=Sum('amount'))['total'] or 0
    
    # Get all scholarship applications
    scholarship_applications = ScholarshipApplication.objects.all().order_by('-date_submitted')
    
    # Get statistics
    pending_applications = scholarship_applications.filter(application_status='pending').count()
    approved_applications = scholarship_applications.filter(application_status='approved').count()
    rejected_applications = scholarship_applications.filter(application_status='rejected').count()
    
    context = {
        'donations': donations,
        'total_donations': total_donations,
        'scholarship_applications': scholarship_applications,
        'pending_applications': pending_applications,
        'approved_applications': approved_applications,
        'rejected_applications': rejected_applications,
    }
    return render(request, 'accounts/admin_dashboard.html', context)

@login_required
@require_POST
def update_application_status(request):
    if not request.user.is_staff:
        return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)
    
    try:
        data = json.loads(request.body)
        application_id = data.get('application_id')
        status = data.get('status')
        
        if not application_id or not status:
            return JsonResponse({'success': False, 'error': 'Missing required fields'}, status=400)
            
        if status not in ['pending', 'approved', 'rejected']:
            return JsonResponse({'success': False, 'error': 'Invalid status value'}, status=400)
            
        application = ScholarshipApplication.objects.get(id=application_id)
        application.application_status = status
        application.save()
        
        return JsonResponse({'success': True, 'message': f'Application {status} successfully'})
    except ScholarshipApplication.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Application not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
@require_POST
def delete_application(request, application_id):
    if not request.user.is_staff:
        return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)
    
    try:
        application = ScholarshipApplication.objects.get(id=application_id)
        application.delete()
        return JsonResponse({'success': True})
    except ScholarshipApplication.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Application not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
