from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class Alumno(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    grado = models.CharField(max_length=100)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)

    def __str__(self):
        return self.nombre

@receiver(post_save, sender=Alumno)
def generate_qr_code(sender, instance, created, **kwargs):
    if created:  # Solo generar el QR si el objeto es nuevo
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr_data = f"{instance.id}-{instance.nombre}"  # Utilizar el id que se asigna después de guardar
        qr.add_data(qr_data)
        qr.make(fit=True)

        # Crear la imagen QR
        img = qr.make_image(fill='black', back_color='white')

        # Guardar imagen en el campo 'qr_code'
        buffer = BytesIO()
        img.save(buffer)
        file_name = f"{instance.nombre}_qr.png"
        instance.qr_code.save(file_name, File(buffer), save=False)

        # Guardar de nuevo el objeto para que se almacene la imagen del QR
        instance.save()  # Esta llamada a save() no llamará a generate_qr_code nuevamente, por la condición `if created`


class RegistroIngreso(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    hora_ingreso = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.alumno.nombre} - {self.hora_ingreso}'