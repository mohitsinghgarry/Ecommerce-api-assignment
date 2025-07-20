from fastapi import APIRouter, HTTPException, Query
from typing import List
from bson import ObjectId

from database import db, oid_to_str
from models import *

router = APIRouter()

# --- Product Routes ---
@router.post("/products", response_model=ProductOut, status_code=201)
def create_product(product: ProductIn):
    product_dict = product.model_dump()
    result = db.products.insert_one(product_dict)
    return {"id": oid_to_str(result.inserted_id)}

@router.get("/products", response_model=ProductPage)
def list_products(
    name: Optional[str] = Query(None),
    size: Optional[str] = Query(None),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    query = {}
    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    if size:
        query["sizes.size"] = size

    products_cursor = db.products.find(query).skip(offset).limit(limit)
    product_list = [prod for prod in products_cursor]
    for prod in product_list:
        prod["_id"] = oid_to_str(prod["_id"])

    page_info = {
        "limit": limit,
        "next": str(offset + limit) if len(product_list) == limit else None,
        "previous": str(offset - limit) if offset > 0 else None,
    }
    return {"data": product_list, "page": page_info}

# --- Order Routes ---
@router.post("/orders", response_model=OrderOut, status_code=201)
def create_order(order: OrderIn):
    order_dict = order.model_dump()
    total_amount = 0
    product_ids = [ObjectId(item['productId']) for item in order_dict['items']]
    products = db.products.find({"_id": {"$in": product_ids}})
    product_map = {oid_to_str(p["_id"]): p for p in products}

    for item in order_dict['items']:
        product = product_map.get(item['productId'])
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item['productId']} not found")
        total_amount += product['price'] * item['qty']

    order_dict['total'] = total_amount
    result = db.orders.insert_one(order_dict)
    return {"id": oid_to_str(result.inserted_id)}

# In routes.py

@router.get("/orders/{user_id}", response_model=OrderPage)
def list_orders(user_id: str, limit: int = 10, offset: int = 0):
    pipeline = [
        {"$match": {"userId": user_id}},
        {"$sort": {"_id": -1}},
        {"$skip": offset},
        {"$limit": limit},
        {"$unwind": "$items"},
        
        {
            "$addFields": {
                "items.productIdObj": {"$toObjectId": "$items.productId"}
            }
        },
        {
            "$lookup": {
                "from": "products",
                "localField": "items.productIdObj",
                "foreignField": "_id",
                "as": "productDetails"
            }
        },

        {"$unwind": "$productDetails"},
        {
            "$group": {
                "_id": "$_id",
                "total": {"$first": "$total"},
                "items": {
                    "$push": {
                        "qty": "$items.qty",
                        "productDetails": {
                            "_id": "$productDetails._id",
                            "name": "$productDetails.name"
                        }
                    }
                }
            }
        }
    ]
    
    orders_cursor = db.orders.aggregate(pipeline)
    order_list = [o for o in orders_cursor]
    
    for order in order_list:
        order['_id'] = oid_to_str(order['_id'])
        for item in order['items']:
            item['productDetails']['_id'] = oid_to_str(item['productDetails']['_id'])
    
    page_info = {
        "limit": limit,
        "next": str(offset + limit) if len(order_list) == limit else None,
        "previous": str(offset - limit) if offset > 0 else None,
    }
    
    return {"data": order_list, "page": page_info}