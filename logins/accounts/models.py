from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.core.validators import RegexValidator

class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=50, default="Unknown")
    last_name = models.CharField(max_length=50, default="Unknown")
    phone_number = models.CharField(max_length=10, default="0000000000")
    email = models.EmailField(default="unknown@example.com")
    aadhar = models.CharField(max_length=12, blank=True, null=True, unique=True)
    pancard = models.CharField(max_length=10, default="UNKNOWN", unique=True)
    permanent_address = models.TextField(default="Not Provided")
    country = models.CharField(max_length=50, default="Unknown")
    state = models.CharField(max_length=50, default="Unknown")
    city = models.CharField(max_length=50, default="Unknown")
    pincode = models.CharField(max_length=10, default="000000")
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    date = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.amount} Donation"

class ScholarshipApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    mobile_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    date_of_birth = models.DateField()
    date_submitted = models.DateTimeField(auto_now_add=True)
    application_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Family details
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    siblings = models.TextField(blank=True, null=True)

    # Address details
    address = models.TextField()
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100, default="Unknown")
    country = models.CharField(max_length=100, default="Unknown")
    student_id = models.CharField(max_length=50, unique=True)
    college_name = models.CharField(max_length=200)
    degree = models.CharField(max_length=100)
    department_head_contact = models.CharField(max_length=15)
    semester_fee = models.DecimalField(max_digits=10, decimal_places=2)

    # Document uploads
    aadhar_card = models.FileField(upload_to='documents/aadhar_cards/', blank=True, null=True)
    pan_card = models.FileField(upload_to='documents/pan_cards/', blank=True, null=True)
    bank_passbook = models.FileField(upload_to='documents/bank_passbooks/', blank=True, null=True)
    college_bonafide = models.FileField(upload_to='documents/college_bonafides/', blank=True, null=True)
    extracurricular_certificate = models.FileField(upload_to='documents/extracurricular_certificates/', blank=True, null=True)

    def __str__(self):
        return f"Scholarship Application - {self.full_name}"

class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.subject}"

    class Meta:
        ordering = ['-created_at']
