from datetime import date, timedelta
from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.main import bp
from app.main.forms import HCPForm, CertificationForm, RevokeCertificationForm, ClientForm
from app.models import User, Company, HCP, Client, Residence, Certification

@bp.route('/')
@bp.route('/dashboard')
@login_required
def dashboard():
    # Get statistics
    total_hcps = HCP.query.filter_by(is_active=True).count()
    total_certifications = Certification.query.filter_by(is_active=True).count()
    
    # Expiring certifications (next 30 days)
    expiry_threshold = date.today() + timedelta(days=30)
    expiring_certs = Certification.query.filter(
        Certification.is_active == True,
        Certification.expiry_date <= expiry_threshold,
        Certification.expiry_date >= date.today()
    ).all()
    
    # Recent certifications
    recent_certs = Certification.query.filter_by(is_active=True)\
        .order_by(Certification.created_at.desc()).limit(5).all()
    
    return render_template('main/dashboard.html',
                         total_hcps=total_hcps,
                         total_certifications=total_certifications,
                         expiring_certs=expiring_certs,
                         recent_certs=recent_certs)

@bp.route('/hcps')
@login_required
def hcp_list():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    
    query = HCP.query.filter_by(is_active=True)
    
    if search:
        query = query.filter(HCP.name.contains(search))
    
    # Filter based on user role
    if current_user.role == 'nurse':
        query = query.filter_by(company_id=current_user.company_id)
    
    hcps = query.order_by(HCP.name).paginate(
        page=page, per_page=20, error_out=False)
    
    return render_template('main/hcp_list.html', hcps=hcps, search=search)

@bp.route('/hcp/<int:id>')
@login_required
def hcp_detail(id):
    hcp = HCP.query.get_or_404(id)
    
    # Check permissions
    if current_user.role == 'viewer' or \
       (current_user.role == 'nurse' and hcp.company_id != current_user.company_id):
        # Limited view for viewers and nurses from other companies
        pass
    
    active_certs = hcp.active_certifications
    expired_certs = hcp.expired_certifications
    
    return render_template('main/hcp_detail.html', 
                         hcp=hcp, 
                         active_certs=active_certs,
                         expired_certs=expired_certs)

@bp.route('/hcp/new', methods=['GET', 'POST'])
@login_required
def hcp_create():
    if current_user.role == 'viewer':
        flash('You do not have permission to create HCPs.', 'error')
        return redirect(url_for('main.hcp_list'))
    
    form = HCPForm()
    
    # Set company choices based on user role
    if current_user.role == 'admin':
        form.company_id.choices = [(c.id, c.name) for c in Company.query.filter_by(is_active=True).all()]
    else:
        form.company_id.choices = [(current_user.company_id, current_user.company.name)]
        form.company_id.data = current_user.company_id
    
    if form.validate_on_submit():
        hcp = HCP(
            name=form.name.data,
            employee_id=form.employee_id.data,
            email=form.email.data,
            phone=form.phone.data,
            company_id=form.company_id.data,
            hire_date=form.hire_date.data,
            is_active=form.is_active.data
        )
        db.session.add(hcp)
        db.session.commit()
        flash(f'HCP {hcp.name} has been created successfully.', 'success')
        return redirect(url_for('main.hcp_detail', id=hcp.id))
    
    return render_template('main/hcp_form.html', form=form, title='Create HCP')

@bp.route('/certifications')
@login_required
def certification_list():
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', 'active', type=str)
    
    query = Certification.query
    
    if status == 'active':
        query = query.filter_by(is_active=True)
    elif status == 'expired':
        query = query.filter(Certification.expiry_date < date.today())
    elif status == 'expiring':
        expiry_threshold = date.today() + timedelta(days=30)
        query = query.filter(
            Certification.is_active == True,
            Certification.expiry_date <= expiry_threshold,
            Certification.expiry_date >= date.today()
        )
    
    # Filter based on user role
    if current_user.role == 'nurse':
        query = query.join(HCP).filter(HCP.company_id == current_user.company_id)
    
    certifications = query.order_by(Certification.expiry_date.asc()).paginate(
        page=page, per_page=20, error_out=False)
    
    return render_template('main/certification_list.html', 
                         certifications=certifications, 
                         status=status)

@bp.route('/certification/new', methods=['GET', 'POST'])
@login_required
def certification_create():
    if current_user.role == 'viewer':
        flash('You do not have permission to issue certifications.', 'error')
        return redirect(url_for('main.certification_list'))
    
    form = CertificationForm()
    
    # Set choices based on user role
    if current_user.role == 'admin':
        form.hcp_id.choices = [(h.id, f"{h.name} ({h.company.name})") 
                              for h in HCP.query.filter_by(is_active=True).all()]
    else:
        form.hcp_id.choices = [(h.id, h.name) 
                              for h in HCP.query.filter_by(
                                  company_id=current_user.company_id, 
                                  is_active=True).all()]
    
    form.client_id.choices = [(c.id, f"{c.initials} ({c.residence.name})") 
                             for c in Client.query.filter_by(is_active=True).all()]
    
    if form.validate_on_submit():
        certification = Certification(
            hcp_id=form.hcp_id.data,
            client_id=form.client_id.data,
            certification_type=form.certification_type.data,
            issue_date=form.issue_date.data,
            expiry_date=form.expiry_date.data,
            issued_by=current_user.id,
            notes=form.notes.data
        )
        db.session.add(certification)
        db.session.commit()
        flash('Certification has been issued successfully.', 'success')
        return redirect(url_for('main.certification_list'))
    
    return render_template('main/certification_form.html', form=form, title='Issue Certification')

@bp.route('/certification/<int:id>/revoke', methods=['GET', 'POST'])
@login_required
def certification_revoke(id):
    certification = Certification.query.get_or_404(id)
    
    # Check permissions
    if current_user.role == 'viewer' or \
       (current_user.role == 'nurse' and certification.hcp.company_id != current_user.company_id):
        flash('You do not have permission to revoke this certification.', 'error')
        return redirect(url_for('main.certification_list'))
    
    if not certification.is_active:
        flash('This certification is already revoked.', 'warning')
        return redirect(url_for('main.certification_list'))
    
    form = RevokeCertificationForm()
    
    if form.validate_on_submit():
        certification.revoke(current_user, form.reason.data)
        db.session.commit()
        flash('Certification has been revoked successfully.', 'success')
        return redirect(url_for('main.certification_list'))
    
    return render_template('main/revoke_certification.html', 
                         form=form, 
                         certification=certification)