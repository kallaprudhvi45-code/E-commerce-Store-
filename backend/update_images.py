import os
import django
from django.core.files import File
import sys

# Setup Django environment
sys.path.append(os.path.join(os.path.dirname(__file__), 'ecommerce'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from products.models import Product

images = {
    "Wireless Noise-Cancelling Headphones": r"C:\Users\kalla\.gemini\antigravity-ide\brain\57c2d81c-93e1-43a8-8637-24da4aa849e6\headphones_1781008046294.png",
    "Minimalist Leather Watch": r"C:\Users\kalla\.gemini\antigravity-ide\brain\57c2d81c-93e1-43a8-8637-24da4aa849e6\watch_1781008146086.png",
    "The Art of Programming Book": r"C:\Users\kalla\.gemini\antigravity-ide\brain\57c2d81c-93e1-43a8-8637-24da4aa849e6\book_1781008213126.png",
    "Ultra-Slim 4K Monitor": r"C:\Users\kalla\.gemini\antigravity-ide\brain\57c2d81c-93e1-43a8-8637-24da4aa849e6\monitor_1781008340674.png",
    "Cotton Classic T-Shirt": r"C:\Users\kalla\.gemini\antigravity-ide\brain\57c2d81c-93e1-43a8-8637-24da4aa849e6\tshirt_1781008362589.png",
}

for product_name, img_path in images.items():
    try:
        product = Product.objects.get(name=product_name)
        with open(img_path, 'rb') as f:
            product.image.save(os.path.basename(img_path), File(f), save=True)
        print(f"Updated image for {product_name}")
    except Exception as e:
        print(f"Error updating {product_name}: {e}")
