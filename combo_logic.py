from sqlalchemy import select, func
from sqlalchemy.orm import joinedload
from database import db
from models import Combination, Product, ProductVariant, Inventory, ColorCombination, Sub_Category
import os
import random

def extract_gender(query: str):
    query = query.lower()
    if "men" in query or "man" in query:
        return "Men"
    elif "women" in query or "lady" in query or "ladies" in query:
        return "Women"
    elif "unisex" in query:
        return "Unisex"
    return None

def get_color_score(base, match):
    score = db.execute(
        select(ColorCombination.score)
        .where(ColorCombination.base_color == base)
        .where(ColorCombination.matching_color == match)
    ).scalar()
    return score

def generate_combos(product_name: str, variant_id: int = None):
    # Find the product by name
    product_row = db.execute(
        select(Product, ProductVariant)
        .join(ProductVariant)
        .where(Product.product_name == product_name)
        .order_by(ProductVariant.variant_id)
    ).first() if not variant_id else db.execute(
        select(Product, ProductVariant)
        .join(ProductVariant)
        .where(Product.product_name == product_name)
        .where(ProductVariant.variant_id == variant_id)
    ).first()

    if not product_row:
        return {"error": "Product not found"}

    main_product, main_variant = product_row
    gender = main_product.gender
    subcat_id = main_product.subcategory_id
    main_style = getattr(main_product, 'style', None)

    def get_combos_for_gender(target_gender):
        combos_raw = db.execute(
            select(Combination).where(Combination.subcategory_id == subcat_id)
        ).scalars().all()
        result_combos = []
        for combo in combos_raw:
            current = []
            valid = True
            for sub_id in combo.combo_list.keys():
                product_row = db.execute(
                    select(Product, ProductVariant)
                    .join(ProductVariant)
                    .join(Inventory)
                    .where(Product.subcategory_id == sub_id)
                    .where(Inventory.quantity > 0)
                    .where(Product.gender == target_gender)
                    .where(Product.style == main_style)  # Match style
                    .order_by(func.random())
                ).first()
                if not product_row:
                    valid = False
                    break
                prod, variant = product_row
                color_score = get_color_score(main_variant.color, variant.color)
                if color_score < 7:
                    valid = False
                    break
                # Check if local image exists, else set to empty string
                local_img_path = f"image/{prod.product_id}.jpg"
                if os.path.exists(local_img_path):
                    img_url = f"/image/{prod.product_id}.jpg"
                else:
                    img_url = ""
                current.append({
                    "product": prod.product_name,
                    "brand": prod.brand,
                    "color": variant.color,
                    "price": variant.current_price,
                    "image": img_url
                })
            if valid and len(current) == len(combo.combo_list):
                result_combos.append({"items": current})
        return result_combos

    # Try gender-specific combos first
    combos = get_combos_for_gender(gender)
    # If not enough, try unisex combos
    if len(combos) < 1 and gender != "Unisex":
        combos = get_combos_for_gender("Unisex")
    if len(combos) < 1:
        return {"error": "Not enough valid combos found"}
    top_combos = combos[:5]
    return {
        "product_name": main_product.product_name,
        "description": getattr(main_product, "product_desc", ""),
        "brand": main_product.brand,
        "color": main_variant.color,
        "product_price": main_variant.current_price,
        "combos": top_combos
    }