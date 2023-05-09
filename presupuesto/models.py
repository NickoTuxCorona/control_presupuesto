from django.db import models

# Create your models here.
class Categoria(models.Model):
    name = models.CharField(max_length=255)
    limit = models.IntegerField()
    
    def __str__(self):
        return self.name

class Transaccion(models.Model):
    description = models.CharField(max_length=255)
    category = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()
    ignore = models.BooleanField(default=False)
    
    def __str__(self):
        return self.description