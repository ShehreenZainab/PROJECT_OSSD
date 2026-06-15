"""
 Authentication Module
Module: auth.py
Purpose: Handle all authentication logic, session storage, and role management
"""

from database import get_connection, close_connection
import hashlib
import secrets
from datetime import datetime

# Stores the currently logged-in user's information
current_user = {}


# ==============================================
# HELPER FUNCTIONS
# ==============================================

def hash_password(password):
    """Hashes a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain_password, hashed_password):
    """Verifies a plain password against a stored hash."""
    return hash_password(plain_password) == hashed_password


def generate_session_token():
    """Generates a unique session token for the logged-in user."""
    return secrets.token_hex(32)


def get_resident_by_email(email):
    """Retrieves resident information by email."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT resident_id, full_name, email, phone, room_number, block_name, is_active
            FROM Resident 
            WHERE email = ? AND is_active = 1
        """, (email,))
        row = cursor.fetchone()
        return dict(row) if row else None
    except Exception as e:
        print(f"[Auth Error] Failed to get resident: {e}")
        return None
    finally:
        close_connection(conn)


def get_admin_by_email(email):
    """Retrieves admin/staff information by email."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT staff_id, full_name, email, phone, role, is_available
            FROM Staff 
            WHERE email = ? AND role = 'Admin' AND is_available = 1
        """, (email,))
        row = cursor.fetchone()
        return dict(row) if row else None
    except Exception as e:
        print(f"[Auth Error] Failed to get admin: {e}")
        return None
    finally:
        close_connection(conn)


def get_staff_by_email(email):
    """Retrieves staff information by email (non-admin staff)."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT staff_id, full_name, email, phone, role, is_available
            FROM Staff 
            WHERE email = ? AND role != 'Admin' AND is_available = 1
        """, (email,))
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        close_connection(conn)


def verify_signup_credentials(email, password):
    """Verifies credentials from the SignUp table."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.signup_id, s.resident_id, s.username, s.password_hash, 
                   r.full_name, r.email, r.phone, r.room_number, r.block_name
            FROM SignUp s
            JOIN Resident r ON s.resident_id = r.resident_id
            WHERE r.email = ? AND r.is_active = 1
        """, (email,))
        row = cursor.fetchone()
        
        if row and verify_password(password, row['password_hash']):
            return {
                'resident_id': row['resident_id'],
                'full_name': row['full_name'],
                'email': row['email'],
                'phone': row['phone'],
                'room_number': row['room_number'],
                'block_name': row['block_name'],
                'username': row['username']
            }
        return None
    except Exception as e:
        print(f"[Auth Error] Failed to verify signup: {e}")
        return None
    finally:
        close_connection(conn)


def log_login_attempt(user_id, user_type, ip_address='127.0.0.1', session_token=None):
    """Records a successful login attempt in the Login table."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        if not session_token:
            session_token = generate_session_token()
        
        cursor.execute("""
            INSERT INTO Login (user_id, user_type, login_time, ip_address, session_token, is_active)
            VALUES (?, ?, ?, ?, ?, 1)
        """, (user_id, user_type, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ip_address, session_token))
        conn.commit()
        return True
    except Exception as e:
        print(f"[Auth Error] Failed to log login: {e}")
        return False
    finally:
        close_connection(conn)


# ==============================================
# MAIN AUTHENTICATION FUNCTIONS
# ==============================================

def login_user(email, password, ip_address='127.0.0.1'):
    """Authenticates a user by email and password."""
    global current_user
    
    logout_user()
    
    resident_data = verify_signup_credentials(email, password)
    if resident_data:
        log_login_attempt(resident_data['resident_id'], 'resident', ip_address)
        
        current_user = {
            "user_id": resident_data['resident_id'],
            "name": resident_data['full_name'],
            "email": resident_data['email'],
            "role": "resident",
            "resident_id": resident_data['resident_id'],
            "staff_id": None,
            "phone": resident_data['phone'],
            "room_number": resident_data['room_number'],
            "block_name": resident_data['block_name'],
            "login_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        return True
    
    admin_data = get_admin_by_email(email)
    if admin_data:
        default_admin_password = hash_password("admin123")
        if verify_password(password, default_admin_password):
            log_login_attempt(admin_data['staff_id'], 'admin', ip_address)
            
            current_user = {
                "user_id": admin_data['staff_id'],
                "name": admin_data['full_name'],
                "email": admin_data['email'],
                "role": "admin",
                "resident_id": None,
                "staff_id": admin_data['staff_id'],
                "phone": admin_data['phone'],
                "staff_role": admin_data['role'],
                "login_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            return True
    
    staff_data = get_staff_by_email(email)
    if staff_data:
        default_staff_password = hash_password("staff123")
        if verify_password(password, default_staff_password):
            log_login_attempt(staff_data['staff_id'], 'staff', ip_address)
            
            current_user = {
                "user_id": staff_data['staff_id'],
                "name": staff_data['full_name'],
                "email": staff_data['email'],
                "role": "staff",
                "resident_id": None,
                "staff_id": staff_data['staff_id'],
                "phone": staff_data['phone'],
                "staff_role": staff_data['role'],
                "login_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            return True
    
    return False


def login_resident_direct(resident_id, ip_address='127.0.0.1'):
    """Direct login for a resident (useful for testing or admin impersonation)."""
    global current_user
    
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT resident_id, full_name, email, phone, room_number, block_name
            FROM Resident 
            WHERE resident_id = ? AND is_active = 1
        """, (resident_id,))
        row = cursor.fetchone()
        
        if row:
            log_login_attempt(resident_id, 'resident', ip_address)
            
            current_user = {
                "user_id": row['resident_id'],
                "name": row['full_name'],
                "email": row['email'],
                "role": "resident",
                "resident_id": row['resident_id'],
                "staff_id": None,
                "phone": row['phone'],
                "room_number": row['room_number'],
                "block_name": row['block_name'],
                "login_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            return True
        return False
    except Exception as e:
        print(f"[Auth Error] Direct login failed: {e}")
        return False
    finally:
        close_connection(conn)


def logout_user():
    """Clears the current_user dictionary and ends the session."""
    global current_user
    current_user = {}


def get_current_user():
    """Returns the current logged-in user's information."""
    return current_user


def is_logged_in():
    """Checks if a user is currently logged in."""
    return len(current_user) > 0


def is_admin():
    """Checks if the current logged-in user is an admin."""
    return current_user.get("role") == "admin"


def is_resident():
    """Checks if the current logged-in user is a resident."""
    return current_user.get("role") == "resident"


def is_staff():
    """Checks if the current logged-in user is a staff member."""
    return current_user.get("role") == "staff"


def has_role(required_role):
    """Checks if the current user has a specific role."""
    return current_user.get("role") == required_role


def get_user_id():
    """Returns the current user's primary ID (resident_id or staff_id)."""
    if is_resident():
        return current_user.get("resident_id")
    elif is_admin() or is_staff():
        return current_user.get("staff_id")
    return None


def get_user_display_name():
    """Returns a formatted display name for the current user."""
    if not is_logged_in():
        return "Guest"
    
    name = current_user.get("name", "Unknown")
    role = current_user.get("role", "user").title()
    
    if is_resident():
        room = current_user.get("room_number", "N/A")
        block = current_user.get("block_name", "N/A")
        return f"{name} ({role} - {block}{room})"
    elif is_staff():
        staff_role = current_user.get("staff_role", "Staff")
        return f"{name} ({staff_role})"
    else:
        return f"{name} ({role})"


# ==============================================
# REGISTRATION FUNCTIONS
# ==============================================

def register_user(resident_id, username, password, security_question=None, security_answer=None):
    """Registers a new user in the SignUp table (creates login credentials for existing resident)."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        
        cursor.execute("SELECT resident_id FROM Resident WHERE resident_id = ?", (resident_id,))
        if not cursor.fetchone():
            print(f"[Auth Error] Resident ID {resident_id} not found")
            return False
        
        cursor.execute("SELECT signup_id FROM SignUp WHERE username = ?", (username,))
        if cursor.fetchone():
            print(f"[Auth Error] Username '{username}' already exists")
            return False
        
        password_hash = hash_password(password)
        cursor.execute("""
            INSERT INTO SignUp (resident_id, username, password_hash, security_question, security_answer)
            VALUES (?, ?, ?, ?, ?)
        """, (resident_id, username, password_hash, security_question, security_answer))
        
        conn.commit()
        return True
        
    except Exception as e:
        print(f"[Auth Error] Registration failed: {e}")
        return False
    finally:
        close_connection(conn)


def change_password(user_id, user_type, old_password, new_password):
    """Changes a user's password."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        
        if user_type == 'resident':
            cursor.execute("""
                SELECT password_hash FROM SignUp WHERE resident_id = ?
            """, (user_id,))
        else:
            print("[Auth Error] Staff password change not implemented yet")
            return False
        
        row = cursor.fetchone()
        if row and verify_password(old_password, row['password_hash']):
            new_hash = hash_password(new_password)
            if user_type == 'resident':
                cursor.execute("""
                    UPDATE SignUp SET password_hash = ? WHERE resident_id = ?
                """, (new_hash, user_id))
            conn.commit()
            return True
        
        return False
    except Exception as e:
        print(f"[Auth Error] Password change failed: {e}")
        return False
    finally:
        close_connection(conn)


# ==============================================
# SESSION MANAGEMENT
# ==============================================

def validate_session(session_token):
    """Validates if a session token is still active."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT user_id, user_type, login_time
            FROM Login
            WHERE session_token = ? AND is_active = 1
            AND datetime(login_time) > datetime('now', '-1 day')
        """, (session_token,))
        row = cursor.fetchone()
        
        if row:
            return {
                'user_id': row['user_id'],
                'user_type': row['user_type'],
                'login_time': row['login_time']
            }
        return None
    except Exception as e:
        print(f"[Auth Error] Session validation failed: {e}")
        return None
    finally:
        close_connection(conn)


def end_all_sessions(user_id, user_type):
    """Ends all active sessions for a user (e.g., on password change)."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Login SET is_active = 0
            WHERE user_id = ? AND user_type = ? AND is_active = 1
        """, (user_id, user_type))
        conn.commit()
        return True
    except Exception as e:
        print(f"[Auth Error] Failed to end sessions: {e}")
        return False
    finally:
        close_connection(conn)

