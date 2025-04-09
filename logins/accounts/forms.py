from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Donation, ScholarshipApplication

# User Signup Form
class SignupForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
        }

# Donation Form
class DonationForm(forms.ModelForm):
    date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        required=True
    )

    class Meta:
        model = Donation
        fields = '__all__'
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Last Name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
            'aadhar': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Aadhar Number'}),
            'pancard': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter PAN Number'}),
            'permanent_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Permanent Address'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Country'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter State'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter City'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Pincode'}),
        }

    # Phone number validation
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.isdigit() or len(phone_number) != 10:
            raise ValidationError("Phone number must be exactly 10 digits.")
        return phone_number

    # Aadhar number validation
    def clean_aadhar(self):
        aadhar = self.cleaned_data.get('aadhar')
        if aadhar and (not aadhar.isdigit() or len(aadhar) != 12):
            raise ValidationError("Aadhar number must be exactly 12 digits.")
        return aadhar

    # PAN card validation
    def clean_pancard(self):
        pancard = self.cleaned_data.get('pancard')
        if len(pancard) != 10 or not pancard[:5].isalpha() or not pancard[5:9].isdigit() or not pancard[9].isalpha():
            raise ValidationError("PAN must be in the format: AAAAA1111A.")
        return pancard

class ScholarshipForm(forms.ModelForm):
    class Meta:
        model = ScholarshipApplication
        fields = [
            'full_name', 'email', 'mobile_number', 'date_of_birth', 'student_id',
            'father_name', 'mother_name', 'siblings',
            'address', 'district', 'state', 'country',
            'college_name', 'degree', 'department_head_contact',
            'semester_fee', 'aadhar_card', 'pan_card',
            'bank_passbook', 'college_bonafide', 'extracurricular_certificate'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'mobile_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter mobile number (e.g., 9876543210)',
                'pattern': '^\+?1?\d{9,15}$'
            }),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'student_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your student ID'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_name': forms.TextInput(attrs={'class': 'form-control'}),
            'siblings': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'college_name': forms.TextInput(attrs={'class': 'form-control'}),
            'degree': forms.TextInput(attrs={'class': 'form-control'}),
            'department_head_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'semester_fee': forms.NumberInput(attrs={'class': 'form-control'}),
            'aadhar_card': forms.FileInput(attrs={'class': 'form-control'}),
            'pan_card': forms.FileInput(attrs={'class': 'form-control'}),
            'bank_passbook': forms.FileInput(attrs={'class': 'form-control'}),
            'college_bonafide': forms.FileInput(attrs={'class': 'form-control'}),
            'extracurricular_certificate': forms.FileInput(attrs={'class': 'form-control'})
        }

    def clean_mobile_number(self):
        mobile_number = self.cleaned_data.get('mobile_number')
        if not mobile_number:
            return mobile_number
            
        # Remove any whitespace
        mobile_number = mobile_number.strip()
        
        # Remove any non-digit characters
        mobile_number = ''.join(filter(str.isdigit, mobile_number))
        
        # Check if it's exactly 10 digits
        if len(mobile_number) != 10:
            raise ValidationError("Mobile number must be exactly 10 digits.")
            
        # Check if it starts with a valid digit (6-9)
        if not mobile_number[0] in ['6', '7', '8', '9']:
            raise ValidationError("Mobile number must start with 6, 7, 8, or 9.")
            
        return mobile_number
