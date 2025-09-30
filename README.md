#  Stock Management System (Flask REST API)

A simple **Flask-based REST API** for managing products in an **e-commerce stock inventory system**.  
Includes **CRUD operations** and a **restock logic** that flags products when available stock drops below 20% of total quantity.  

---

## 🚀 Features
- **Product Management**
  - Add, update, retrieve, delete products
- **Restock Logic**
  - Auto-calculates restock status (`available_quantity < 20% of total_quantity`)
  - Manual override of restock status
- **API Endpoints**
  - JSON-based REST API
- **Modular Structure**
  - Models, routes, services, database setup
- **Unit Tests**
  - Written using **pytest**

---

## Project Structure
```bash
stock_management/
│── app.py                  # Entry point
│── config.py               # App configuration (DB URL, settings)
│── database.py             # SQLAlchemy database setup
│── requirements.txt        # Python dependencies
│
├── models/
│   └── product.py          # Product model (SQLAlchemy ORM)
│
├── routes/
│   ├── product_routes.py   # CRUD API endpoints
│   └── restock_routes.py   # Restock logic endpoints
│
├── services/
│   └── product_service.py  # Business logic for product operations
│
└── tests/
    └── test_product_api.py # Unit tests for API
```

---

## ⚙️ Installation & Setup

### 1. Clone repository & create virtual environment
```bash
git clone <your-repo-url>
cd stock_management
python -m venv venv
venv\Scripts\activate 
pip install -r requirements.txt  # Install dependencies
python app.py  # Run python app
```