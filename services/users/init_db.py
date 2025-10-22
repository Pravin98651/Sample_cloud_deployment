import os
import sys
from src import create_app, db
from src.api.users.models import User

def init_db():
    app = create_app()
    with app.app_context():
        try:
            print("Creating database tables...")
            db.create_all()
            print("Database tables created successfully!")
            
            # Create a test user if it doesn't exist
            if not User.query.filter_by(email='test@example.com').first():
                user = User(
                    username='testuser',
                    email='test@example.com',
                    password='testpass123'  # In a real app, this should be hashed
                )
                db.session.add(user)
                db.session.commit()
                print("Test user created!")
                
        except Exception as e:
            print(f"Error: {e}")
            return False
    return True

if __name__ == '__main__':
    print("Initializing database...")
    if init_db():
        print("Database initialized successfully!")
    else:
        print("Failed to initialize database.")
        sys.exit(1)
