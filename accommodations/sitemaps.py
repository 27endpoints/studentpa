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
            # Authentication
            "login",
            "logout",
            "register",
            "register_role_selection",
            "register_student",
            "register_landlord",
            
            # Accommodation
            "accommodation_list",
            "accommodation_detail",  # note: detail pages are dynamic, we'll handle separately
            "landlord_dashboard",
            "landlord_profile_update",
            "accommodation_create",
            "accommodation_update",
            "accommodation_delete",
            "accommodation_preview",
            
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