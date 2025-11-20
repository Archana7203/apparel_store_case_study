import ast
import datetime
import os
import random
from database import db, engine
from models import (
    Category, OfferUsage, Sub_Category, Combination, Base, ColorCombination,
    CustomerPersonal, OrderItem, CustomerMeta, Address, CustomerPreference,
    Product, ProductVariant, Inventory, OrderHeader, Offer
)
import csv
import sys
from dateutil import parser
from enums import (
    GenderEnum, ActiveStatusEnum, AddressTypeEnum,
    EmploymentEnum, ProductGenderEnum, OccasionEnum,
    StyleEnum, SeasonEnum
)
combo_data = [
    (1, {5: "pant", 9: "shoes", 13: "watches"}),
    (1, {5: "pant", 9: "shoes", 15: "belt"}),
    (1, {5: "pant", 12: "boots", 15: "belt"}),
    (1, {5: "pant", 12: "boots", 13: "watches"}),
    (5, {1: "shirt", 9: "shoes", 13: "watches"}),
    (5, {1: "shirt", 9: "shoes", 15: "belt"}),
    (5, {1: "shirt", 12: "boots", 13: "watches"}),
    (5, {1: "shirt", 12: "boots", 15: "belt"}),
    (9, {16: "socks"}),
    (12, {16: "socks"}),
    (4, {8: "leggings", 14: "handbag", 11: "sandals"}),
    (3, {6: "jeans", 10: "sneakers", 14: "handbag"}),
    (3, {6: "jeans", 10: "sneakers", 13: "watches"}),
    (3, {7: "skirt", 11: "sandals", 14: "handbag"}),
    (7, {3: "crop top", 11: "sandals", 14: "handbag"}),
    (7, {3: "crop top", 10: "sneakers", 13: "watches"}),
    (7, {3: "crop top", 10: "sneakers", 14: "handbag"}),
    (2, {6: "jeans", 10: "sneakers", 13: "watches"}),
    (6, {2: "tshirt", 10: "sneakers", 13: "watches"}),
    (6, {3: "crop top", 10: "sneakers", 13: "watches"}),
    (6, {3: "crop top", 10: "sneakers", 15: "belt"}),
    (10, {14: "handbag"}),
    (11, {14: "handbag"}),
    (13, {15: "belt"}),
    (16, {9: "shoes"}),
    (15, {13: "watches"}),
    (14, {13: "watches"}),
]

def insert_categories():
    try:
        main_categories = [
            Category(category_id=1, category_name="Top wear"),
            Category(category_id=2, category_name="Bottom wear"),
            Category(category_id=3, category_name="Footwear"),
            Category(category_id=4, category_name="Accessories"),
        ]
        db.add_all(main_categories)
        db.flush()

        subcategories = [
            Sub_Category(subcategory_id=1, subcategory_name="Shirt", category_id=1),
            Sub_Category(subcategory_id=2, subcategory_name="T-shirt", category_id=1),
            Sub_Category(subcategory_id=3, subcategory_name="Crop-top", category_id=1),
            Sub_Category(subcategory_id=4, subcategory_name="Kurti", category_id=1),
            Sub_Category(subcategory_id=5, subcategory_name="Pants", category_id=2),
            Sub_Category(subcategory_id=6, subcategory_name="Jeans", category_id=2),
            Sub_Category(subcategory_id=7, subcategory_name="Skirts", category_id=2),
            Sub_Category(subcategory_id=8, subcategory_name="Leggings", category_id=2),
            Sub_Category(subcategory_id=9, subcategory_name="Shoes", category_id=3),
            Sub_Category(subcategory_id=10, subcategory_name="Sneakers", category_id=3),
            Sub_Category(subcategory_id=11, subcategory_name="Sandals", category_id=3),
            Sub_Category(subcategory_id=12, subcategory_name="Boots", category_id=3),
            Sub_Category(subcategory_id=13, subcategory_name="Watches", category_id=4),
            Sub_Category(subcategory_id=14, subcategory_name="Handbag", category_id=4),
            Sub_Category(subcategory_id=15, subcategory_name="Belt", category_id=4),
            Sub_Category(subcategory_id=16, subcategory_name="Socks", category_id=4),
        ]
        db.add_all(subcategories)
        db.commit()
        print("Categories and subcategories inserted.")
    except Exception as e:
        db.rollback()
        print("Error inserting categories:", e)

def random_date():
    start = datetime.datetime(2024, 1, 1, 12, 0, 0)
    end = datetime.datetime(2025, 6, 12, 12, 0, 0)
    delta = end - start
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return start + datetime.timedelta(seconds=random_seconds)

def insert_combos():
    try:
        for subcat_id, combo_list in combo_data:
            combo = Combination(
                subcategory_id=subcat_id,
                combo_list=combo_list,
                created_at=random_date(),
                updated_at=random_date()
            )
            db.add(combo)
        db.commit()
        print("27 combos inserted.")
    except Exception as e:
        db.rollback()
        print("Error inserting combos:", e)

def insert_color_combinations():
    try:
        with open("data/color_combination.csv", newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            color_entries = []

            for row in reader:
                color_entry = ColorCombination(
                    base_color=row["Base_Color"].strip(),
                    matching_color=row["Matching_Color"].strip(),
                    score=int(row["Score"])
                )
                color_entries.append(color_entry)

            db.add_all(color_entries)
            db.commit()
            print("Color combinations inserted from CSV successfully!")

    except Exception as e:
        db.rollback()
        print("Error inserting color combinations:", e)

def insert_customers_from_csv():
    try:
        with open('data/customer_personal.csv', newline='', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                print("Inserting customer:", row)
                row = {k.strip(): v.strip() if isinstance(v, str) else v for k, v in row.items()}
                
                dob = datetime.datetime.strptime(row['date_of_birth'], '%Y-%m-%d').date()
                created_at = datetime.datetime.strptime(row['created_at'], '%Y-%m-%d').date()
                last_login = datetime.datetime.strptime(row['last_login'], '%Y-%m-%d %H:%M:%S')

                customer = CustomerPersonal(
                    customer_id=int(row['customer_id']),
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    email_id=row['email_id'],
                    phone_number=row['phone_number'],  # already fine now
                    date_of_birth=dob,
                    gender=GenderEnum(row['gender']).value,
                    profile_pic=row['profile_pic'],
                    created_at=created_at,
                    last_login=last_login,
                    active_status=ActiveStatusEnum(row['active_status']).value
                )
                db.add(customer)

            db.commit()
            print("Customer data inserted successfully.")
            sys.stdout.flush()
    except Exception as e:
        db.rollback()
        print("Error inserting customer data:", e)

def insert_customer_meta_from_csv():
    try:
        with open('data/customer_meta.csv', newline='', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            entries = []
            for row in reader:
                row = {k.strip(): v.strip() if isinstance(v, str) else v for k, v in row.items()}
                created_at = datetime.datetime.strptime(row['created_at'], '%Y-%m-%d %H:%M:%S')
                updated_at = datetime.datetime.strptime(row['updated_at'], '%Y-%m-%d %H:%M:%S')
                entry = CustomerMeta(
                    customer_id=int(row['customer_id']),
                    marital_status=row['marital_status'].upper() == 'TRUE' if row['marital_status'] else None,
                    employment_status=EmploymentEnum(row['employment_status']).value if row['employment_status'] else None,
                    is_verified=row['is_verified'].upper() == 'TRUE' if row['is_verified'] else None,
                    abandoned_cart=int(row['abandoned_cart']) if row['abandoned_cart'] else None,
                    created_at=created_at,
                    updated_at=updated_at
                )
                entries.append(entry)

            db.add_all(entries)
            db.commit()
            print(f"Inserted {len(entries)} customer_meta records.")
    except Exception as e:
        db.rollback()
        print("Error inserting customer_meta:", e)

def insert_addresses_from_csv():
    try:
        with open("data/address_data.csv", newline='', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                row = {k.strip(): v.strip() if isinstance(v, str) else v for k, v in row.items()}
                address = Address(
                    address_id=int(row["address_id"]),
                    customer_id=int(row["customer_id"]),
                    address_line_1=row["address_line_1"],
                    address_line_2=row["address_line_2"],
                    city=row["city"],
                    state=row["state"],
                    country=row["country"],
                    postal_code=row["postal_code"],
                    address_type=AddressTypeEnum(row['address_type']).value,
                    default_address=row["default_address"].lower() == "true",
                    landmark=row["landmark"],
                    address_phone_no=row["address_phone_no"],
                    address_person_name=row["address_person_name"]
                )
                db.add(address)
            db.commit()
            print("Address data inserted successfully.")
    except Exception as e:
        db.rollback()
        print("Error inserting addresses:", e)

def insert_customer_preferences_from_csv():
    try:
        with open("data/customer_preferences.csv", newline='', encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            for row in reader:
                row = {k.strip(): v.strip() for k, v in row.items()}
                created_at = datetime.datetime.strptime(row["created_at"], "%Y-%m-%d %H:%M:%S")
                updated_at = datetime.datetime.strptime(row["updated_at"], "%Y-%m-%d %H:%M:%S")
                preference = CustomerPreference(
                    customer_id=int(row["customer_id"]),
                    style_preference_1=row["style_preference_1"],
                    style_preference_2=row["style_preference_2"],
                    style_preference_3=row["style_preference_3"],
                    marketing_opted_in=row["marketing_opted_in"].upper() == "TRUE",
                    preferred_language=row["preferred_language"],
                    created_at=created_at,
                    updated_at=updated_at
                )
                db.add(preference)
            db.commit()
            print("Customer preferences inserted successfully.")
    except Exception as e:
        db.rollback()
        print("Error inserting customer preferences:", e)
def insert_products_from_csv():
    try:
        with open("data/product.csv", newline='', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                row = {k.strip(): v.strip() for k, v in row.items()}
                product = Product(
                    product_id=int(row["product_id"]),
                    subcategory_id=int(row["subcategory_id"]),
                    brand=row["brand"],
                    material=row["material"],
                    vendor_name=row["vendor_name"],
                    min_order_qty=int(row["min_order_qty"]),
                    max_order_qty=int(row["max_order_qty"]),
                    launch_date=datetime.datetime.fromisoformat(row["launch_date"]),
                    rating=int(row["rating"]),
                    occasion=OccasionEnum(row["occasion"]).value,
                    style=StyleEnum(row["style"]).value,
                    season=SeasonEnum(row["season"]).value,
                    gender=ProductGenderEnum(row["gender"]).value,
                    product_name=row["product_name"],
                    product_desc=row["product_desc"],
                    created_at=datetime.datetime.fromisoformat(row["created_at"]),
                    updated_at=datetime.datetime.fromisoformat(row["updated_at"])
                )
                db.add(product)
            db.commit()
            print("Product data inserted successfully.")
    except Exception as e:
        db.rollback()
        print("Error inserting product data:", e)

def insert_product_variants_from_csv():
    try:
        with open("data/product_variant.csv", newline='', encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            for row in reader:
                row = {k.strip(): v.strip() for k, v in row.items()}
                variant = ProductVariant(
                    variant_id=int(row["variant_id"]),
                    product_id=int(row["product_id"]),
                    mrp=float(row["mrp"]),
                    discount_percent=float(row["discount_percent"]),
                    current_price=float(row["current_price"]),
                    color=row["color"],
                    size=row["size"],
                    img_url=row["img_url"],
                    est_delivery_time=row["est_delivery_time"],
                    created_at=datetime.datetime.strptime(row["created_at"], "%Y-%m-%d %H:%M:%S%z"),
                    updated_at=datetime.datetime.strptime(row["updated_at"], "%Y-%m-%d %H:%M:%S%z"),
                )
                db.add(variant)
            db.commit()
            print("Product variants inserted successfully.")
    except Exception as e:
        db.rollback()
        print("Error inserting product variants:", e)

def insert_inventory_from_csv():
    try:
        with open("data/inventory.csv", newline='', encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            for row in reader:
                row = {k.strip(): v.strip() for k, v in row.items()}
                entry = Inventory(
                    variant_id=int(row["variant_id"]),
                    quantity=int(row["quantity"]),
                    restock_level=int(row["restock_level"]),
                    created_at=datetime.datetime.strptime(row["created_at"], "%Y-%m-%d %H:%M:%S%z"),
                    updated_at=datetime.datetime.strptime(row["updated_at"], "%Y-%m-%d %H:%M:%S%z")
                )
                db.add(entry)
            db.commit()
            print("Inventory data inserted successfully.")
    except Exception as e:
        db.rollback()
        print("Error inserting inventory data:", e)

def insert_order_headers_from_csv():
    try:
        with open("data/order_header.csv", newline='', encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            entries = []

            for row in reader:
                row = {k.strip(): v.strip() for k, v in row.items()}
                
                order_date = parser.parse(row["order_date"]).strftime("%Y-%m-%d %H:%M:%S")
                created_at = parser.parse(row["created_at"]).strftime("%Y-%m-%d %H:%M:%S")
                updated_at = parser.parse(row["updated_at"]).strftime("%Y-%m-%d %H:%M:%S")

                entry = OrderHeader(
                    id=int(row["id"]),
                    order_date=datetime.datetime.strptime(order_date, "%Y-%m-%d %H:%M:%S"),
                    customer_id=int(row["customer_id"]),
                    status=row["status"],
                    total_amount=float(row["total_amount"]),
                    shipping_address_id=int(row["shipping_address_id"]),
                    created_at=datetime.datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S"),
                    updated_at=datetime.datetime.strptime(updated_at, "%Y-%m-%d %H:%M:%S")
                )
                entries.append(entry)

            db.add_all(entries)
            db.commit()
            print(f"{len(entries)} order headers inserted successfully.")
    except Exception as e:
        db.rollback()
        print("Error inserting order headers:", e)

def insert_order_items_from_csv():
    try:
        with open("data/order_items.csv", newline='', encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            entries = []

            for row in reader:
                row = {k.strip(): v.strip() for k, v in row.items()}
                created_at = parser.parse(row["created_at"])
                updated_at = parser.parse(row["updated_at"])

                entry = OrderItem(
                    order_id=int(row["order_id"]),
                    product_variant_id=int(row["product_variant_id"]),
                    quantity=int(row["quantity"]),
                    price=float(row["price"]),
                    offer_usage_id=int(row["offer_usage_id"]) if row["offer_usage_id"] else None,
                    created_at=created_at,
                    updated_at=updated_at
                )
                entries.append(entry)

            db.add_all(entries)
            db.commit()
            print(f"{len(entries)} order items inserted successfully.")
    except Exception as e:
        db.rollback()
        print("Error inserting order items:", e)

def insert_offers_from_csv():
    try:
        with open("data/offers.csv", newline='', encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            for row in reader:
                created_at = parser.parse(row["created_at"])
                updated_at = parser.parse(row["updated_at"])
                start_date = parser.parse(row["start_date"])
                end_date = parser.parse(row["end_date"])
                offer = Offer(
                    name=row["name"],
                    type=row["type"],
                    discount=float(row["discount"]),
                    start_date=start_date,
                    end_date=end_date,
                    applicable_products=ast.literal_eval(row["applicable_products"]),
                    created_at=created_at,
                    updated_at=updated_at
                )
                db.add(offer)

            db.commit()
            print("Offers inserted successfully.")
    except Exception as e:
        db.rollback()
        print("Error inserting offers:", e)

def insert_offer_usage_from_csv():
    try:
        with open("data/offer_usage.csv", newline='', encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            usages = []
            for row in reader:
                row = {k.strip(): v.strip() for k, v in row.items()}
                use_date = parser.parse(row["use_date"]).date()
                created_at = parser.parse(row["created_at"])
                updated_at = parser.parse(row["updated_at"])
                usage = OfferUsage(
                    offer_usage_id=int(row["offer_usage_id"]),
                    offer_id=int(row["offer_id"]),
                    user_id=int(row["user_id"]),
                    order_id=int(row["order_id"]),
                    discount_applied=float(row["discount_applied"]),
                    use_date=use_date,
                    created_at=created_at,
                    updated_at=updated_at
                )
                usages.append(usage)

            db.add_all(usages)
            db.commit()
            print(f"{len(usages)} offer_usage records inserted.")
    except Exception as e:
        db.rollback()
        print("Error inserting offer usage data:", e)

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    insert_customers_from_csv()
    insert_categories()
    insert_combos()
    insert_color_combinations()
    insert_customer_meta_from_csv()
    insert_addresses_from_csv()
    insert_customer_preferences_from_csv()
    insert_products_from_csv()
    insert_product_variants_from_csv()
    insert_inventory_from_csv()
    insert_order_headers_from_csv()
    insert_order_items_from_csv()
    insert_offers_from_csv()
    insert_offer_usage_from_csv()
    db.close()