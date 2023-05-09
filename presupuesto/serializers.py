from rest_framework import serializers
from .models import Categoria, Transaccion
from datetime import datetime

import logging

logger = logging.getLogger(__name__)


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'
    
    def categoria_exists(self, category_id):
        if Categoria.objects.filter(id=category_id).exists():
            raise serializers.ValidationError(
                f"Ya existe una categoría con el id {category_id}")
        else:
            return True
        
class TransaccionSerializer(serializers.ModelSerializer):
    date = serializers.CharField(required=False)
    category = serializers.PrimaryKeyRelatedField(queryset=Categoria.objects.all())

    class Meta:
        model = Transaccion
        fields = '__all__'

    def create(self, validated_data):
        if 'date' not in validated_data:
            validated_data['date'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        category_id = validated_data.pop('category')
        try:
            validated_data['category'] = Categoria.objects.get(id=category_id)
        except Categoria.DoesNotExist:
            raise serializers.ValidationError(
                f"No existe una categoría con el id {category_id}")
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        category_id = validated_data.pop('category')
        try:
            validated_data['category'] = Categoria.objects.get(id=category_id)
        except Categoria.DoesNotExist:
            raise serializers.ValidationError(
                f"No existe una categoría con el id {category_id}")
        return super().update(instance, validated_data)
    
        
    def transaccion_exists(self, transaccion_id):
        if Transaccion.objects.filter(id=transaccion_id).exists():
            raise serializers.ValidationError(
                f"Ya existe una transacción con el id {transaccion_id}")
        else:
            return True