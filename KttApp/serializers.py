from rest_framework import serializers

from .models import *

class CascProductCodesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CascProductCodes
        fields = "__all__"


class HsCodesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HsCode
        fields = "__all__"