from django.contrib import admin
from django.contrib.auth.models import Group
from accommodations import forms
from django import forms
from .models import Accommodation, Location, AccommodationImage, LandlordProfile, StudentProfile, SiteContent
from django.db import models




class AccommodationImageInline(admin.TabularInline):
    model = AccommodationImage
    extra = 1

@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    list_display = [ 'landlord','is_featured', 'location', 'price', 'available_rooms', 'is_approved', 'is_available']
    list_filter = ['is_approved', 'room_type', 'location', 'created_at']
    list_editable = ['is_approved', 'is_featured', 'available_rooms']
    search_fields = ['description', 'landlord__username']
    inlines = [AccommodationImageInline]
    actions = ['approve_accommodations', 'disapprove_accommodations']

    def approve_accommodations(self, request, queryset):
        queryset.update(is_approved=True)
    approve_accommodations.short_description = "Approve selected accommodations"

    def disapprove_accommodations(self, request, queryset):
        queryset.update(is_approved=False)
    disapprove_accommodations.short_description = "Disapprove selected accommodations"

    def feature_accommodations(self, request, queryset):
        queryset.update(is_featured=True)
    feature_accommodations.short_description = "Mark selected as featured"

    def unfeature_accommodations(self, request, queryset):
        queryset.update(is_featured=False)
    unfeature_accommodations.short_description = "Remove featured from selected"


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(AccommodationImage)
class AccommodationImageAdmin(admin.ModelAdmin):
    list_display = ['accommodation', 'image', 'is_primary']
    list_filter = ['is_primary']

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'university', 'phone_number', 'created_at']
    list_filter = ['university', 'created_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'university']

@admin.register(LandlordProfile)
class LandlordProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'company_name', 'is_verified', 'created_at']
    list_filter = ['is_verified', 'created_at']
    search_fields = ['user__username', 'company_name']
    actions = ['verify_landlords', 'unverify_landlords']

    def verify_landlords(self, request, queryset):
        queryset.update(is_verified=True)
    verify_landlords.short_description = "Verify selected landlords"

    def unverify_landlords(self, request, queryset):
        queryset.update(is_verified=False)
    unverify_landlords.short_description = "Unverify selected landlords"

# Create landlord group in admin
def create_landlord_group():
    group, created = Group.objects.get_or_create(name='Landlords')
    return group



class SiteContentForm(forms.ModelForm):
    class Meta:
        model = SiteContent
        fields = '__all__'
        widgets = {
            'content': forms.Textarea(attrs={'rows': 30, 'cols': 100, 'style': 'font-family: monospace;'}),
        }

@admin.register(SiteContent)
class SiteContentAdmin(admin.ModelAdmin):
    form = SiteContentForm
    list_display = ['content_type', 'title', 'last_updated', 'is_active']
    list_editable = ['is_active']
    list_filter = ['content_type', 'is_active']
    readonly_fields = ['last_updated']

    fieldsets = (
        (None, {
            'fields': ('content_type', 'title', 'is_active')
        }),
        ('Content', {
            'fields': ('content',),
            'description': '''
            <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 15px; border-left: 4px solid #3b82f6;">
                <h4 style="margin-top: 0; color: #000000;">HTML Styling Guide: Ungathithizi Sbali</h4>
                <div style="display: grid; grid-template-columns: 1fr 1fr; color: #000000; gap: 10px; font-family: monospace; font-size: 14px;">
                    <div>
                        <strong>Text Formatting:</strong><br>
                        &lt;b&gt;<b>bold text</b>&lt;/b&gt;<br>
                        &lt;i&gt;<i>italic text</i>&lt;/i&gt;<br>
                        &lt;u&gt;<u>underlined text</u>&lt;/u&gt;<br>
                        &lt;strong&gt;<strong>strong text</strong>&lt;/strong&gt;<br>
                        &lt;em&gt;<em>emphasized text</em>&lt;/em&gt;
                    </div>
                    <div>
                        <strong>Headings:</strong><br>
                        &lt;h1&gt;Main Title&lt;/h1&gt;<br>
                        &lt;h2&gt;Section Title&lt;/h2&gt;<br>
                        &lt;h3&gt;Subsection&lt;/h3&gt;<br>
                        &lt;h4&gt;Small Heading&lt;/h4&gt;
                    </div>
                    <div>
                        <strong>Lists:</strong><br>
                        &lt;ul&gt;<br>
                        &nbsp;&lt;li&gt;item 1&lt;/li&gt;<br>
                        &nbsp;&lt;li&gt;item 2&lt;/li&gt;<br>
                        &lt;/ul&gt;<br>
                        &lt;ol&gt;<br>
                        &nbsp;&lt;li&gt;item 1&lt;/li&gt;<br>
                        &nbsp;&lt;li&gt;item 2&lt;/li&gt;<br>
                        &lt;/ol&gt;
                    </div>
                    <div>
                        <strong>Other Elements:</strong><br>
                        &lt;p&gt;paragraph&lt;/p&gt;<br>
                        &lt;br&gt; (line break)<br>
                        &lt;a href="url"&gt;link&lt;/a&gt;<br>
                        &lt;hr&gt; (horizontal line)
                    </div>
                </div>
            </div>
            '''
        }),
    )

