import json, os


from flask import abort, current_app as app, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from . import admin
from forms import TableForm
from ..models import User, Table

def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)

@admin.route('/admin-dashboard', methods=['GET', 'POST'])
@login_required
def admin_dashboard():
    """
    Route for admin home page, contains links to catalog and account mgmt
    """
    check_admin()

    return render_template('admin/admin-dashboard.html')

@admin.route('update-catalog', methods=['GET', 'POST'])
@login_required
def update_catalog():
    """
    Route for editing, creating, or deleting items
    """
    check_admin()

    form = TableForm()

    if form.validate_on_submit():
        new_table = {"name": form.name.data,
                    "catalog_no": form.catalog_no.data,
                    "price": form.price.data,
                    "length": form.length.data,
                    "width": form.width.data,
                    "height": form.height.data,
                    "color": form.color.data,
                    "chair_count": form.chair_count.data,
                    "chair_color": form.chair_color.data,
                    "chair_height": form.chair_height.data,
                    "chair_length": form.chair_length.data,
                    "chair_width": form.chair_width.data
                    }
        photo = form.image.data
        filename = secure_filename(photo.filename)
        photo.save(os.path.join(app.config["UPLOAD_PATH"], filename))
        print new_table
        new_table["photo"] = os.path.join(app.config["UPLOAD_PATH"], filename)
        Table.insert_table(new_table)
        flash('Dining table successfully added.')

    return render_template('admin/update-catalog.html', action="Add", form=form,
                            title="Update Catalog")

@admin.route('edit-catalog', methods=['GET', 'POST'])
@login_required
def edit_catalog():
    """
    View to edit or delete existing catalog item
    """
    check_admin()

    form = TableForm()

    return render_template('admin/edit-catalog.html', action="Edit", form=form, title="Edit Catalog")

@admin.route('/api-edit', methods=['GET', 'POST'])
@login_required
def perform_edit():
    """
    Passes updated data to db, uploads new photo, removes old photo
    """
    raw_table = dict(request.form)
    json_table = json.loads(raw_table['newData'][0])
    table_id = json_table["id"]
    updated_table = {
                    "name": json_table['name'],
                    "catalog_no": json_table['catalog_no'],
                    "price": json_table['price'],
                    "length": json_table["length"],
                    "width": json_table["width"],
                    "height": json_table["height"],
                    "color": json_table['color'],
                    "chair_count": json_table["chair_count"],
                    "chair_color": json_table["chair_color"],
                    "chair_length": json_table["chair_length"],
                    "chair_width": json_table["chair_width"],
                    "chair_height": json_table["chair_height"],
                    }
    print updated_table

    old_photo = json_table['photoToRemove']
    if old_photo != 'None':

        print 'photo being updated'
        f = request.files['image']

        os.remove(os.path.join(app.config["UPLOAD_PATH"], old_photo))

        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config["UPLOAD_PATH"], filename))
        updated_table["photo"] = os.path.join(app.config["UPLOAD_PATH"], filename)

    response = Table.update_table(table_id, updated_table)
    return 'success'

@admin.route('/api-delete', methods=['GET', 'POST'])
@login_required
def perform_delete():
    """
    deletes item from db based on catalog no., removes photo
    """
    check_admin()

    searchObj = json.loads(request.data)

    deleted_table = Table.delete_table(searchObj)

    os.remove(os.path.join(app.config["UPLOAD_PATH"], deleted_table))

    return jsonify(res='success')
