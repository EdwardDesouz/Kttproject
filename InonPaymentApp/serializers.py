from rest_framework import serializers
from .models import InNonImporter

class InNonSeralizer(serializers.ModelSerializer):
    class Meta:
        model = InNonImporter
        fields = ["Code","Name","Name1","CRUEI","Status"]