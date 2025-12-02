# Warehouse Manager

Web-based warehouse management application built with Flask.

## Features

- Create, edit, and delete multiple warehouses
- Add, edit, and delete products within each warehouse
- Adjust stock levels (increase/decrease quantities)
- Search products by name
- Sort products by name or quantity

## Installation

```bash
cd viikko5/warehouse
poetry install
```

## Running the Application

```bash
poetry run python run.py
```

The application will be available at http://127.0.0.1:5000

### Development Mode

To enable debug mode:

```bash
FLASK_DEBUG=true poetry run python run.py
```

## Running Tests

```bash
poetry run pytest
```
