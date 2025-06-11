# Med-Trained Staff Tracking App
A Flask application to track medication-trained healthcare professional certifications.

## Getting Started

1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize the database**

   ```bash
   python -c "from app import db; db.create_all()"
   ```

3. **Create a user** (optional example)

   ```bash
   python - <<'EOF'
   from app import db
   from app.models import User
   u = User(username='admin')
   u.set_password('password')
   db.session.add(u)
   db.session.commit()
   EOF
   ```

4. **Run the application**

   ```bash
   python wsgi.py
   ```

Navigate to `http://localhost:5000` and log in with the credentials you created.
