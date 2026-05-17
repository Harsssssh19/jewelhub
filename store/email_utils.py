from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def _format_details(details):
    if not details:
        return []
    return [(label, value) for label, value in details.items()]


def send_templated_email(*, subject, to_email, template_name, context=None, from_email=None, admin_copy=False):
    context = context or {}
    from_email = from_email or settings.DEFAULT_FROM_EMAIL

    html_body = render_to_string(template_name, context)
    text_body = strip_tags(html_body)

    recipients = [to_email]
    if admin_copy and settings.CONTACT_RECEIVER_EMAIL:
        recipients.append(settings.CONTACT_RECEIVER_EMAIL)

    message = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=from_email,
        to=recipients,
    )
    message.attach_alternative(html_body, "text/html")
    message.send(fail_silently=False)


def _order_action_for_status(status):
    status = (status or "").strip()
    status_map = {
        'Pending': ('Order received', 'We have received your order and will start processing it soon.', 'View your orders'),
        'Accepted': ('Order accepted', 'Your order has been accepted and is being prepared.', 'View your orders'),
        'Packed': ('Order packed', 'Your order has been packed and is ready for dispatch.', 'View your orders'),
        'On The Way': ('Order shipped', 'Your order is on the way to you.', 'Track your order'),
        'Delivered': ('Order delivered', 'Your order has been delivered successfully.', 'Review your order'),
        'Cancelled': ('Order cancelled', 'Your order has been cancelled. If you need help, please contact support.', 'Continue shopping'),
    }
    return status_map.get(status, ('Order updated', 'Your JewelHub order has been updated.', 'View your orders'))


def send_registration_email(user):
    if not user.email:
        return

    send_templated_email(
        subject="Welcome to JewelHub",
        to_email=user.email,
        template_name="emails/registration_welcome.html",
        context={
            "user": user,
            "details": {
                "Username": user.username,
                "Email": user.email,
            },
        },
    )


def send_registration_admin_alert(user):
    if not settings.CONTACT_RECEIVER_EMAIL:
        return

    send_templated_email(
        subject=f"New registration: {user.username}",
        to_email=settings.CONTACT_RECEIVER_EMAIL,
        template_name="emails/admin_notification.html",
        context={
            "title": "New customer registration",
            "intro": "A new user has created an account on JewelHub.",
            "details": {
                "Username": user.username,
                "Email": user.email or "Not provided",
            },
        },
    )


def send_order_email(order, *, status_label="Order received", extra_details=None):
    if not order.user.email:
        return

    details = {
        "Order ID": order.id,
        "Product": order.product.title,
        "Quantity": order.quantity,
        "Status": order.status,
        "Payment": "Paid" if order.payment_status else "Pending / COD",
        "Amount": f"₹{order.order_total}",
    }
    if extra_details:
        details.update(extra_details)

    send_templated_email(
        subject=f"{status_label} - JewelHub order #{order.id}",
        to_email=order.user.email,
        template_name="emails/order_notification.html",
        context={
            "title": status_label,
            "intro": "We have an update about your JewelHub order.",
            "details": details,
            "user": order.user,
            "order": order,
            "action_url": f"{settings.SITE_URL}/orders/",
            "action_label": "View your orders",
            "status_label": status_label,
        },
    )


def send_order_admin_alert(order, action_label="New order placed"):
    if not settings.CONTACT_RECEIVER_EMAIL:
        return

    send_templated_email(
        subject=f"{action_label}: order #{order.id}",
        to_email=settings.CONTACT_RECEIVER_EMAIL,
        template_name="emails/admin_notification.html",
        context={
            "title": action_label,
            "intro": "A store order needs attention.",
            "status_label": action_label,
            "details": {
                "Order ID": order.id,
                "Customer": order.user.get_full_name() or order.user.username,
                "Email": order.user.email or "Not provided",
                "Product": order.product.title,
                "Quantity": order.quantity,
                "Status": order.status,
                "Payment": "Paid" if order.payment_status else "Pending / COD",
            },
        },
    )


def send_order_status_update_email(order, previous_status):
    if not order.user.email:
        return

    status_title, intro, action_label = _order_action_for_status(order.status)

    send_templated_email(
        subject=f"{status_title} - #{order.id}",
        to_email=order.user.email,
        template_name="emails/order_notification.html",
        context={
            "title": status_title,
            "intro": intro,
            "details": {
                "Order ID": order.id,
                "Product": order.product.title,
                "Previous status": previous_status,
                "Current status": order.status,
                "Payment": "Paid" if order.payment_status else "Pending / COD",
            },
            "user": order.user,
            "order": order,
            "action_url": f"{settings.SITE_URL}/orders/",
            "action_label": action_label,
            "status_label": order.status,
        },
    )


def send_password_change_email(user):
    if not user.email:
        return

    send_templated_email(
        subject="Your JewelHub password was changed",
        to_email=user.email,
        template_name="emails/password_change_notification.html",
        context={
            "title": "Password changed",
            "intro": "Your JewelHub account password has been updated successfully.",
            "details": {
                "Username": user.username,
                "Email": user.email,
            },
            "action_url": f"{settings.SITE_URL}/accounts/password-change/",
            "action_label": "Change password again",
        },
    )


def send_password_change_admin_alert(user):
    if not settings.CONTACT_RECEIVER_EMAIL:
        return

    send_templated_email(
        subject=f"Password changed: {user.username}",
        to_email=settings.CONTACT_RECEIVER_EMAIL,
        template_name="emails/admin_notification.html",
        context={
            "title": "Password change notification",
            "intro": "A user changed their JewelHub password.",
            "status_label": "Security update",
            "details": {
                "Username": user.username,
                "Email": user.email or "Not provided",
            },
        },
    )
