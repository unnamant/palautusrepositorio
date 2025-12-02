from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import db
from .models import Warehouse, Product

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    warehouses = Warehouse.query.all()
    return render_template('index.html', warehouses=warehouses)


# Warehouse routes
@bp.route('/warehouse/new', methods=['GET', 'POST'])
def new_warehouse():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()

        if not name:
            flash('Warehouse name is required', 'error')
            return render_template('warehouse_form.html', warehouse=None)

        warehouse = Warehouse(name=name, description=description)
        db.session.add(warehouse)
        db.session.commit()
        flash('Warehouse created successfully', 'success')
        return redirect(url_for('main.index'))

    return render_template('warehouse_form.html', warehouse=None)


@bp.route('/warehouse/<int:warehouse_id>')
def view_warehouse(warehouse_id):
    warehouse = Warehouse.query.get_or_404(warehouse_id)
    sort_by = request.args.get('sort', 'name')
    order = request.args.get('order', 'asc')
    search = request.args.get('search', '').strip()

    # Validate sort parameters
    if sort_by not in ['name', 'quantity']:
        sort_by = 'name'
    if order not in ['asc', 'desc']:
        order = 'asc'

    products = Product.query.filter_by(warehouse_id=warehouse_id)

    if search:
        products = products.filter(Product.name.ilike(f'%{search}%'))

    if sort_by == 'quantity':
        if order == 'desc':
            products = products.order_by(Product.quantity.desc())
        else:
            products = products.order_by(Product.quantity.asc())
    else:
        if order == 'desc':
            products = products.order_by(Product.name.desc())
        else:
            products = products.order_by(Product.name.asc())

    products = products.all()

    return render_template(
        'warehouse_detail.html',
        warehouse=warehouse,
        products=products,
        sort_by=sort_by,
        order=order,
        search=search
    )


@bp.route('/warehouse/<int:warehouse_id>/edit', methods=['GET', 'POST'])
def edit_warehouse(warehouse_id):
    warehouse = Warehouse.query.get_or_404(warehouse_id)

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()

        if not name:
            flash('Warehouse name is required', 'error')
            return render_template('warehouse_form.html', warehouse=warehouse)

        warehouse.name = name
        warehouse.description = description
        db.session.commit()
        flash('Warehouse updated successfully', 'success')
        return redirect(url_for('main.view_warehouse', warehouse_id=warehouse.id))

    return render_template('warehouse_form.html', warehouse=warehouse)


@bp.route('/warehouse/<int:warehouse_id>/delete', methods=['POST'])
def delete_warehouse(warehouse_id):
    warehouse = Warehouse.query.get_or_404(warehouse_id)
    db.session.delete(warehouse)
    db.session.commit()
    flash('Warehouse deleted successfully', 'success')
    return redirect(url_for('main.index'))


# Product routes
@bp.route('/warehouse/<int:warehouse_id>/product/new', methods=['GET', 'POST'])
def new_product(warehouse_id):
    warehouse = Warehouse.query.get_or_404(warehouse_id)

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        quantity_str = request.form.get('quantity', '0').strip()

        if not name:
            flash('Product name is required', 'error')
            return render_template(
                'product_form.html', warehouse=warehouse, product=None
            )

        try:
            quantity = int(quantity_str)
            if quantity < 0:
                raise ValueError("Quantity cannot be negative")
        except ValueError:
            flash('Invalid quantity', 'error')
            return render_template(
                'product_form.html', warehouse=warehouse, product=None
            )

        product = Product(name=name, quantity=quantity, warehouse_id=warehouse_id)
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully', 'success')
        return redirect(url_for('main.view_warehouse', warehouse_id=warehouse_id))

    return render_template('product_form.html', warehouse=warehouse, product=None)


@bp.route(
    '/warehouse/<int:warehouse_id>/product/<int:product_id>/edit',
    methods=['GET', 'POST']
)
def edit_product(warehouse_id, product_id):
    warehouse = Warehouse.query.get_or_404(warehouse_id)
    product = Product.query.get_or_404(product_id)

    if product.warehouse_id != warehouse_id:
        flash('Product not found in this warehouse', 'error')
        return redirect(url_for('main.view_warehouse', warehouse_id=warehouse_id))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        quantity_str = request.form.get('quantity', '0').strip()

        if not name:
            flash('Product name is required', 'error')
            return render_template(
                'product_form.html', warehouse=warehouse, product=product
            )

        try:
            quantity = int(quantity_str)
            if quantity < 0:
                raise ValueError("Quantity cannot be negative")
        except ValueError:
            flash('Invalid quantity', 'error')
            return render_template(
                'product_form.html', warehouse=warehouse, product=product
            )

        product.name = name
        product.quantity = quantity
        db.session.commit()
        flash('Product updated successfully', 'success')
        return redirect(url_for('main.view_warehouse', warehouse_id=warehouse_id))

    return render_template('product_form.html', warehouse=warehouse, product=product)


@bp.route(
    '/warehouse/<int:warehouse_id>/product/<int:product_id>/delete',
    methods=['POST']
)
def delete_product(warehouse_id, product_id):
    product = Product.query.get_or_404(product_id)

    if product.warehouse_id != warehouse_id:
        flash('Product not found in this warehouse', 'error')
        return redirect(url_for('main.view_warehouse', warehouse_id=warehouse_id))

    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully', 'success')
    return redirect(url_for('main.view_warehouse', warehouse_id=warehouse_id))


@bp.route(
    '/warehouse/<int:warehouse_id>/product/<int:product_id>/adjust',
    methods=['POST']
)
def adjust_quantity(warehouse_id, product_id):
    product = Product.query.get_or_404(product_id)

    if product.warehouse_id != warehouse_id:
        flash('Product not found in this warehouse', 'error')
        return redirect(url_for('main.view_warehouse', warehouse_id=warehouse_id))

    action = request.form.get('action')
    amount_str = request.form.get('amount', '1').strip()

    try:
        amount = int(amount_str)
        if amount < 1:
            raise ValueError("Amount must be at least 1")
    except ValueError:
        flash('Invalid amount', 'error')
        return redirect(url_for('main.view_warehouse', warehouse_id=warehouse_id))

    if action == 'increase':
        product.quantity += amount
        flash(f'Stock increased by {amount}', 'success')
    elif action == 'decrease':
        if product.quantity >= amount:
            product.quantity -= amount
            flash(f'Stock decreased by {amount}', 'success')
        else:
            flash('Cannot decrease below zero', 'error')
            return redirect(url_for('main.view_warehouse', warehouse_id=warehouse_id))
    else:
        flash('Invalid action', 'error')
        return redirect(url_for('main.view_warehouse', warehouse_id=warehouse_id))

    db.session.commit()
    return redirect(url_for('main.view_warehouse', warehouse_id=warehouse_id))
