from rest_framework import serializers

from .models import CreditCard

class CreditCardRequest(serializers.Serializer):
    number = serializers.CharField()
    expiry_date = serializers.CharField()
    cvv = serializers.CharField()


class CreditCardSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    encrypted_number = serializers.CharField()
    encrypted_expiry_date = serializers.CharField()
    encrypted_cvv = serializers.CharField()

    def create(self, validated_data):
        return CreditCard.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.encrypted_number = validated_data.get('encrypted_number', instance.encrypted_number)
        instance.encrypted_expiry_date = validated_data.get('encrypted_expiry_date', instance.encrypted_expiry_date)
        instance.encrypted_cvv = validated_data.get('encrypted_cvv', instance.encrypted_cvv)
        instance.save()
        return instance