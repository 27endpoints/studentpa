from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class SiteContent(models.Model):
    CONTENT_TYPES = [
        ('terms', 'Terms and Conditions'),
        ('privacy', 'Privacy Policy'),
        ('about', 'About Us'),
        ('safety', 'Safety Guidelines'),
    ]

    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES, unique=True)
    title = models.CharField(max_length=200)
    content = models.TextField(help_text="You can use HTML tags for styling: <b>bold</b>, <i>italic</i>, <u>underline</u>, <ul><li>lists</li></ul>, <h1>-<h6> headings, etc.")
    last_updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Site Content"
        verbose_name_plural = "Site Contents"

    def __str__(self):
        return f"{self.get_content_type_display()} - {self.title}"

class Location(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True) #for future use
    university = models.CharField(max_length=100, blank=True)   #for future use
    course = models.CharField(max_length=100, blank=True)    #for future use
    year_of_study = models.PositiveIntegerField(null=True, blank=True)  #for future use
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - Student"

class LandlordProfile(models.Model):

    TITLE_CHOICES = [
        ('Mr', 'Mr'),
        ('M.s', 'M.s'),
        ('Mrs', 'Mrs'),

    ]

    title = models.CharField(
        max_length=5, # Sufficient for 'M.s' or 'Mrs'
        choices=TITLE_CHOICES,
        default='Mr',
        blank=False,
        null=False
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True)
    company_name = models.CharField(max_length=100, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Landlord"

class Accommodation(models.Model):
    ROOM_TYPES = [
        ('single', 'Single Room'),
        ('double', 'Double Room'),
        ('triple', 'Triple+ Room'),

    ]

    landlord = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=2000)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    available_rooms = models.PositiveIntegerField(default=1)
    is_approved = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)

    @property
    def is_available(self):
        return self.available_rooms > 0 and self.is_approved

    def __str__(self):
        return f"{self.landlord.landlordprofile.company_name} - {self.location}"
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("accommodation_detail", kwargs={"pk": self.pk})

class AccommodationImage(models.Model):
    accommodation = models.ForeignKey(Accommodation, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='accommodations/')
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.accommodation.title}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Profile will be created in the registration view based on role
        pass

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Check if profiles exist before saving
    if hasattr(instance, 'studentprofile'):
        instance.studentprofile.save()
    if hasattr(instance, 'landlordprofile'):
        instance.landlordprofile.save()