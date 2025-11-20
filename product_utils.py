import datetime
from db import db
from models import Product, ProductVariant, Inventory

def add_product_to_db(product):
    now = datetime.datetime.utcnow()
    new_product = Product(
        product_name=product["product_name"],
        brand=product["brand"],
        subcategory_id=int(product["subcategory_id"]),
        material=product["material"],
        vendor_name=product["vendor_name"],
        min_order_qty=int(product["min_order_qty"]),
        max_order_qty=int(product["max_order_qty"]),
        launch_date=now,
        rating=int(product["rating"]),
        occasion=product["occasion"],
        style=product["style"],
        season=product["season"],
        gender=product["gender"],
        product_desc=product["product_desc"],
        created_at=now,
        updated_at=now
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product.product_id

def add_variants_to_db(product_id, variants):
    now = datetime.datetime.utcnow()
    variant_ids = []
    for v in variants:
        variant = ProductVariant(
            product_id=product_id,
            mrp=float(v.get("mrp", 0)),
            discount_percent=float(v.get("discount_percent", 0)),
            current_price=float(v.get("current_price", 0)),
            color=v["color"],
            size=v["size"],
            img_url=v.get("img_url", ""),
            est_delivery_time=v.get("est_delivery_time", "3-5 days"),
            created_at=now,
            updated_at=now
        )
        db.add(variant)
        db.flush()
        variant_ids.append(variant.variant_id)
    db.commit()
    return variant_ids

def add_inventory_to_db(inventories):
    now = datetime.datetime.utcnow()
    for inv in inventories:
        entry = Inventory(
            variant_id=inv["variant_id"],
            quantity=int(inv.get("stock", 0)),
            restock_level=int(inv.get("restock_level", 5)),
            created_at=now,
            updated_at=now
        )
        db.add(entry)
    db.commit()
    return True
