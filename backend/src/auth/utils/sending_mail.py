import logging
import smtplib

from src.config import settings


class SendMail:
    @staticmethod
    def _create_link_to_verify(code: str) -> str:
        return f'{settings.BASE_URL}{code}/'

    def _send_verification_mail(
            self,
            email_to_send: str,
            code: str
    ):
        try:
            server = smtplib.SMTP_SSL(
                host=settings.EMAIL_HOST,
                port=settings.EMAIL_PORT
            )
            server.starttls()
            server.login(
                user=settings.FROM,
                password=settings.EMAIL_PASSWORD
            )
            server.sendmail(
                from_addr=settings.FROM,
                to_addrs=email_to_send,
                msg=self._create_link_to_verify(code)
            )
            server.quit()
            logging.info(f'Сообщение отправлено {email_to_send}')
        except smtplib.SMTPException as e:
            logging.error(e)
