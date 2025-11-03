from django.core.management.base import BaseCommand
from accommodations.models import SiteContent
from datetime import datetime

class Command(BaseCommand):
    help = 'Create initial site content pages'
    
    def handle(self, *args, **options):
        current_date = datetime.now().strftime("%B %d, %Y")
        
        initial_content = [
            {
                'content_type': 'terms',
                'title': 'Terms and Conditions',
                'content': f'''
<h1>Terms and Conditions</h1>

<p><strong>Last Updated:</strong> {current_date}</p>

<h2>1. Acceptance of Terms</h2>
<p>By accessing and using StudentPA, you accept and agree to be bound by the terms and provision of this agreement.</p>

<h2>2. Use License</h2>
<p>Permission is granted to temporarily use StudentPA for personal, non-commercial transitory viewing only.</p>

<h2>3. Account Responsibilities</h2>
<ul>
    <li>You are responsible for maintaining the confidentiality of your account</li>
    <li>You must be at least 18 years old to create an account</li>
    <li>You agree to provide accurate and complete information</li>
</ul>

<h2>4. Landlord Responsibilities</h2>
<p><i>Landlords agree to:</i></p>
<ul>
    <li>Provide accurate property information</li>
    <li>Respond to student inquiries in a timely manner</li>
    <li>Maintain safe and habitable accommodations</li>
</ul>

<h2>5. Student Responsibilities</h2>
<p><u>Students agree to:</u></p>
<ul>
    <li>Follow all safety guidelines when viewing properties</li>
    <li>Provide accurate personal information</li>
    <li>Respect landlord properties and viewing appointments</li>
</ul>

<h2>6. Limitation of Liability</h2>
<p>StudentPA shall not be held liable for any interactions between students and landlords.</p>
'''
            },
            {
                'content_type': 'privacy',
                'title': 'Privacy Policy',
                'content': f'''
<h1>Privacy Policy</h1>

<p><strong>Last Updated:</strong> {current_date}</p>

<h2>1. Information We Collect</h2>
<p>We collect information you provide directly to us, including:</p>
<ul>
    <li><b>Account Information:</b> Name, email, phone number</li>
    <li><b>Property Information:</b> Accommodation details, photos</li>
    <li><b>Usage Data:</b> How you use our platform</li>
</ul>

<h2>2. How We Use Your Information</h2>
<p>We use the information we collect to:</p>
<ul>
    <li>Provide and maintain our service</li>
    <li>Notify you about changes to our service</li>
    <li>Allow you to participate in interactive features</li>
    <li>Provide customer support</li>
</ul>

<h2>3. Data Sharing</h2>
<p>We may share your information in the following situations:</p>
<ul>
    <li><i>With Landlords:</i> Student contact information for property inquiries</li>
    <li><i>With Students:</i> Landlord contact information for property viewing</li>
    <li><i>With Service Providers:</i> To monitor and analyze platform usage</li>
</ul>

<h2>4. Data Security</h2>
<p>We implement appropriate security measures to protect your personal information.</p>

<h2>5. Your Rights</h2>
<p>You have the right to:</p>
<ul>
    <li>Access and update your personal information</li>
    <li>Delete your account and associated data</li>
    <li>Opt-out of marketing communications</li>
</ul>
'''
            }
        ]
        
        for content_data in initial_content:
            content_type = content_data['content_type']
            
            obj, created = SiteContent.objects.get_or_create(
                content_type=content_type,
                defaults=content_data
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created {content_type} content')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'{content_type} content already exists')
                )