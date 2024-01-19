from django.db import models
from cryptography.fernet import Fernet

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class CreditCard(BaseModel):
    encrypted_number = models.CharField(max_length=255)
    encrypted_expiry_date = models.CharField(max_length=255)
    encrypted_cvv = models.CharField(max_length=255)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    @property
    def number(self):
        return self.decrypt_field(self.encrypted_number)

    @property
    def expiry_date(self):
        return self.decrypt_field(self.encrypted_expiry_date)

    @property
    def cvv(self):
        return self.decrypt_field(self.encrypted_cvv)

    def encrypt_field(self, value):
        key = self.user.password[:32].encode('utf-8')
        cipher = Fernet(key)
        return cipher.encrypt(value.encode('utf-8'))

    def decrypt_field(self, value):
        key = self.user.password[:32].encode('utf-8')
        cipher = Fernet(key)
        decrypted_value = cipher.decrypt(value).decode('utf-8')
        return decrypted_value

    class Meta:
        db_table = "credit_card"

