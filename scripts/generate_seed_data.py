# python
#!/usr/bin/env python3
import argparse
import csv
import gzip
import os
import random
import sys
import uuid
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Iterable, Tuple


def fmt_price(value_cents: int) -> str:
    d = (Decimal(value_cents) / Decimal(100)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return f"{d:.2f}"


def open_writer(path: Path, gz: bool):
    if gz:
        f = gzip.open(path.with_suffix(path.suffix + ".gz"), mode="wt", encoding="utf-8", newline="")
    else:
        f = path.open("w", encoding="utf-8", newline="")
    return f


def generate_restaurants(
        count: int,
        seed: int,
        start_id: int = 1,
) -> Iterable[dict]:
    random.seed(seed)

    adjectives = [
        "Sunset", "Golden", "Urban", "Coastal", "Silver", "Emerald", "Blue", "Crimson",
        "Rustic", "Grand", "Maple", "Cedar", "Highland", "Lakeside",
    ]
    nouns = [
        "Grill", "Kitchen", "Bistro", "Table", "Garden", "Diner", "House", "Terrace",
        "Canteen", "Corner", "Fork", "Spoon", "Skillet", "Oven",
    ]
    cuisines = [
        "Italian", "Mexican", "Indian", "Chinese", "Japanese", "Thai", "Greek",
        "American", "French", "Turkish", "Korean", "Spanish", "Vietnamese",
    ]
    cities = [
        ("New York", "USA"),
        ("Los Angeles", "USA"),
        ("Chicago", "USA"),
        ("Houston", "USA"),
        ("Toronto", "Canada"),
        ("Vancouver", "Canada"),
        ("London", "UK"),
        ("Manchester", "UK"),
        ("Berlin", "Germany"),
        ("Paris", "France"),
        ("Madrid", "Spain"),
        ("Mumbai", "India"),
        ("Bengaluru", "India"),
        ("Tokyo", "Japan"),
        ("Seoul", "South Korea"),
        ("Bangkok", "Thailand"),
        ("Istanbul", "Türkiye"),
        ("Sydney", "Australia"),
    ]

    created_at = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc).isoformat()

    for i in range(count):
        rid = start_id + i
        adj = random.choice(adjectives)
        noun = random.choice(nouns)
        cuisine = random.choice(cuisines)
        city, country = random.choice(cities)

        name = f"{adj} {noun} #{rid}"
        address = f"{100 + (rid % 900)} {adj} St"
        phone = f"+1-202-000-{rid:04d}"
        email = f"contact{rid}@example.org"  # placeholder, not real

        yield {
            "id": rid,
            "name": name,
            "description": "Casual dining with diverse menu",
            "address": address,
            "phone_number": phone,
            "email": email,
            "cuisine": cuisine,
            "city": city,
            "country": country,
            "is_active": "True" if random.random() > 0.03 else "False",
            "created_at": created_at,
        }


def generate_menu_items_for_restaurant(
        restaurant_id: int,
        count: int,
        next_item_id: int,
        rnd: random.Random,
) -> Tuple[int, Iterable[dict]]:
    adjectives = [
        "Spicy", "Smoky", "Crispy", "Creamy", "Tangy", "Savory", "Herbed",
        "Zesty", "Grilled", "Roasted", "Glazed", "Classic", "Deluxe", "Hearty",
    ]
    bases = [
        "Pizza", "Burger", "Wrap", "Bowl", "Salad", "Soup", "Sandwich",
        "Pasta", "Curry", "Tacos", "Dumplings", "Noodles", "Kebab", "Rice",
    ]
    proteins = [
        "Chicken", "Beef", "Pork", "Tofu", "Paneer", "Mushroom", "Lamb",
        "Fish", "Shrimp", "Veggie",
    ]
    cuisines = [
        "Italian", "Mexican", "Indian", "Chinese", "Japanese", "Thai", "Greek",
        "American", "French", "Turkish", "Korean", "Spanish", "Vietnamese",
    ]
    categories = ["Starters", "Mains", "Desserts", "Beverages", "Sides"]

    created_at = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc).isoformat()

    items = []
    for _ in range(count):
        adj = rnd.choice(adjectives)
        cui = rnd.choice(cuisines)
        pro = rnd.choice(proteins)
        base = rnd.choice(bases)
        name = f"{adj} {cui} {pro} {base}"
        if rnd.random() < 0.12:
            name = f"{name} #{rnd.randint(1, 9999)}"

        desc = f"{adj} {base} with {pro} in {cui} style."
        price_cents = rnd.randint(250, 2999)  # 2.50 to 29.99
        cat = rnd.choice(categories)

        items.append({
            "id": next_item_id,
            "restaurant_id": restaurant_id,
            "name": name,
            "description": desc,
            "category": cat,
            "price": fmt_price(price_cents),
            "is_available": "True" if rnd.random() > 0.05 else "False",
            "created_at": created_at,
        })
        next_item_id += 1

    return next_item_id, items


def generate_menu_items_stream(
        total_items: int,
        restaurants_count: int,
        min_per_rest: int,
        max_per_rest: int,
        seed: int,
        start_item_id: int = 1,
) -> Iterable[dict]:
    rnd = random.Random(seed)
    remaining = total_items

    for r_index in range(restaurants_count):
        if remaining <= 0:
            break
        rid = r_index + 1
        per = rnd.randint(min_per_rest, max_per_rest)
        per = min(per, remaining)
        start_item_id, items = generate_menu_items_for_restaurant(rid, per, start_item_id, rnd)
        for it in items:
            yield it
        remaining -= per


def write_to_csv(args, restaurants_path: Path, menu_items_path: Path):
    # Restaurants CSV
    with open_writer(restaurants_path, gz=args.gzip) as f_rest:
        writer = csv.DictWriter(
            f_rest,
            fieldnames=[
                "id", "name", "description", "address", "phone_number", "email",
                "cuisine", "city", "country", "is_active", "created_at",
            ],
        )
        writer.writeheader()
        for row in generate_restaurants(args.restaurants, seed=args.seed, start_id=1):
            writer.writerow(row)

    # Menu Items CSV
    with open_writer(menu_items_path, gz=args.gzip) as f_items:
        writer = csv.DictWriter(
            f_items,
            fieldnames=[
                "id", "restaurant_id", "name", "description", "category",
                "price", "is_available", "created_at",
            ],
        )
        writer.writeheader()

        total = 0
        for row in generate_menu_items_stream(
                total_items=args.items_total,
                restaurants_count=args.restaurants,
                min_per_rest=args.items_per_restaurant_min,
                max_per_rest=args.items_per_restaurant_max,
                seed=args.seed,
                start_item_id=1,
        ):
            writer.writerow(row)
            total += 1
            if args.print_progress_every and total % args.print_progress_every == 0:
                print(f"Wrote {total} menu items...")

    print("Done.")
    print(f"Restaurants CSV: {restaurants_path}{'.gz' if args.gzip else ''}")
    print(f"Menu items CSV:  {menu_items_path}{'.gz' if args.gzip else ''}")


def write_to_db(args):
    # Ensure the project root (server/) is on sys.path to import Django settings and your apps
    base_dir = Path(__file__).resolve().parents[1]  # points to server/
    sys.path.insert(0, str(base_dir))

    # Set up Django
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "coresite.settings")
    import django
    django.setup()

    from django.db import transaction
    from django.db.models import Value
    from django.db.models.functions import Concat

    # TODO: Replace this import with your actual app's models
    # For example: from apps.restaurants.models import Restaurant, MenuItem
    from apps.restaurants.models import Menu, Restaurant, MenuItem, MenuItemIngredient


    # A unique tag to re-select this batch reliably
    seed_tag = uuid.uuid4().hex
    tagged_marker = f"[seed:{seed_tag}]"

    print("Inserting restaurants...")
    restaurants_buffer = []
    created_at_dt = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    for row in generate_restaurants(args.restaurants, seed=args.seed, start_id=1):
        # Tag the description so we can re-query just this batch
        desc = f"{row['description']} {tagged_marker}"
        restaurants_buffer.append(Restaurant(
            name=row["name"],
            description=desc,
            address=row["address"],
            phone_number=row["phone_number"],
            email=row["email"],
            cuisine=row["cuisine"],
            city=row["city"],
            country=row["country"],
            is_active=(row["is_active"] == "True"),
            created_at=created_at_dt,
        ))

    batch_size = int(os.environ.get("SEED_RESTAURANTS_BATCH", "5000"))
    with transaction.atomic():
        Restaurant.objects.bulk_create(restaurants_buffer, batch_size=batch_size)

    # Re-select just-created restaurants in a deterministic order and get their IDs
    new_rest_ids = list(
        Restaurant.objects
        .filter(description__contains=tagged_marker)
        .order_by("id")
        .values_list("id", flat=True)
    )
    if len(new_rest_ids) != args.restaurants:
        raise SystemExit(f"Expected {args.restaurants} restaurants inserted, found {len(new_rest_ids)}.")

    print(f"Inserted {len(new_rest_ids)} restaurants.")

    # Now insert menu items mapped to those restaurant IDs
    print("Inserting menu items...")
    items_buffer = []
    items_batch_size = int(os.environ.get("SEED_MENUITEMS_BATCH", "20000"))
    total_items_written = 0

    # We want each restaurant to get between min and max items,
    # so set items_total to restaurants * max to let the generator distribute
    items_total = args.restaurants * args.items_per_restaurant_max

    for item in generate_menu_items_stream(
            total_items=items_total,
            restaurants_count=args.restaurants,
            min_per_rest=args.items_per_restaurant_min,
            max_per_rest=args.items_per_restaurant_max,
            seed=args.seed,
            start_item_id=1,
    ):
        # Map logical restaurant_id (1..N) to actual DB pk
        logical_rid = item["restaurant_id"]
        actual_rid = new_rest_ids[logical_rid - 1]

        menu = Menu.objects.filter(restaurant_id=actual_rid).first()
        if menu is None:
            menu = Menu.objects.create(restaurant_id=actual_rid, name="Default Menu")

        items_buffer.append(MenuItem(
            menu_id=menu.id,
            name=item["name"],
            description=item["description"],
            category=item["category"],
            price=Decimal(item["price"]),
            is_available=(item["is_available"] == "True"),
            created_at=created_at_dt,
        ))

        if len(items_buffer) >= items_batch_size:
            with transaction.atomic():
                MenuItem.objects.bulk_create(items_buffer, batch_size=items_batch_size)
            total_items_written += len(items_buffer)
            items_buffer.clear()
            if args.print_progress_every and total_items_written % args.print_progress_every == 0:
                print(f"Wrote {total_items_written} menu items...")

    # Flush remaining items
    if items_buffer:
        with transaction.atomic():
            MenuItem.objects.bulk_create(items_buffer, batch_size=items_batch_size)
        total_items_written += len(items_buffer)

    print(f"Done. Wrote {total_items_written} menu items to DB.")


def main():
    parser = argparse.ArgumentParser(description="Generate synthetic restaurants and menu items.")
    parser.add_argument("--out-dir", default="server/data", help="Output directory for CSV files.")
    parser.add_argument("--restaurants", type=int, default=10_000, help="Number of restaurants to generate.")
    parser.add_argument("--items-total", type=int, default=1_000_000,
                        help="Approx total menu items to generate (used for CSV mode).")
    parser.add_argument("--items-per-restaurant-min", type=int, default=50,
                        help="Min menu items per restaurant.")
    parser.add_argument("--items-per-restaurant-max", type=int, default=250,
                        help="Max menu items per restaurant.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility.")
    parser.add_argument("--gzip", action="store_true", help="Also write .gz compressed files.")
    parser.add_argument("--print-progress-every", type=int, default=200_000,
                        help="Print progress after this many menu items.")
    parser.add_argument("--to-db", action="store_true",
                        help="Write directly into the Django database instead of CSV.")
    args = parser.parse_args()

    if args.items_per_restaurant_min < 0 or args.items_per_restaurant_max < 0:
        raise SystemExit("Per-restaurant counts must be non-negative.")
    if args.items_per_restaurant_min > args.items_per_restaurant_max:
        raise SystemExit("Min per-restaurant cannot exceed max.")

    if True:  # Direct DB mode
        write_to_db(args)
        return

    # CSV mode (original behavior)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    restaurants_path = out_dir / "restaurants.csv"
    menu_items_path = out_dir / "menu_items.csv"
    write_to_csv(args, restaurants_path, menu_items_path)


if __name__ == "__main__":
    main()