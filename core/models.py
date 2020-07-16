from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator
from django.core.validators import MinLengthValidator

class Product(models.Model):
    sku_id = models.CharField(max_length=13, unique=True)
    description = models.CharField(max_length=200, blank=False)
    price = models.DecimalField(decimal_places=2, max_digits=10,
        validators=[MinValueValidator(Decimal('0.01'))])
