import os
import django
import sys

# Setup Django environment
sys.path.append(os.path.join(os.path.dirname(__file__), 'ecommerce'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from products.models import Product

def run_seed():
    print("Seeding products...")
    Product.objects.all().delete()
    
    products = [
        {
            "name": "Wireless Noise-Cancelling Headphones",
            "category": "Electronics",
            "description": "Experience pure sound with our premium noise-cancelling headphones. Features 30 hours of battery life and active noise cancellation.",
            "price": 299.99,
            "stock": 50,
        },
        {
            "name": "Minimalist Leather Watch",
            "category": "Clothing",
            "description": "A sleek, minimalist watch featuring genuine leather straps and a durable stainless steel case. Perfect for any occasion.",
            "price": 149.00,
            "stock": 100,
        },
        {
            "name": "The Art of Programming Book",
            "category": "Books",
            "description": "Master the fundamentals of computer science and software engineering with this comprehensive guide.",
            "price": 45.50,
            "stock": 200,
        },
        {
            "name": "Ultra-Slim 4K Monitor",
            "category": "Electronics",
            "description": "Enhance your workspace with this vibrant 27-inch 4K UHD monitor. Features ultra-slim bezels and true-to-life colors.",
            "price": 399.99,
            "stock": 30,
        },
        {
            "name": "Cotton Classic T-Shirt",
            "category": "Clothing",
            "description": "Premium 100% organic cotton t-shirt. Breathable, comfortable, and perfect for everyday wear.",
            "price": 25.00,
            "stock": 500,
        },
    ]

    for data in products:
        Product.objects.create(**data)
        print(f"Created {data['name']}")
        
    print("Seed complete!")

if __name__ == '__main__':
    run_seed()
