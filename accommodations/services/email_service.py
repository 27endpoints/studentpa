from django.core.mail import EmailMessage
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class EmailSubmissionService:
    @staticmethod
    def send_pdf_submission(user, pdf_file, message=None):
        """
        Send PDF submission via email

        
        """
         # Check if email is configured
        if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
            logger.error("Email configuration is missing.")
            return False

        try:
            subject = f"📄 Proof of Payment - {user.username}"
            
            # Build email body step by step
            body_parts = [
                "New Proof of Payment Submission Received!",
                "",
                "Landlord Details:",
                f"- Username: {user.username}",
                f"- Full Name: {user.get_full_name() or 'Not provided'}",
                f"- Email: {user.email}",
                f"- Company: {getattr(user.landlordprofile, 'company_name', 'Not provided')}",
                f"- Phone: {getattr(user.landlordprofile, 'phone_number', 'Not provided')}",
                ""
            ]
            
            # Add message if provided
            if message:
                body_parts.extend([
                    "Additional Message:",
                    message,
                    ""
                ])
            
            # Add file details
            body_parts.extend([
                f"File: {pdf_file.name}",
                f"Size: {pdf_file.size / (1024*1024):.2f} MB",
                "",
                "---",
                "This submission was sent from StudentPA Landlord Dashboard."
            ])
            
            # Join all parts
            body = "\n".join(body_parts)
            
            # Create email
            email = EmailMessage(
                subject=subject,
                body=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.ADMIN_EMAIL],
            )
            
            # Attach the PDF file
            email.attach(pdf_file.name, pdf_file.read(), 'application/pdf')
            
            # Send email
            email.send(fail_silently=False)
            
            logger.info(f"PDF submission sent successfully for user {user.username}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send PDF submission: {e}")
            return False