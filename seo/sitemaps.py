from django.contrib.sitemaps import Sitemap
from .models import Region, Subregion

class RegionSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Region.objects.all()

    def location(self, obj):
        return f"/area/{obj.name}/"


class SubregionSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Subregion.objects.select_related("region").all()

    def location(self, obj):
        return f"/area/{obj.region.name}/{obj.name}/"
