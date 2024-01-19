from base64 import urlsafe_b64encode

from cryptography.fernet import Fernet
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .models import CreditCard
from .serializers import CreditCardSerializer, CreditCardRequest

class CreditCardListView(generics.ListCreateAPIView):
    queryset = CreditCard.objects.all()
    serializer_class = CreditCardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CreditCardDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CreditCard.objects.all()
    serializer_class = CreditCardSerializer
    permission_classes = [permissions.IsAuthenticated]

@api_view(['GET'])
def get_credit_card_details(request, card_id):
    try:
        credit_card = CreditCard.objects.get(pk=card_id)
    except CreditCard.DoesNotExist:
        return Response({'error': 'Cartão de crédito não encontrado'}, status=404)

    key = Fernet.generate_key()
    cipher = Fernet(b'sMZ2TCjKeEsh-D6PmpZ5TuTNHsmdvyt0zqKvbF5AYME=')

    decrypted_number = cipher.decrypt(credit_card.encrypted_number).decode('utf-8')
    decrypted_expiry_date = cipher.decrypt(credit_card.encrypted_expiry_date).decode('utf-8')
    decrypted_cvv = cipher.decrypt(credit_card.encrypted_cvv).decode('utf-8')

    response_data = {
        'id': credit_card.id,
        'number': decrypted_number,
        'expiry_date': decrypted_expiry_date,
        'cvv': decrypted_cvv,
    }

    return Response(response_data)

@swagger_auto_schema(method='POST', request_body=CreditCardRequest)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def encrypt_credit_card(request):
    key = Fernet.generate_key()
    cipher = Fernet(b'sMZ2TCjKeEsh-D6PmpZ5TuTNHsmdvyt0zqKvbF5AYME=')

    card_data = {
        "number": request.data.get("number"),
        "expiry_date": request.data.get("expiry_date"),
        "cvv": request.data.get("cvv"),
    }

    number_str = card_data["number"].encode("utf-8")
    expiry_date_str = card_data["expiry_date"].encode("utf-8")
    cvv_str = card_data["cvv"].encode("utf-8")

    encrypted_number = cipher.encrypt(number_str)
    encrypted_expiry_date = cipher.encrypt(expiry_date_str)
    encrypted_cvv = cipher.encrypt(cvv_str)
    
    response_data = {
        'encrypted_number': encrypted_number,
        'encrypted_expiry_date': encrypted_expiry_date,
        'encrypted_cvv': encrypted_cvv,
    }

    return Response(response_data)
