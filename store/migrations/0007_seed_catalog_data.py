from django.db import migrations


def seed_catalog(apps, schema_editor):
    Category = apps.get_model('store', 'Category')
    Product = apps.get_model('store', 'Product')

    category_rows = [
        {
            'title': 'Rings',
            'slug': 'rings',
            'description': 'Gold, silver, and diamond rings for everyday wear and special occasions.',
            'category_image': 'category/rings.jpg',
            'is_active': True,
            'is_featured': True,
        },
        {
            'title': 'Necklaces',
            'slug': 'necklaces',
            'description': 'Elegant necklaces, chains, and pendants with classic jewellery styling.',
            'category_image': 'category/necklaces.jpg',
            'is_active': True,
            'is_featured': True,
        },
        {
            'title': 'Earrings',
            'slug': 'earrings',
            'description': 'Studs and drop earrings in gold and silver finishes.',
            'category_image': 'category/ear-rings.jpg',
            'is_active': True,
            'is_featured': True,
        },
        {
            'title': 'Bracelets',
            'slug': 'bracelets',
            'description': 'Bracelets and bangles with polished gold styling.',
            'category_image': 'category/bracelets.jpg',
            'is_active': True,
            'is_featured': True,
        },
        {
            'title': 'Watches',
            'slug': 'watches',
            'description': 'Fashion watches and statement timepieces for men and women.',
            'category_image': 'category/watches.jpg',
            'is_active': True,
            'is_featured': True,
        },
        {
            'title': 'Gifts',
            'slug': 'gifts',
            'description': 'Gift-ready jewellery picks and special occasion items.',
            'category_image': 'category/gifts.jpg',
            'is_active': True,
            'is_featured': False,
        },
        {
            'title': 'Beaded Necklaces',
            'slug': 'beaded-necklaces',
            'description': 'Beaded necklace styles and handcrafted jewellery pieces.',
            'category_image': 'category/bead-necklace.jpg',
            'is_active': True,
            'is_featured': False,
        },
    ]

    categories = {}
    for row in category_rows:
        category, _ = Category.objects.update_or_create(
            slug=row['slug'],
            defaults=row,
        )
        categories[row['slug']] = category

    product_rows = [
        {
            'sku': 'JH-RNG-001',
            'title': 'Gold and Diamond Ring',
            'slug': 'gold-and-diamond-ring',
            'short_description': 'Classic gold ring with a diamond accent.',
            'detail_description': 'A timeless ring designed for daily elegance and gifting.',
            'product_image': 'product/gold-and-diamond-ring.jpg',
            'price': '12999.00',
            'category_slug': 'rings',
            'is_active': True,
            'is_featured': True,
        },
        {
            'sku': 'JH-RNG-002',
            'title': 'Gold Ring with Blue Stones',
            'slug': 'gold-ring-with-blue-stones',
            'short_description': 'Gold ring with bright blue stone accents.',
            'detail_description': 'A statement ring with a polished gold finish and blue stones.',
            'product_image': 'product/Gold-Ring-with-Blue-Stones.jpg',
            'price': '8999.00',
            'category_slug': 'rings',
            'is_active': True,
            'is_featured': True,
        },
        {
            'sku': 'JH-RNG-003',
            'title': 'Gold Ring with Pink Stone and Diamonds',
            'slug': 'gold-ring-with-pink-stone-and-diamonds',
            'short_description': 'Gold ring with pink stone and diamond detailing.',
            'detail_description': 'A premium ring designed for festive and occasion wear.',
            'product_image': 'product/Gold-ring-with-pink-stone-and-diamonds.jpg',
            'price': '10999.00',
            'category_slug': 'rings',
            'is_active': True,
            'is_featured': True,
        },
        {
            'sku': 'JH-RNG-004',
            'title': 'Gold Ring with White Stone',
            'slug': 'gold-ring-with-white-stone',
            'short_description': 'Minimal gold ring with a white stone finish.',
            'detail_description': 'Simple and elegant ring style for everyday wear.',
            'product_image': 'product/Gold-Ring-with-White-Stone.jpg',
            'price': '7499.00',
            'category_slug': 'rings',
            'is_active': True,
            'is_featured': False,
        },
        {
            'sku': 'JH-RNG-005',
            'title': 'Platinum Ring with Diamonds',
            'slug': 'platinum-ring-with-diamonds',
            'short_description': 'Platinum ring with a diamond-studded pattern.',
            'detail_description': 'A premium ring with a luxury finish and elegant sparkle.',
            'product_image': 'product/platinum-ring-with-diamonds.jpg',
            'price': '15999.00',
            'category_slug': 'rings',
            'is_active': True,
            'is_featured': True,
        },
        {
            'sku': 'JH-NCK-001',
            'title': 'Gold Necklace with Diamonds',
            'slug': 'gold-necklace-with-diamonds',
            'short_description': 'Gold necklace accented with diamond details.',
            'detail_description': 'An elegant necklace suited for formal wear and gifting.',
            'product_image': 'product/Gold-Necklace-with-Diamonds.jpg',
            'price': '21999.00',
            'category_slug': 'necklaces',
            'is_active': True,
            'is_featured': True,
        },
        {
            'sku': 'JH-NCK-002',
            'title': 'Silver Necklace with Big Diamond',
            'slug': 'silver-necklace-with-big-diamond',
            'short_description': 'Silver necklace with a large diamond centerpiece.',
            'detail_description': 'A standout necklace for special events and premium gifting.',
            'product_image': 'product/Silver-Necklace-with-Big-Diamond.jpg',
            'price': '17999.00',
            'category_slug': 'necklaces',
            'is_active': True,
            'is_featured': False,
        },
        {
            'sku': 'JH-NCK-003',
            'title': 'Beads Necklace',
            'slug': 'beads-necklace',
            'short_description': 'Beaded necklace with a traditional look.',
            'detail_description': 'A versatile beaded necklace for ethnic and casual outfits.',
            'product_image': 'product/Beads-Necklace.jpg',
            'price': '6999.00',
            'category_slug': 'beaded-necklaces',
            'is_active': True,
            'is_featured': False,
        },
        {
            'sku': 'JH-NCK-004',
            'title': 'Mangalsutra with Gold Locket',
            'slug': 'mangalsutra-with-gold-locket',
            'short_description': 'Traditional mangalsutra with a gold locket.',
            'detail_description': 'Designed with a refined traditional finish for everyday use.',
            'product_image': 'product/Mangalsutra-with-Gold-Locket.jpg',
            'price': '8999.00',
            'category_slug': 'gifts',
            'is_active': True,
            'is_featured': False,
        },
        {
            'sku': 'JH-EAR-001',
            'title': 'Gold Leafy Earrings',
            'slug': 'gold-leafy-earrings',
            'short_description': 'Leaf-inspired earrings with a gold finish.',
            'detail_description': 'Lightweight earrings with a stylish botanical silhouette.',
            'product_image': 'product/Gold-Leafy-Earrings.jpg',
            'price': '5499.00',
            'category_slug': 'earrings',
            'is_active': True,
            'is_featured': True,
        },
        {
            'sku': 'JH-EAR-002',
            'title': 'Gold Star Earrings',
            'slug': 'gold-star-earrings',
            'short_description': 'Star-shaped gold earrings.',
            'detail_description': 'A playful and elegant pair for everyday wear.',
            'product_image': 'product/Gold-Star-Earrings.jpg',
            'price': '4599.00',
            'category_slug': 'earrings',
            'is_active': True,
            'is_featured': False,
        },
        {
            'sku': 'JH-EAR-003',
            'title': 'Silver Earrings with Blue Stone',
            'slug': 'silver-earrings-with-blue-stone',
            'short_description': 'Silver earrings with blue stone detail.',
            'detail_description': 'A refined pair for both casual and festive outfits.',
            'product_image': 'product/Silver-Earrings-with-Blue-Stone.jpg',
            'price': '3999.00',
            'category_slug': 'earrings',
            'is_active': True,
            'is_featured': False,
        },
        {
            'sku': 'JH-BRC-001',
            'title': 'Gold Bracelet',
            'slug': 'gold-bracelet',
            'short_description': 'Simple gold bracelet with a polished finish.',
            'detail_description': 'A classic bracelet for layering or standalone wear.',
            'product_image': 'product/Gold-Bracelet.jpg',
            'price': '8999.00',
            'category_slug': 'bracelets',
            'is_active': True,
            'is_featured': True,
        },
        {
            'sku': 'JH-BRC-002',
            'title': 'Gold Bracelets',
            'slug': 'gold-bracelets',
            'short_description': 'Pair of gold bracelets with a luxury look.',
            'detail_description': 'A bold bracelet set suitable for gifting and events.',
            'product_image': 'product/Gold-Bracelets.jpg',
            'price': '14999.00',
            'category_slug': 'bracelets',
            'is_active': True,
            'is_featured': False,
        },
        {
            'sku': 'JH-WAT-001',
            'title': 'Anne Klein Gold Watch',
            'slug': 'anne-klein-gold-watch',
            'short_description': 'Elegant gold watch with a refined dial.',
            'detail_description': 'A fashion-forward watch designed for everyday styling.',
            'product_image': 'product/Anne-Klein-Gold-Watch.jpg',
            'price': '11999.00',
            'category_slug': 'watches',
            'is_active': True,
            'is_featured': True,
        },
        {
            'sku': 'JH-WAT-002',
            'title': 'Gold Casio Touch Watch',
            'slug': 'gold-casio-touch-watch',
            'short_description': 'Gold touch watch inspired by sporty luxury.',
            'detail_description': 'A stylish watch with a modern gold-toned design.',
            'product_image': 'product/Gold-Casio-Touch-Watch.jpg',
            'price': '9999.00',
            'category_slug': 'watches',
            'is_active': True,
            'is_featured': True,
        },
        {
            'sku': 'JH-WAT-003',
            'title': 'Mr Boho Gold Watch',
            'slug': 'mr-boho-gold-watch',
            'short_description': 'Minimal gold watch with a contemporary look.',
            'detail_description': 'A sleek everyday watch with a lightweight profile.',
            'product_image': 'product/Mr-Boho-Gold-Watch.jpg',
            'price': '10999.00',
            'category_slug': 'watches',
            'is_active': True,
            'is_featured': False,
        },
        {
            'sku': 'JH-WAT-004',
            'title': 'Gold and Steel Rado Watch with Black Dial',
            'slug': 'gold-and-steel-rado-watch-with-black-dial',
            'short_description': 'Gold and steel watch with a black dial.',
            'detail_description': 'A premium two-tone timepiece with a striking contrast dial.',
            'product_image': 'product/Gold-and-Steel-Rado-Watch-with-Black-Dial.jpg',
            'price': '18999.00',
            'category_slug': 'watches',
            'is_active': True,
            'is_featured': False,
        },
        {
            'sku': 'JH-WAT-005',
            'title': 'Gold Watch with White Dial',
            'slug': 'gold-watch-with-white-dial',
            'short_description': 'Gold watch featuring a white dial.',
            'detail_description': 'Clean and versatile watch style for daily wear.',
            'product_image': 'product/Gold-Watch-with-White-Dial.jpg',
            'price': '8999.00',
            'category_slug': 'watches',
            'is_active': True,
            'is_featured': False,
        },
        {
            'sku': 'JH-WAT-006',
            'title': 'Gold Watch with White Dial and Diamonds',
            'slug': 'gold-watch-with-white-dial-and-diamonds',
            'short_description': 'Luxury gold watch with white dial and diamond accents.',
            'detail_description': 'A premium watch with an elegant dial and sparkling details.',
            'product_image': 'product/Gold-Watch-with-White-Dial-and-Diamonds.jpg',
            'price': '19999.00',
            'category_slug': 'watches',
            'is_active': True,
            'is_featured': True,
        },
        {
            'sku': 'JH-WAT-007',
            'title': 'Gold Bitcoin Watch',
            'slug': 'gold-bitcoin-watch',
            'short_description': 'Novelty gold watch with a bitcoin-inspired design.',
            'detail_description': 'A statement piece for unique jewellery and gift collections.',
            'product_image': 'product/gold-bitcoin.jpg',
            'price': '13999.00',
            'category_slug': 'watches',
            'is_active': True,
            'is_featured': False,
        },
    ]

    for row in product_rows:
        category = categories[row.pop('category_slug')]
        Product.objects.update_or_create(
            sku=row['sku'],
            defaults={**row, 'category': category},
        )


def unseed_catalog(apps, schema_editor):
    Category = apps.get_model('store', 'Category')
    Product = apps.get_model('store', 'Product')

    seeded_skus = [
        'JH-RNG-001', 'JH-RNG-002', 'JH-RNG-003', 'JH-RNG-004', 'JH-RNG-005',
        'JH-NCK-001', 'JH-NCK-002', 'JH-NCK-003', 'JH-NCK-004',
        'JH-EAR-001', 'JH-EAR-002', 'JH-EAR-003',
        'JH-BRC-001', 'JH-BRC-002',
        'JH-WAT-001', 'JH-WAT-002', 'JH-WAT-003', 'JH-WAT-004', 'JH-WAT-005', 'JH-WAT-006', 'JH-WAT-007',
    ]
    seeded_categories = ['rings', 'necklaces', 'earrings', 'bracelets', 'watches', 'gifts', 'beaded-necklaces']

    Product.objects.filter(sku__in=seeded_skus).delete()
    Category.objects.filter(slug__in=seeded_categories).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_alter_order_options_alter_payment_options_and_more'),
    ]

    operations = [
        migrations.RunPython(seed_catalog, unseed_catalog),
    ]
