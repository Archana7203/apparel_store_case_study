# --- Imports ---
from fastapi import FastAPI, Query, Request, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from combo_logic import generate_combos
from email_utils import process_and_send_emails
from product_utils import add_product_to_db, add_variants_to_db, add_inventory_to_db
from db import db
import traceback
from models import Product, ProductVariant

# --- FastAPI app setup ---
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/image", StaticFiles(directory="image"), name="image")
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- API endpoint: Send emails and return recipients ---
@app.post("/api/send_emails")
def api_send_emails(product: dict = Body(...)):
    try:
        recipients = process_and_send_emails(product)
        return {"recipients": recipients}
    except Exception as e:
        print("Exception in /api/send_emails:")
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e), "trace": traceback.format_exc()})

# --- Admin page ---
@app.get("/admin", response_class=HTMLResponse)
def serve_admin(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})

# --- Landing page route ---
@app.get("/", response_class=HTMLResponse)
def serve_landing(request: Request):
    return templates.TemplateResponse("landing.html", {"request": request})

# --- /home route to serve the main home page (index.html or home.html) ---
@app.get("/home", response_class=HTMLResponse)
def serve_home(request: Request):
    return FileResponse("index.html")

# --- Products page ---
@app.get("/products", response_class=HTMLResponse)
def serve_products(request: Request):
    return templates.TemplateResponse("products.html", {"request": request})

# --- Product detail page ---
@app.get("/product/{product_id}", response_class=HTMLResponse)
def serve_product_detail(request: Request, product_id: int):
    return templates.TemplateResponse("product_detail.html", {"request": request, "product_id": product_id})

# --- API endpoint: Get 400 products ---
@app.get("/api/products")
def api_get_products():
    products = []
    product_objs = db.query(Product).limit(400).all()
    for prod in product_objs:
        variant = db.query(ProductVariant).filter(ProductVariant.product_id == prod.product_id).first()
        products.append({
            "product_id": prod.product_id,
            "name": prod.product_name,
            "brand": prod.brand,
            "color": variant.color if variant else '',
            "style": prod.style,
            "image": variant.img_url if variant and variant.img_url else '',
        })
    return {"products": products}

# --- API endpoint: Get product detail and variants ---
@app.get("/api/product/{product_id}")
def api_get_product_detail(product_id: int):
    prod = db.query(Product).filter(Product.product_id == product_id).first()
    product_variants = db.query(ProductVariant).filter(ProductVariant.product_id == product_id).all()
    first_variant = product_variants[0] if product_variants else None
    return {
        "product_id": prod.product_id,
        "name": prod.product_name,
        "brand": prod.brand,
        "color": first_variant.color if first_variant else '',
        "style": prod.style,
        "description": prod.product_desc,
        "image": first_variant.img_url if first_variant and first_variant.img_url else '',
        "price": first_variant.current_price if first_variant else '',
        "variants": [
            {
                "variant_id": v.variant_id,
                "color": v.color,
                "size": v.size,
                "current_price": v.current_price
            } for v in product_variants
        ]
    }

# --- API endpoint: Get recommendations for a variant ---
@app.get("/api/recommendations")
def api_get_recommendations(variant_id: int):
    variant = db.query(ProductVariant).filter(ProductVariant.variant_id == variant_id).first()
    product = db.query(Product).filter(Product.product_id == variant.product_id).first() if variant else None
    combos = generate_combos(product.product_name, int(variant_id)) if product else {"combos": []}
    return {"combos": combos.get("combos", [])}

# --- API endpoint: Get recommendations by query ---
@app.get("/recommendations")
def get_recommendations(query: str = Query(...)):
    try:
        result = generate_combos(query)
        if "error" in result:
            return JSONResponse(result, status_code=404)
        return result
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

# --- API endpoint: Add product (step 1) ---
@app.post("/api/add_product")
def add_product(product: dict = Body(...)):
    product_id = add_product_to_db(product)
    return {"success": True, "product_id": product_id}

# --- API endpoint: Add variants (step 2) ---
@app.post("/api/add_variants")
def add_variants(data: dict = Body(...)):
    product_id = data["product_id"]
    variants = data["variants"]
    variant_ids = add_variants_to_db(product_id, variants)
    return {"success": True, "variant_ids": variant_ids}

# --- API endpoint: Add inventory (step 3) ---
@app.post("/api/add_inventory")
def add_inventory(data: dict = Body(...)):
    inventories = data["inventories"]
    add_inventory_to_db(inventories)
    return {"success": True}
