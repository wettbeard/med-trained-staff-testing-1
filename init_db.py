from app import create_app, db
from app.models import User, Company, HCP, Client, Residence, Certification
from datetime import date, timedelta
from werkzeug.security import generate_password_hash

def init_database():
    app = create_app()
    
    with app.app_context():
        # Drop all tables and recreate
        db.drop_all()
        db.create_all()
        
        # Create sample companies
        companies = [
            Company(name='MedCare Solutions', address='123 Healthcare Ave', phone='555-0101', email='info@medcare.com'),
            Company(name='Wellness Partners', address='456 Wellness St', phone='555-0102', email='contact@wellness.com'),
            Company(name='Community Health Services', address='789 Community Blvd', phone='555-0103', email='hello@community.com')
        ]
        
        for company in companies:
            db.session.add(company)
        
        db.session.commit()
        
        # Create sample users
        users = [
            User(username='admin', email='admin@medcert.com', role='admin', company_id=1, is_active=True),
            User(username='nurse1', email='nurse1@medcert.com', role='nurse', company_id=1, is_active=True),
            User(username='nurse2', email='nurse2@medcert.com', role='nurse', company_id=2, is_active=True),
            User(username='viewer1', email='viewer1@medcert.com', role='viewer', company_id=3, is_active=True),
        ]
        
        # Set passwords
        for user in users:
            user.set_password('password123')  # Change in production
            db.session.add(user)
        
        db.session.commit()
        
        # Create sample residences
        residences = [
            Residence(name='Sunrise Manor', address='100 Sunrise Dr', company_id=1),
            Residence(name='Oak Grove Home', address='200 Oak St', company_id=2),
            Residence(name='Peaceful Gardens', address='300 Garden Way', company_id=3),
        ]
        
        for residence in residences:
            db.session.add(residence)
        
        db.session.commit()
        
        # Create sample HCPs
        hcps = [
            HCP(name='Alice Johnson', employee_id='EMP001', email='alice@medcare.com', company_id=1, hire_date=date(2023, 1, 15)),
            HCP(name='Bob Smith', employee_id='EMP002', email='bob@medcare.com', company_id=1, hire_date=date(2023, 3, 10)),
            HCP(name='Carol Davis', employee_id='EMP003', email='carol@wellness.com', company_id=2, hire_date=date(2023, 2, 20)),
            HCP(name='David Wilson', employee_id='EMP004', email='david@community.com', company_id=3, hire_date=date(2023, 4, 5)),
        ]
        
        for hcp in hcps:
            db.session.add(hcp)
        
        db.session.commit()
        
        # Create sample clients
        clients = [
            Client(initials='JD', client_code='CLI001', residence_id=1, is_primary=True),
            Client(initials='MS', client_code='CLI002', residence_id=1, is_primary=False),
            Client(initials='RB', client_code='CLI003', residence_id=2, is_primary=True),
            Client(initials='LK', client_code='CLI004', residence_id=3, is_primary=False),
        ]
        
        for client in clients:
            db.session.add(client)
        
        db.session.commit()
        
        # Create sample certifications
        certifications = [
            Certification(
                hcp_id=1, client_id=1, certification_type='medication_administration',
                issue_date=date.today() - timedelta(days=30),
                expiry_date=date.today() + timedelta(days=335),
                issued_by=1, notes='Initial certification'
            ),
            Certification(
                hcp_id=1, client_id=2, certification_type='insulin_administration',
                issue_date=date.today() - timedelta(days=15),
                expiry_date=date.today() + timedelta(days=350),
                issued_by=2, notes='Insulin administration training completed'
            ),
            Certification(
                hcp_id=2, client_id=1, certification_type='medication_administration',
                issue_date=date.today() - timedelta(days=60),
                expiry_date=date.today() + timedelta(days=20),  # Expiring soon
                issued_by=1, notes='Standard medication certification'
            ),
            Certification(
                hcp_id=3, client_id=3, certification_type='emergency_medication',
                issue_date=date.today() - timedelta(days=45),
                expiry_date=date.today() + timedelta(days=320),
                issued_by=1, notes='Emergency medication protocols'
            ),
        ]
        
        for cert in certifications:
            db.session.add(cert)
        
        db.session.commit()
        
        print("Database initialized successfully!")
        print("\nSample login credentials:")
        print("Admin: admin / password123")
        print("Nurse: nurse1 / password123")
        print("Viewer: viewer1 / password123")

if __name__ == '__main__':
    init_database()