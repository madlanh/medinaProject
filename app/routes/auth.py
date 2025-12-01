from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from app.models.models import User
from app.utils.decorators import login_required

auth_bp = Blueprint('auth', __name__)

from werkzeug.security import check_password_hash

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login berhasil!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('admin.dashboard'))
        else:
            flash('Username atau password salah.', 'danger')

    return render_template('admin_login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    session.clear()
    flash('Anda telah logout.', 'success')
    return redirect(url_for('auth.login'))
