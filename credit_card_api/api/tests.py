from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from cryptography.fernet import Fernet
from django.contrib.auth.models import User

from .models import CreditCard

class CreditCardAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', password='testpassword')
        
        self.card_data = {
            'number': '5275477609353716',
            'expiry_date': '03/25',
            'cvv': '320',
        }
        
        self.card_data_encrypted = {
            'user': self.user,
            "encrypted_number": "gAAAAABlqm-PennceNnDj8lFP_-vRCFNivsgLtsxA6AgV08OIg9hz-lDse4YsrvzXfKCT0Rmm4xUBRMuXqpulwb6JAIXt4NDVxBT69eUnMspbUKZEoezLgU=",
            "encrypted_expiry_date": "gAAAAABlqm-Qi6xC8usc_9C0CKOwyBZ7P__6h3RszSXA4VRm1WMwIt_NpK86H-lzfMqeb7yUfwUzMSSz9yC0udZipDDe2BSBFw==",
            "encrypted_cvv": "gAAAAABlqm-Qp859wDdAjESMMrWmKP2_oui-tGFNRvJt1iqkz24B99DTuUqu_MMmGJ3nQQzh280vilUPSn7TXTIKyNAMKjzbtg=="
        }

    def test_encrypt_credit_card(self):
        url = reverse('encrypt-credit-card')
        response = self.client.post(url, data=self.card_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertIn('encrypted_number', response.data)
        self.assertIn('encrypted_expiry_date', response.data)
        self.assertIn('encrypted_cvv', response.data)

    def test_get_credit_card_details(self):
        credit_card = CreditCard.objects.create(**self.card_data_encrypted)

        cipher = Fernet(b'sMZ2TCjKeEsh-D6PmpZ5TuTNHsmdvyt0zqKvbF5AYME=')
        
        decrypted_number = cipher.decrypt(credit_card.encrypted_number).decode('utf-8')
        decrypted_expiry_date = cipher.decrypt(credit_card.encrypted_expiry_date).decode('utf-8')
        decrypted_cvv = cipher.decrypt(credit_card.encrypted_cvv).decode('utf-8')
        
        client = APIClient()
        client.force_authenticate(user=self.user)

        url = reverse('credit-card-detail', args=[credit_card.id])
        response = client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['id'], credit_card.id)
        self.assertEqual(response.data['number'], decrypted_number)
        self.assertEqual(response.data['expiry_date'], decrypted_expiry_date)
        self.assertEqual(response.data['cvv'], decrypted_cvv)
