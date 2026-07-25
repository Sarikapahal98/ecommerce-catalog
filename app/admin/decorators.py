from functools import wraps
from flask import g, flash, redirect, url_for

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.user or not g.user.is_admin:
            flash('Admin access required.')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function