# JewelHub - Django Jewellery E-commerce

<p align="center">
	<b>Modern jewellery store built with Django, Razorpay payments, dynamic product discovery, and polished storefront UX.</b>
</p>

<p align="center">
	<img alt="Python" src="https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white">
	<img alt="Django" src="https://img.shields.io/badge/Django-6.0.3-092E20?logo=django&logoColor=white">
	<img alt="Supabase" src="https://img.shields.io/badge/Database-Supabase-3ECF8E?logo=supabase&logoColor=white">
	<img alt="Razorpay" src="https://img.shields.io/badge/Payments-Razorpay-0C2451">
	<img alt="Bootstrap" src="https://img.shields.io/badge/UI-Bootstrap-7952B3?logo=bootstrap&logoColor=white">
</p>

---

## Why This Project

JewelHub is a complete jewellery e-commerce application focused on:

- Elegant storefront experience
- Authentication and profile management
- Cart and checkout workflows
- Razorpay online payment integration
- Cash on Delivery support
- Contact form with SMTP email delivery
- Policy pages and enhanced footer navigation
- Dynamic shop search and category filtering

---

## Core Features

### Storefront
- Dynamic home page with featured categories and products
- Product detail pages with related products
- Category-wise product browsing
- Dynamic shop page with live search query support (`q`) and category filter

### User & Account
- Register / Login / Logout
- Profile and address management
- Password change and password reset flows

### Cart & Orders
- Add to cart / remove / quantity increment and decrement
- Shipping address selection at checkout
- Order creation and order history

### Payments
- Razorpay checkout integration
- HMAC signature verification on backend
- Session-based checkout state management
- COD fallback flow

### Contact & Policies
- Contact Us page with SMTP-backed email notifications
- Styled HTML email body for admin notifications
- Shipping Policy, Privacy Policy, Return Policy, Terms & Conditions pages

### UI/UX Improvements
- Header floating search overlay (click to expand)
- Footer social links and policy navigation
- Rupee currency display across storefront

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 6.0.3 |
| Database | Supabase PostgreSQL |
| Payments | Razorpay |
| Email | SMTP (Gmail) |
| Frontend | Bootstrap + jQuery + custom CSS |
| Admin Theme | django-jazzmin |

---

## Project Structure

```text
Jewellery Project/
|- jewelryshop/
|  |- settings.py
|  |- urls.py
|  |- static/
|- store/
|  |- models.py
|  |- views.py
|  |- urls.py
|  |- forms.py
|  |- migrations/
|- templates/
|  |- base.html
|  |- navbar.html
|  |- footer.html
|  |- store/
|  |- account/
|  |- emails/
|- media/
|- requirements.txt
|- .env
|- manage.py
```

---

## Local Setup

### 1. Clone and enter project

```bash
git clone <your-repo-url>
cd "Jewellery Project"
```

### 2. Create and activate virtual environment

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create `.env` in project root.

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
EMAIL_TIMEOUT=30
EMAIL_HOST_USER=YOUR_SMTP_USERNAME
EMAIL_HOST_PASSWORD=YOUR_GMAIL_APP_PASSWORD
DEFAULT_FROM_EMAIL=YOUR_FROM_EMAIL
CONTACT_RECEIVER_EMAIL=YOUR_RECEIVER_EMAIL

DATABASE_URL=postgresql://postgres.<project-ref>:<db-password>@aws-0-<region>.pooler.supabase.com:6543/postgres?sslmode=require
# Optional alternative if DATABASE_URL is not set
DB_NAME=postgres
DB_USER=postgres.<project-ref>
DB_PASSWORD=YOUR_SUPABASE_DB_PASSWORD
DB_HOST=aws-0-<region>.pooler.supabase.com
DB_PORT=6543
DB_SSL_REQUIRE=True
```

### 5. Apply migrations and run server

```bash
python manage.py migrate
python manage.py runserver 3000
```

Open: `http://127.0.0.1:3000`

---

## Payment Configuration

Razorpay keys are configured in [jewelryshop/settings.py](jewelryshop/settings.py).

For production:
- Replace test keys with live keys
- Enable HTTPS
- Set production-safe `ALLOWED_HOSTS`
- Disable `DEBUG`

---

## Search Experience

Header search opens as a floating overlay and routes to:

`/shop/?q=<search_term>`

Dynamic shop page supports:
- query by product title/description/SKU/category
- category filter via query params
- empty state feedback
- add-to-cart directly from results

---

## Contact Email Flow

When users submit the Contact form:

1. Backend validates required fields
2. Sends multipart email (plain + styled HTML)
3. Uses `reply_to` as customer email
4. Receiver gets formatted notification with all details

Email template path: [templates/emails/contact_notification.html](templates/emails/contact_notification.html)

---

## Useful Commands

```bash
python manage.py check
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 3000
```

---

## Troubleshooting

### Search does not return expected products
- Verify products are active (`is_active=True`)
- Check query string in URL

### Contact email not sending
- Confirm Gmail app password in `.env`
- Verify SMTP settings
- Run `python manage.py check`

### Static assets not loading
- Ensure `STATIC_URL` and `STATICFILES_DIRS` are configured
- Hard refresh browser cache

---

## Security Notes

- Do not commit `.env`
- Keep payment secrets private
- Rotate credentials before production launch
- Use HTTPS and secure cookie settings in production

---

## Current Status

Project is functional and ready for:
- local development
- feature iteration
- staging deployment after environment hardening

---

## Future Enhancements

- Product sorting on shop page (price/newest/popularity)
- Wishlist persistence
- Coupon and discount engine
- Order emails to customers
- Admin analytics dashboard

---

## Maintainer

Built and customized for JewelHub storefront workflows.
