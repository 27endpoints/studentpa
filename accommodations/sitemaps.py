from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.contrib.sitemaps import Sitemap
from .models import Accommodation 



class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        # List all named URLs that should appear in the sitemap
        return [
            
            # Accommodation
            "home",
            "accommodation_list",
            "landlord_dashboard",
            "landlord_profile_update",
            "accommodation_create",
            
            # Content pages
            "terms_and_conditions",
            "privacy_policy",
            "about_us",
            "safety_guidelines",
        ]

    def location(self, item):
        return reverse(item)


class AccommodationSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Accommodation.objects.all()  

    def location(self, obj):
        return obj.get_absolute_url()  