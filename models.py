from sqlalchemy import Integer, String, Float, Boolean, Date, DateTime, ForeignKey, ARRAY, JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base
import datetime
from enums import *

class Category(Base):
    __tablename__ = 'category'
    category_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    category_name: Mapped[str] = mapped_column(String(50), nullable=False)
    subcategories: Mapped[list["Sub_Category"]] = relationship(back_populates="parent_category", cascade="all, delete-orphan")

class Sub_Category(Base):
    __tablename__ = 'sub_category'
    subcategory_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    subcategory_name: Mapped[str] = mapped_column(String(50), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey('category.category_id'))
    parent_category: Mapped["Category"] = relationship(back_populates="subcategories")
    combinations: Mapped[list["Combination"]] = relationship(back_populates="subcategory")
    products: Mapped[list["Product"]] = relationship(back_populates="subcategory")

class Combination(Base):
    __tablename__ = 'combination_table'
    combo_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    subcategory_id: Mapped[int] = mapped_column(ForeignKey("sub_category.subcategory_id"), nullable=False)
    combo_list: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime)
    subcategory: Mapped["Sub_Category"] = relationship(back_populates="combinations")

class ColorCombination(Base):
    __tablename__ = "color_combination"
    color_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    base_color: Mapped[str] = mapped_column(String(50), nullable=False)
    matching_color: Mapped[str] = mapped_column(String(50), nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)

class CustomerPersonal(Base):
    __tablename__ = 'customer_personal'
    customer_id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email_id: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    phone_number: Mapped[str] = mapped_column(String(15), nullable=False)
    date_of_birth: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    gender: Mapped[GenderEnum] = mapped_column(String(10), nullable=False)
    profile_pic: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime.date] = mapped_column(Date, default=datetime.date.today)
    last_login: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)
    active_status: Mapped[ActiveStatusEnum] = mapped_column(String(10), nullable=False)
    meta: Mapped["CustomerMeta"] = relationship(back_populates="customer", uselist=False)
    addresses: Mapped[list["Address"]] = relationship(back_populates="customer", cascade="all, delete-orphan")
    preferences = relationship("CustomerPreference", back_populates="customer", lazy="joined")
    orders: Mapped[list["OrderHeader"]] = relationship(back_populates="customer", cascade="all, delete-orphan")

class CustomerMeta(Base):
    __tablename__ = 'customer_meta'
    meta_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer_personal.customer_id"), nullable=False)
    marital_status: Mapped[bool | None] = mapped_column(Boolean)
    employment_status: Mapped[EmploymentEnum | None] = mapped_column(String(50))
    is_verified: Mapped[bool | None] = mapped_column(Boolean)
    abandoned_cart: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime)
    customer: Mapped["CustomerPersonal"] = relationship(back_populates="meta")

class Address(Base):
    __tablename__ = "address"
    address_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer_personal.customer_id"), nullable=False)
    address_line_1: Mapped[str] = mapped_column(String(100), nullable=False)
    address_line_2: Mapped[str] = mapped_column(String(100), nullable=True)
    city: Mapped[str] = mapped_column(String(50), nullable=False)
    state: Mapped[str] = mapped_column(String(50), nullable=False)
    country: Mapped[str] = mapped_column(String(50), nullable=False)
    postal_code: Mapped[str] = mapped_column(String(20), nullable=False)
    address_type: Mapped[AddressTypeEnum] = mapped_column(String(20), nullable=False)
    default_address: Mapped[bool] = mapped_column(Boolean, default=False)
    landmark: Mapped[str] = mapped_column(String(100), nullable=True)
    address_phone_no: Mapped[str] = mapped_column(String(20), nullable=False)
    address_person_name: Mapped[str] = mapped_column(String(50), nullable=False)
    customer: Mapped["CustomerPersonal"] = relationship(back_populates="addresses", lazy="joined")
    orders: Mapped[list["OrderHeader"]] = relationship(back_populates="address", cascade="all, delete-orphan")

class CustomerPreference(Base):
    __tablename__ = "customer_preferences"
    preference_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer_personal.customer_id"), nullable=False)
    style_preference_1: Mapped[StyleEnum] = mapped_column(String(30))
    style_preference_2: Mapped[StyleEnum] = mapped_column(String(30))
    style_preference_3: Mapped[StyleEnum] = mapped_column(String(30))
    marketing_opted_in: Mapped[bool] = mapped_column(Boolean, default=False)
    preferred_language: Mapped[str] = mapped_column(String(30))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime)
    customer = relationship("CustomerPersonal", back_populates="preferences")

class Product(Base):
    __tablename__ = "product"
    product_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    subcategory_id: Mapped[int] = mapped_column(ForeignKey("sub_category.subcategory_id"), nullable=False)
    brand: Mapped[str] = mapped_column(String(100), nullable=False)
    material: Mapped[str] = mapped_column(String(100), nullable=False)
    vendor_name: Mapped[str] = mapped_column(String(100), nullable=False)
    min_order_qty: Mapped[int] = mapped_column(Integer, nullable=False)
    max_order_qty: Mapped[int] = mapped_column(Integer, nullable=False)
    launch_date: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    occasion: Mapped[OccasionEnum] = mapped_column(String(50), nullable=False)
    style: Mapped[StyleEnum] = mapped_column(String(50), nullable=False)
    season: Mapped[SeasonEnum] = mapped_column(String(20), nullable=False)
    gender: Mapped[ProductGenderEnum] = mapped_column(String(20), nullable=False)
    product_name: Mapped[str] = mapped_column(String(200), nullable=False)
    product_desc: Mapped[str] = mapped_column(String(500), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    subcategory = relationship("Sub_Category", back_populates="products")
    variants: Mapped[list["ProductVariant"]] = relationship(back_populates="product", cascade="all, delete-orphan")

class ProductVariant(Base):
    __tablename__ = "product_variant"

    variant_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.product_id"), nullable=False)
    mrp: Mapped[float] = mapped_column(Float, nullable=False)
    discount_percent: Mapped[float] = mapped_column(Float, nullable=False)
    current_price: Mapped[float] = mapped_column(Float, nullable=False)
    color: Mapped[str] = mapped_column(String(30), nullable=False)
    size: Mapped[str] = mapped_column(String(30), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=True)
    est_delivery_time: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime)

    product = relationship("Product", back_populates="variants")
    inventory: Mapped["Inventory"] = relationship(back_populates="variant", uselist=False, cascade="all, delete-orphan")


class Inventory(Base):
    __tablename__ = "inventory"

    variant_id: Mapped[int] = mapped_column(ForeignKey("product_variant.variant_id"), primary_key=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    restock_level: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)

    variant: Mapped["ProductVariant"] = relationship(back_populates="inventory")


class OrderHeader(Base):
    __tablename__ = "order_header"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_date: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer_personal.customer_id"), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    total_amount: Mapped[float] = mapped_column(Float, nullable=False)
    shipping_address_id: Mapped[int] = mapped_column(ForeignKey("address.address_id"), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)

    customer: Mapped["CustomerPersonal"] = relationship()
    address: Mapped["Address"] = relationship()
    items: Mapped[list["OrderItem"]] = relationship(back_populates="order", cascade="all, delete-orphan")
    offer_usages: Mapped[list["OfferUsage"]] = relationship(back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("order_header.id"), nullable=False)
    product_variant_id: Mapped[int] = mapped_column(ForeignKey("product_variant.variant_id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    offer_usage_id: Mapped[int | None] = mapped_column(ForeignKey("offer_usage.offer_usage_id"), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)

    order = relationship("OrderHeader", back_populates="items")
    variant = relationship("ProductVariant")
    offer_usage = relationship("OfferUsage", lazy="joined", uselist=False)


class Offer(Base):
    __tablename__ = "offers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)  # e.g. 'season', 'coupon'
    discount: Mapped[float] = mapped_column(Float, nullable=False)
    start_date: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    applicable_products: Mapped[list[int]] = mapped_column(ARRAY(Integer), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)

    usages: Mapped[list["OfferUsage"]] = relationship(back_populates="offer", cascade="all, delete-orphan")


class OfferUsage(Base):
    __tablename__ = "offer_usage"

    offer_usage_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    offer_id: Mapped[int] = mapped_column(ForeignKey("offers.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("customer_personal.customer_id"), nullable=False)
    order_id: Mapped[int] = mapped_column(ForeignKey("order_header.id"), nullable=False)
    discount_applied: Mapped[float] = mapped_column(Float, nullable=False)
    use_date: Mapped[datetime.date] = mapped_column(Date)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime)

    offer: Mapped["Offer"] = relationship(back_populates="usages")
    customer: Mapped["CustomerPersonal"] = relationship()
    order: Mapped["OrderHeader"] = relationship(back_populates="offer_usages")
