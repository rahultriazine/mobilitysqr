from rest_framework import serializers
from mobility_apps.master.models import Currency , Currency_Conversion,Currency_Conversion_History,Per_Diem

class CurrencySerializers(serializers.ModelSerializer):
    class Meta:
        model =  Currency
        # fields = ('firstname','lastname')
        fields = '__all__'

class Currency_ConversionSerializers(serializers.ModelSerializer):
    class Meta:
        model =  Currency_Conversion
        # fields = ('firstname','lastname')
        fields = '__all__'

class Currency_Conversion_HistorySerializers(serializers.ModelSerializer):
    class Meta:
        model =  Currency_Conversion_History
        # fields = ('firstname','lastname')
        fields = '__all__'


class Per_DiemSerializers(serializers.ModelSerializer):
    class Meta:
        model =  Per_Diem
        # fields = ('firstname','lastname')
        fields = '__all__'