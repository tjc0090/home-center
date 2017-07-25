from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from . import auth
from forms import LoginForm
from ..models import User

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle requests to the /login route
    Log an employee in through the login form
    """
    form = LoginForm()

    if form.validate_on_submit():
        #confirms user and password exist and match
        admin = User.get_user(form.username.data)
        if admin is not None and User.check_pass(form.username.data, form.password.data):
            admin_obj = User(admin)
            print admin
            print str(admin["_id"])
            print admin_obj
            login_user(admin_obj)

            return redirect(url_for('admin.admin_dashboard'))

            # if admin["is_admin"]:
            #     print "success"
                #return redirect(url_for('home.admin_dashboard'))

        else:
            flash('Invalid email or password.')

    return render_template('auth/login.html', form=form, title='Login')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have successfully been logged out')

    return redirect(url_for('auth.login'))
