from src.config import settings


class SendMail:

    @staticmethod
    def _create_link_to_verify(code):
        return f'{settings.BASE_URL}{code}/'

    def _send_verification_mail(self, code):
        pass
