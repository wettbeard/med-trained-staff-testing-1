from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Optional, Length
from datetime import date, timedelta

class HCPForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(max=100)])
    employee_id = StringField('Employee ID', validators=[Optional(), Length(max=50)])
    email = StringField('Email', validators=[Optional(), Email(), Length(max=120)])
    phone = StringField('Phone', validators=[Optional(), Length(max=20)])
    company_id = SelectField('Company', coerce=int, validators=[DataRequired()])
    hire_date = DateField('Hire Date', validators=[Optional()])
    is_active = BooleanField('Active', default=True)
    submit = SubmitField('Save HCP')

class CertificationForm(FlaskForm):
    hcp_id = SelectField('Healthcare Professional', coerce=int, validators=[DataRequired()])
    client_id = SelectField('Client', coerce=int, validators=[DataRequired()])
    certification_type = SelectField('Certification Type', choices=[
        ('medication_administration', 'Medication Administration'),
        ('insulin_administration', 'Insulin Administration'),
        ('emergency_medication', 'Emergency Medication'),
        ('controlled_substances', 'Controlled Substances')
    ], validators=[DataRequired()])
    issue_date = DateField('Issue Date', validators=[DataRequired()], default=date.today)
    expiry_date = DateField('Expiry Date', validators=[DataRequired()], 
                           default=lambda: date.today() + timedelta(days=365))
    notes = TextAreaField('Notes', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Issue Certification')

class RevokeCertificationForm(FlaskForm):
    reason = TextAreaField('Revocation Reason', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('Revoke Certification')

class ClientForm(FlaskForm):
    initials = StringField('Client Initials', validators=[DataRequired(), Length(max=10)])
    client_code = StringField('Client Code', validators=[Optional(), Length(max=20)])
    residence_id = SelectField('Residence', coerce=int, validators=[DataRequired()])
    is_primary = BooleanField('Primary Client')
    is_active = BooleanField('Active', default=True)
    submit = SubmitField('Save Client')