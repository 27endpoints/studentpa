from django.shortcuts import render, get_object_or_404
from .models import Region
from django.shortcuts import render, get_object_or_404
from .models import Region, Subregion


def region_page(request, region_name):
    region = get_object_or_404(Region, name__iexact=region_name)
    return render(request, "seo/region_page.html", {"region": region})

def subregion_page(request, region_name, sub_name):
    region = get_object_or_404(Region, name__iexact=region_name)
    subregion = get_object_or_404(Subregion, region=region, name__iexact=sub_name)
    return render(request, "seo/subregion_page.html", {
        "region": region,
        "subregion": subregion
    })
