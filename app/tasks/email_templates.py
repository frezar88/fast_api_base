from datetime import datetime
from email.message import EmailMessage

from pydantic import EmailStr

from app.config import settings


def create_booking_confirmation_template(
        booking: dict,
        email_to: EmailStr
):
    email = EmailMessage()
    email['Subject'] = "Подтверждение бронирования"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to

    email.set_content(f"""
    <h1>Подтвердите бронирование</h1>
    Вы забронировали отель с {datetime.strptime(booking['date_from'], '%Y-%m-%d')}
    по {datetime.strptime(booking['date_to'], '%Y-%m-%d')}
    """,
                      subtype="html")

    return email
