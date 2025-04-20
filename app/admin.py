from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from app.models import Product
from app import db

admin = Blueprint('admin', __name__)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


@admin.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if not current_user.is_admin:
        return redirect(url_for('views.index'))

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = float(request.form.get('price'))
        category = request.form.get('category')

        if 'image' not in request.files:
            flash('No image selected')
            return redirect(request.url)

        file = request.files['image']
        if file.filename == '':
            flash('No image selected')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

            new_product = Product(
                name=name,
                description=description,
                price=price,
                category=category,
                image=filename
            )

            db.session.add(new_product)
            db.session.commit()

            flash('Product added successfully!')
            return redirect(url_for('admin.add_product'))

    return render_template('admin/add_product.html')