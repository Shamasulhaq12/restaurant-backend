import os
import sys
import random
from datetime import datetime, timezone
from pathlib import Path

# Setup Django
base_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(base_dir))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "coresite.settings")
import django
django.setup()

from django.db import transaction
from apps.restaurants.models import MenuItem, MenuItemIngredient


def seed_ingredients(limit=None, offset=0):
    created_at = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

    ingredient_names = [
        "Tomato", "Onion", "Cheese", "Garlic", "Olive Oil", "Basil",
        "Chicken", "Beef", "Mushroom", "Pepper", "Salt", "Butter",
        "Spinach", "Coriander", "Mint", "Lemon", "Chili", "Rice", "Pasta"
    ]

    total_items = MenuItem.objects.count()
    print(f"📦 Total Menu Items in DB: {total_items}")

    # get subset with offset + limit
    qs = MenuItem.objects.all().order_by("id")
    if limit:
        qs = qs[offset:offset + limit]

    print(f"➡️ Processing {qs.count()} menu items (offset={offset}, limit={limit})")

    for item in qs:
        if item.ingredients.exists():  # already has ingredients
            print(f"⏭ Skipping {item.name}, already has ingredients")
            continue

        num_ing = random.randint(3, 6)  # how many ingredients per item
        ing_buffer = []
        for _ in range(num_ing):
            ing = MenuItemIngredient(
                menu_item=item,
                name=random.choice(ingredient_names),
                quantity=f"{random.randint(1, 500)}g",
                description=f"Fresh {item.name} ingredient",
                created_at=created_at,
                updated_at=created_at,
            )
            ing_buffer.append(ing)

        with transaction.atomic():
            MenuItemIngredient.objects.bulk_create(ing_buffer, batch_size=500)

        print(f"✅ Added {num_ing} ingredients to {item.name}")


if __name__ == "__main__":
    # Example: seed_ingredients(limit=50, offset=0)
    # Next run: seed_ingredients(limit=50, offset=50), etc.
    seed_ingredients(limit=50, offset=0)
