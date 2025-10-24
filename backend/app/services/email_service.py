"""Email service for sending emails via SMTP"""
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional
from jinja2 import Template
from app.core.config import settings

logger = logging.getLogger(__name__)


class EmailService:
    """Service for sending emails"""

    def __init__(self):
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.from_email = settings.EMAIL_FROM
        self.from_name = settings.APP_NAME

    def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None
    ) -> bool:
        """
        Send an email

        Args:
            to_email: Recipient email address
            subject: Email subject
            html_content: HTML content of the email
            text_content: Plain text content (optional)

        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = f"{self.from_name} <{self.from_email}>"
            message["To"] = to_email

            # Add plain text part
            if text_content:
                part1 = MIMEText(text_content, "plain")
                message.attach(part1)

            # Add HTML part
            part2 = MIMEText(html_content, "html")
            message.attach(part2)

            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(message)

            logger.info(f"Email sent successfully to {to_email}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False

    def send_verification_email(
        self,
        to_email: str,
        user_name: str,
        verification_code: str
    ) -> bool:
        """
        Send email verification code

        Args:
            to_email: User email address
            user_name: User's full name
            verification_code: 6-digit OTP code

        Returns:
            bool: True if email sent successfully
        """
        subject = "Verify your ZIP Platform email"

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background-color: #2563eb;
                    color: white;
                    padding: 20px;
                    text-align: center;
                    border-radius: 5px 5px 0 0;
                }}
                .content {{
                    background-color: #f9fafb;
                    padding: 30px;
                    border-radius: 0 0 5px 5px;
                }}
                .code-box {{
                    background-color: white;
                    border: 2px dashed #2563eb;
                    padding: 20px;
                    text-align: center;
                    font-size: 32px;
                    font-weight: bold;
                    letter-spacing: 5px;
                    margin: 20px 0;
                    color: #2563eb;
                }}
                .footer {{
                    margin-top: 20px;
                    padding-top: 20px;
                    border-top: 1px solid #e5e7eb;
                    font-size: 12px;
                    color: #6b7280;
                    text-align: center;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>ZIP Platform</h1>
                </div>
                <div class="content">
                    <h2>Hi {user_name},</h2>
                    <p>Thank you for registering with ZIP Platform. Please use the verification code below to verify your email address:</p>

                    <div class="code-box">
                        {verification_code}
                    </div>

                    <p><strong>This code will expire in 10 minutes.</strong></p>

                    <p>If you didn't request this verification, please ignore this email.</p>

                    <p>Best regards,<br>ZIP Platform Team</p>
                </div>
                <div class="footer">
                    <p>&copy; 2025 ZIP Platform. All rights reserved.</p>
                    <p>Accra, Ghana</p>
                </div>
            </div>
        </body>
        </html>
        """

        text_content = f"""
        Hi {user_name},

        Thank you for registering with ZIP Platform.

        Your verification code is: {verification_code}

        This code will expire in 10 minutes.

        If you didn't request this verification, please ignore this email.

        Best regards,
        ZIP Platform Team
        """

        return self.send_email(to_email, subject, html_content, text_content)

    def send_password_reset_email(
        self,
        to_email: str,
        user_name: str,
        reset_token: str
    ) -> bool:
        """
        Send password reset email

        Args:
            to_email: User email address
            user_name: User's full name
            reset_token: Password reset token

        Returns:
            bool: True if email sent successfully
        """
        subject = "Reset your ZIP Platform password"
        reset_link = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background-color: #2563eb;
                    color: white;
                    padding: 20px;
                    text-align: center;
                    border-radius: 5px 5px 0 0;
                }}
                .content {{
                    background-color: #f9fafb;
                    padding: 30px;
                    border-radius: 0 0 5px 5px;
                }}
                .button {{
                    display: inline-block;
                    padding: 12px 30px;
                    background-color: #2563eb;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                    margin: 20px 0;
                }}
                .footer {{
                    margin-top: 20px;
                    padding-top: 20px;
                    border-top: 1px solid #e5e7eb;
                    font-size: 12px;
                    color: #6b7280;
                    text-align: center;
                }}
                .warning {{
                    background-color: #fef3c7;
                    border-left: 4px solid #f59e0b;
                    padding: 15px;
                    margin: 20px 0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>ZIP Platform</h1>
                </div>
                <div class="content">
                    <h2>Hi {user_name},</h2>
                    <p>We received a request to reset your password. Click the button below to reset it:</p>

                    <center>
                        <a href="{reset_link}" class="button">Reset Password</a>
                    </center>

                    <p>Or copy and paste this link into your browser:</p>
                    <p style="word-break: break-all; color: #2563eb;">{reset_link}</p>

                    <div class="warning">
                        <strong>⚠️ Security Notice:</strong>
                        <p>This link will expire in 1 hour. If you didn't request a password reset, please ignore this email or contact support if you're concerned about your account's security.</p>
                    </div>

                    <p>Best regards,<br>ZIP Platform Team</p>
                </div>
                <div class="footer">
                    <p>&copy; 2025 ZIP Platform. All rights reserved.</p>
                    <p>Accra, Ghana</p>
                </div>
            </div>
        </body>
        </html>
        """

        text_content = f"""
        Hi {user_name},

        We received a request to reset your password.

        Click this link to reset your password:
        {reset_link}

        This link will expire in 1 hour.

        If you didn't request a password reset, please ignore this email.

        Best regards,
        ZIP Platform Team
        """

        return self.send_email(to_email, subject, html_content, text_content)

    def send_welcome_email(
        self,
        to_email: str,
        user_name: str
    ) -> bool:
        """Send welcome email to new users"""
        subject = "Welcome to ZIP Platform!"

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background-color: #2563eb;
                    color: white;
                    padding: 20px;
                    text-align: center;
                    border-radius: 5px 5px 0 0;
                }}
                .content {{
                    background-color: #f9fafb;
                    padding: 30px;
                    border-radius: 0 0 5px 5px;
                }}
                .features {{
                    background-color: white;
                    padding: 20px;
                    margin: 20px 0;
                    border-radius: 5px;
                }}
                .feature-item {{
                    padding: 10px 0;
                }}
                .button {{
                    display: inline-block;
                    padding: 12px 30px;
                    background-color: #2563eb;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                    margin: 20px 0;
                }}
                .footer {{
                    margin-top: 20px;
                    padding-top: 20px;
                    border-top: 1px solid #e5e7eb;
                    font-size: 12px;
                    color: #6b7280;
                    text-align: center;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Welcome to ZIP Platform!</h1>
                </div>
                <div class="content">
                    <h2>Hi {user_name},</h2>
                    <p>Welcome aboard! We're excited to have you as part of the ZIP Platform family.</p>

                    <div class="features">
                        <h3>What you can do with ZIP:</h3>
                        <div class="feature-item">🔧 <strong>Mobile Car Maintenance</strong> - Book professional technicians to come to you</div>
                        <div class="feature-item">🚗 <strong>Car Rentals</strong> - Rent vehicles for any duration</div>
                        <div class="feature-item">🛒 <strong>Auto Parts Store</strong> - Shop for genuine auto parts and accessories</div>
                    </div>

                    <center>
                        <a href="{settings.FRONTEND_URL}" class="button">Get Started</a>
                    </center>

                    <p>If you have any questions, our support team is here to help!</p>

                    <p>Best regards,<br>ZIP Platform Team</p>
                </div>
                <div class="footer">
                    <p>&copy; 2025 ZIP Platform. All rights reserved.</p>
                    <p>Accra, Ghana</p>
                </div>
            </div>
        </body>
        </html>
        """

        return self.send_email(to_email, subject, html_content)


# Singleton instance
email_service = EmailService()
