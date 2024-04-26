from django.conf import settings
from django.core.mail import send_mail

from collect_money.celery import app


@app.task(bind=True)
def send_message_user(self, subject: str, body: str, mail: str) -> None:
    '''Отправить сообщение на почту.'''

    try:
        send_mail(
            subject,
            body,
            settings.EMAIL_HOST_USER,
            [f'{mail}'],
            fail_silently=False,
        )
    except Exception:
        return self.retry(countdown=300)
