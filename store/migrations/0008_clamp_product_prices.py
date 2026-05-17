from decimal import Decimal

from django.db import migrations


def clamp_product_prices(apps, schema_editor):
    Product = apps.get_model('store', 'Product')

    lower_bound = Decimal('1000.00')
    upper_bound = Decimal('1500.00')

    for product in Product.objects.all().only('id', 'price'):
        if product.price < lower_bound:
            product.price = lower_bound
        elif product.price > upper_bound:
            product.price = upper_bound
        else:
            continue

        product.save(update_fields=['price'])


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_seed_catalog_data'),
    ]

    operations = [
        migrations.RunPython(clamp_product_prices, migrations.RunPython.noop),
    ]