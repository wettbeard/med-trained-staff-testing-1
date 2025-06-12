from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.admin import bp
from app.models import User, Company, HCP, Certification

def admin_required(f):
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Admin access required.', 'error')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/users')
@login_required
@admin_required
def user_management():
    users = User.query.all()
    return render_template('admin/user_management.html', users=users)

@bp.route('/user/<int:id>/toggle-status')
@login_required
@admin_required
def toggle_user_status(id):
    user = User.query.get_or_404(id)
    user.is_active = not user.is_active
    db.session.commit()
    status = 'activated' if user.is_active else 'deactivated'
    flash(f'User {user.username} has been {status}.', 'success')
    return redirect(url_for('admin.user_management'))

@bp.route('/user/<int:id>/change-role/<role>')
@login_required
@admin_required
def change_user_role(id, role):
    if role not in ['admin', 'nurse', 'viewer']:
        flash('Invalid role specified.', 'error')
        return redirect(url_for('admin.user_management'))
    
    user = User.query.get_or_404(id)
    old_role = user.role
    user.role = role
    db.session.commit()
    flash(f'User {user.username} role changed from {old_role} to {role}.', 'success')
    return redirect(url_for('admin.user_management'))

@bp.route('/reports')
@login_required
@admin_required
def reports():
    # Generate various reports
    total_users = User.query.count()
    active_users = User.query.filter_by(is_active=True).count()
    total_hcps = HCP.query.count()
    active_hcps = HCP.query.filter_by(is_active=True).count()
    total_certifications = Certification.query.count()
    active_certifications = Certification.query.filter_by(is_active=True).count()
    
    # Certifications by company
    company_stats = db.session.query(
        Company.name,
        db.func.count(Certification.id).label('cert_count')
    ).join(HCP).join(Certification).group_by(Company.name).all()
    
    return render_template('admin/reports.html',
                         total_users=total_users,
                         active_users=active_users,
                         total_hcps=total_hcps,
                         active_hcps=active_hcps,
                         total_certifications=total_certifications,
                         active_certifications=active_certifications,
                         company_stats=company_stats)