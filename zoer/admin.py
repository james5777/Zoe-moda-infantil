from flask import Blueprint, render_template, request, url_for, redirect, flash, session, g

from werkzeug.security import generate_password_hash, check_password_hash

from .models import Administrador

from zoer import db

import functools



bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/admin_dashboard')
def admin_dashboard():
    return render_template('admin/admin_dashboard.html')



@bp.route('/crear_producto')
def crear_producto():
    return render_template('admin/crear_producto.html')



@bp.route('/manage_carousel')
def manage_carousel():
    return render_template('admin/manage_carousel.html')



@bp.route('/list_products')
def list_products():
    return render_template('admin/list_products.html')







@bp.route('/list_orders')
def list_orders():
    return render_template('admin/list_orders.html')



@bp.route('/list_users')
def list_users():
    return render_template('admin/list_users.html')