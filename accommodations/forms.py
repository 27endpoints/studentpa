from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Accommodation, AccommodationImage, StudentProfile, LandlordProfile, Location
from django_recaptcha.fields import ReCaptchaField
from django.core.validators import FileExtensionValidator

class RoleSelectionForm(forms.Form):
    ROLE_CHOICES = [
        ('student', 'Student - Looking for accommodation'),
        ('landlord', 'Landlord - Want to list accommodations'),
    ]
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.RadioSelect,
        required=True
    )


class CustomUserCreationForm(UserCreationForm):
    # captcha = ReCaptchaField()
    email = forms.EmailField(required=False)   #for future use
    last_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'password1', 'password2']

class StudentRegistrationForm(CustomUserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    phone_number = forms.CharField(max_length=20, required=False)  #for future use
    university = forms.CharField(max_length=100, required=False)  #for future use

    class Meta(CustomUserCreationForm.Meta):
        pass

class LandlordRegistrationForm(CustomUserCreationForm):
    phone_number = forms.CharField(max_length=20, required=False)
    company_name = forms.CharField(max_length=100, required=False)

    class Meta(CustomUserCreationForm.Meta):
        pass

class AccommodationForm(forms.ModelForm):
    class Meta:
        model = Accommodation
        fields = ['description', 'room_type', 'price', 'location', 'available_rooms']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'room_type': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'location': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'title': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'price': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'available_rooms': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
        }

class AccommodationImageForm(forms.ModelForm):
    class Meta:
        model = AccommodationImage
        fields = ['image', 'is_primary']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
        }

class AccommodationWithImagesForm(forms.Form):
    # Accommodation fields
    description = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-md',
        'rows': 4,
        'placeholder': 'Describe your accommodation...'
    }))
    room_type = forms.ChoiceField(choices=Accommodation.ROOM_TYPES, widget=forms.Select(attrs={
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'
    }))
    price = forms.DecimalField(widget=forms.NumberInput(attrs={
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-md',
        'placeholder': '450'
    }))
    location = forms.ModelChoiceField(queryset=None, widget=forms.Select(attrs={
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'
    }))
    available_rooms = forms.IntegerField(initial=1, widget=forms.NumberInput(attrs={
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'
    }))

    # Image fields - allow up to 5 images
    image_1 = forms.ImageField(required=True, widget=forms.FileInput(attrs={
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'
    }))
    image_2 = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'
    }))
    image_3 = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'
    }))


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['location'].queryset = Location.objects.all()


class PDFSubmissionForm(forms.Form):
    pdf_file = forms.FileField(
        label='Upload Proof of Payment',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        widget=forms.FileInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md',
            'accept': '.pdf'
        })
    )
    message = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md',
            'rows': 3,
            'placeholder': 'Optional message or notes...'
        })
    )
    
    def clean_pdf_file(self):
        pdf_file = self.cleaned_data.get('pdf_file')
        if pdf_file:
            # Check file size (10MB limit)
            if pdf_file.size > 10 * 1024 * 1024:
                raise forms.ValidationError("File size must be under 10MB")
            
            # Basic PDF validation
            if not pdf_file.name.lower().endswith('.pdf'):
                raise forms.ValidationError("Only PDF files are allowed")
                
        return pdf_file

