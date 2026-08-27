import random
import time

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from properties.models import Property
from .models import Enquiry,VisitorEmail

from django.core.validators import validate_email
from django.core.exceptions import ValidationError
def contact(request):

    property_id = request.GET.get("property")

    selected_property = None

    if property_id:
        selected_property = Property.objects.filter(
            property_id=property_id
        ).first()

    # ==========================================================
    # SEND OTP
    # ==========================================================

    if request.method == "POST" and request.POST.get("action") == "send_otp":

        email = request.POST.get("email", "").strip().lower()

        # Basic email validation
        if not email or "@" not in email or "." not in email.split("@")[-1]:

            return JsonResponse({
                "success": False,
                "message": "Please enter a valid email address."
            }, status=400)

        # Prevent sending OTP again too quickly
        last_sent = request.session.get("otp_sent_at")

        if last_sent:

            if time.time() - float(last_sent) < 60:

                remaining = 60 - int(
                    time.time() - float(last_sent)
                )

                return JsonResponse({
                    "success": False,
                    "message": f"Please wait {remaining} seconds before requesting another OTP."
                }, status=429)

        # Generate 6-digit OTP
        otp = str(
            random.randint(100000, 999999)
        )

        # Save OTP information in session
        request.session["email_otp"] = otp
        request.session["otp_email"] = email
        request.session["otp_created_at"] = time.time()
        request.session["otp_sent_at"] = time.time()
        request.session["otp_attempts"] = 0
        request.session["email_verified"] = False

        try:

            send_mail(

                subject="Prime Estates - Email Verification OTP",

                message=(
                    f"Hello,\n\n"
                    f"Your Prime Estates email verification OTP is:\n\n"
                    f"{otp}\n\n"
                    f"This OTP is valid for 5 minutes.\n\n"
                    f"Please do not share this OTP with anyone.\n\n"
                    f"Thank you,\n"
                    f"Prime Estates"
                ),

                from_email=settings.DEFAULT_FROM_EMAIL,

                recipient_list=[email],

                fail_silently=False,
            )

            return JsonResponse({
                "success": True,
                "message": "OTP has been sent to your email."
            })

        except Exception as error:

            # Remove OTP if email sending failed
            request.session.pop("email_otp", None)
            request.session.pop("otp_email", None)
            request.session.pop("otp_created_at", None)
            request.session.pop("otp_sent_at", None)

            print("EMAIL ERROR:", error)

            return JsonResponse({
                "success": False,
                "message": "Unable to send OTP. Please check your email and try again."
            }, status=500)

    # ==========================================================
    # AUTOMATIC OTP VERIFICATION
    # ==========================================================

    if request.method == "POST" and request.POST.get("action") == "verify_otp":

        entered_otp = request.POST.get(
            "otp",
            ""
        ).strip()

        saved_otp = request.session.get(
            "email_otp"
        )

        otp_email = request.session.get(
            "otp_email"
        )

        otp_created_at = request.session.get(
            "otp_created_at"
        )

        otp_attempts = int(
            request.session.get(
                "otp_attempts",
                0
            )
        )

        # OTP doesn't exist
        if not saved_otp or not otp_created_at:

            return JsonResponse({
                "success": False,
                "verified": False,
                "message": "OTP expired. Please request a new OTP."
            })

        # Maximum attempts
        if otp_attempts >= 5:

            request.session.pop("email_otp", None)
            request.session.pop("otp_email", None)
            request.session.pop("otp_created_at", None)

            return JsonResponse({
                "success": False,
                "verified": False,
                "message": "Too many incorrect attempts. Please request a new OTP."
            })

        # OTP expiry - 5 minutes
        if time.time() - float(otp_created_at) > 300:

            request.session.pop("email_otp", None)
            request.session.pop("otp_email", None)
            request.session.pop("otp_created_at", None)

            return JsonResponse({
                "success": False,
                "verified": False,
                "message": "OTP has expired. Please request a new OTP."
            })

        # Wrong OTP
        if entered_otp != saved_otp:

            otp_attempts += 1

            request.session["otp_attempts"] = otp_attempts

            remaining_attempts = 5 - otp_attempts

            return JsonResponse({
                "success": False,
                "verified": False,
                "message": f"Incorrect OTP. {remaining_attempts} attempts remaining."
            })

        # ======================================================
        # OTP CORRECT
        # ======================================================

        request.session["email_verified"] = True

        return JsonResponse({
            "success": True,
            "verified": True,
            "message": "Email verified successfully."
        })

    # ==========================================================
    # FINAL ENQUIRY SUBMISSION
    # ==========================================================

    if request.method == "POST":

        name = request.POST.get(
            "name",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip().lower()

        phone = request.POST.get(
            "phone",
            ""
        ).strip()

        enquiry_type = request.POST.get(
            "enquiry_type",
            "general"
        )

        message = request.POST.get(
            "message",
            ""
        ).strip()

        property_id = request.POST.get(
            "property_id"
        )

        # ======================================================
        # PHONE VALIDATION
        # ======================================================

        if not phone.isdigit() or len(phone) != 10 or phone[0] not in "6789":

            messages.error(
                request,
                "Please enter a valid 10-digit Indian mobile number."
            )

            return redirect(
                "contact"
            )

        # ======================================================
        # EMAIL VERIFICATION CHECK
        # ======================================================

        email_verified = request.session.get(
            "email_verified",
            False
        )

        verified_email = request.session.get(
            "otp_email"
        )

        if not email_verified:

            messages.error(
                request,
                "Please verify your email address before submitting."
            )

            return redirect(
                "contact"
            )

        # Make sure user didn't change email after verification
        if email != verified_email:

            request.session["email_verified"] = False

            messages.error(
                request,
                "Email address was changed. Please verify the new email address."
            )

            return redirect(
                "contact"
            )

        # ======================================================
        # GET PROPERTY
        # ======================================================

        selected_property = None

        if property_id:

            selected_property = Property.objects.filter(
                property_id=property_id
            ).first()

        # ======================================================
        # CREATE ENQUIRY
        # ======================================================

        Enquiry.objects.create(

            name=name,

            email=email,

            phone=phone,

            enquiry_type=enquiry_type,

            property=selected_property,

            message=message,
        )

        # ======================================================
        # CLEAR OTP DATA
        # ======================================================

        request.session.pop(
            "email_otp",
            None
        )

        request.session.pop(
            "otp_email",
            None
        )

        request.session.pop(
            "otp_created_at",
            None
        )

        request.session.pop(
            "otp_sent_at",
            None
        )

        request.session.pop(
            "otp_attempts",
            None
        )

        request.session.pop(
            "email_verified",
            None
        )

        messages.success(
            request,
            "Thank you! Your email has been verified and our team will contact you shortly."
        )

        return redirect(
            "contact"
        )

    context = {
        "selected_property": selected_property,
    }

    return render(
        request,
        "contact.html",
        context
    )

@require_POST
def save_visitor_email(request):

    try:
        email = request.POST.get("email", "").strip().lower()

        if not email:
            return JsonResponse({
                "success": False,
                "message": "Email is required."
            }, status=400)

        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({
                "success": False,
                "message": "Please enter a valid email address."
            }, status=400)

        visitor_email, created = VisitorEmail.objects.get_or_create(
            email=email
        )

        return JsonResponse({
            "success": True,
            "message": "Email saved successfully."
        })

    except Exception as e:

        print("====================================")
        print("SAVE VISITOR EMAIL ERROR:")
        print(e)
        print("====================================")

        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=500)