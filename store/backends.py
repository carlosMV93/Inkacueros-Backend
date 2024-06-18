# Importa la clase base para el backend de correo electrónico SMTP de Django
from django.core.mail.backends.smtp import EmailBackend


# Define una clase que herede del backend de correo electrónico SMTP de Django
class SSLOffBackend(EmailBackend):
    def open(self):
        # Llama al método 'open' de la clase base para iniciar la conexión SMTP
        self.connection = super().open()

        # Realiza ajustes adicionales si es necesario, por ejemplo, iniciar TLS
        # Esto es opcional y depende de tus requisitos y configuración específica
        self.connection.starttls()

        # Devuelve la conexión actualizada
        return self.connection
