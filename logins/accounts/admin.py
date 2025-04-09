from django.contrib import admin
from django.db.models import Sum
from .models import Donation, ScholarshipApplication, Contact

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'amount', 'date')
    list_filter = ('date',)
    search_fields = ('user__username', 'first_name', 'last_name', 'email')
    readonly_fields = ('date',)
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        self.total_donations = queryset.aggregate(total=Sum('amount'))['total'] or 0
        return queryset
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['total_donations'] = self.get_queryset(request).aggregate(total=Sum('amount'))['total'] or 0
        return super().changelist_view(request, extra_context=extra_context)

@admin.register(ScholarshipApplication)
class ScholarshipApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'student_id', 'college_name', 'degree', 'semester_fee', 'date_submitted', 'application_status')
    list_filter = ('date_submitted', 'degree', 'application_status')
    search_fields = ('full_name', 'student_id', 'college_name', 'email')
    readonly_fields = ('date_submitted',)
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('user', 'full_name', 'email', 'date_of_birth', 'student_id')
        }),
        ('Family Details', {
            'fields': ('father_name', 'mother_name', 'siblings')
        }),
        ('Address Information', {
            'fields': ('address', 'district', 'state', 'country')
        }),
        ('Educational Details', {
            'fields': ('college_name', 'degree', 'department_head_contact', 'semester_fee')
        }),
        ('Documents', {
            'fields': ('aadhar_card', 'pan_card', 'bank_passbook', 'college_bonafide', 'extracurricular_certificate')
        }),
        ('Status', {
            'fields': ('application_status',)
        })
    )

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'subject', 'created_at')
    list_filter = ('created_at', 'subject')
    search_fields = ('first_name', 'last_name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)