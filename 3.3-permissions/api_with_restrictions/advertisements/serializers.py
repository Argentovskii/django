from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement
from advertisements.models import Advertisement, AdvertisementStatusChoices

class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        request = self.context['request']
        user = request.user

        status = data.get(
            'status',
            getattr(self.instance, 'status', AdvertisementStatusChoices.OPEN)
        )

        if status == AdvertisementStatusChoices.OPEN:

            qs = Advertisement.objects.filter(
                creator=user,
                status=AdvertisementStatusChoices.OPEN
            )

            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.count() >= 10:
                raise serializers.ValidationError(
                    'Нельзя иметь более 10 открытых объявлений.'
                )

        return data
