from itertools import product
from mimetypes import init



import database_models
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import Product
from database import  engine, get_db
from sqlalchemy.orm import Session



app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

database_models.Base.metadata.create_all(bind=engine)

@app.get("/")
def greet():
    return {"message": "Welcome to FastAPI"}

products = [
    Product(
        id=1,
        name="phone",
        description="A smartphone",
        price=999.99,
        quantity=10
    ),
    Product(
        id=2,
        name="laptop",
        description="A high-performance laptop",
        price=1999.99,
        quantity=5
    ),
    Product(
        id=3,
        name="tablet",
        description="A portable tablet",
        price=599.99,
        quantity=15
    ),
    Product(
        id=4,
        name="headphones",
        description="Noise-cancelling headphones",
        price=299.99,
        quantity=20
    ),
    Product(
        id=5,
        name="smartwatch",
        description="A feature-rich smartwatch",
        price=399.99,
        quantity=10
    ),
    Product(
        id=6,
        name="camera",
        description="A digital camera",
        price=499.99,
        quantity=8
    )
]




@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    return db.query(database_models.Product).all()


@app.get("/products/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/products")
def add_product(product: Product, db: Session = Depends(get_db)): 
    db_product = database_models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@app.put("/products/{id}")
def update_product(id: int, updated_product: Product, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if not db_product:
        return None
    for key, value in updated_product.model_dump().items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return db_product


