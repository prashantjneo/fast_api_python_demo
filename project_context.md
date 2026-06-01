# Project Context: FastAPI Demo

## Directory Structure

- **config/**: Configuration settings and environment variables parsing.
- **database/**: Database connection setup and DB utilities. For now, contains `dummy_db.py` for in-memory mockup.
- **models/**: ORM models representing the database tables.
- **schemas/**: Pydantic schemas for request validation and response formatting.
- **repositories/**: Abstraction layer over the database operations. Contains generic operations.
- **services/**: Business logic layer. Services coordinate repositories and perform computations.
- **routers/**: FastAPI route definitions (endpoints). These call the service layer.

## Generic CRUD Pattern

The project currently uses a generic repository pattern to handle basic CRUD (Create, Read, Update, Delete) operations without having to write duplicate code for every new table.

### How to use the GenericRepository

When you want to perform operations on a new table, you just instantiate the `GenericRepository` with the table name.

```python
from repositories.generic_repository import GenericRepository

# Example for a "products" table
product_repo = GenericRepository(table_name="products")

# Create a new product
new_product = product_repo.create({"name": "Laptop", "price": 1000.0})

# Get all products
all_products = product_repo.get_all()

# Get product by ID
product = product_repo.get_by_id(1)

# Update product
updated_product = product_repo.update(1, {"price": 950.0})

# Delete product
product_repo.delete(1)
```

Currently, the `GenericRepository` stores data in a simple in-memory dictionary located in `database/dummy_db.py`. When we transition to a real database (like PostgreSQL with SQLAlchemy), we can update the `GenericRepository` class, and all other services utilizing it will automatically start interacting with the real database.
