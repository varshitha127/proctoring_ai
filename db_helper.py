import mysql.connector
from mysql.connector import pooling
import logging
from typing import Optional, Tuple, List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "quizo",
    "pool_name": "quizo_pool",
    "pool_size": 5
}

# Create connection pool
try:
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(**DB_CONFIG)
    logger.info("Database connection pool created successfully")
except mysql.connector.Error as err:
    logger.error(f"Error creating connection pool: {err}")
    raise

def get_connection():
    """Get a connection from the pool"""
    try:
        return connection_pool.get_connection()
    except mysql.connector.Error as err:
        logger.error(f"Error getting connection from pool: {err}")
        raise

def insert_signup(email: str, username: str, password: str) -> Tuple[int, str]:
    """
    Insert a new user signup record
    Returns: (status_code, message)
    """
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            
            # Check if email or username already exists
            check_query = "SELECT email, username FROM quizo.sign_up WHERE email = %s OR username = %s"
            cursor.execute(check_query, (email, username))
            existing = cursor.fetchone()
            
            if existing:
                if existing[0] == email:
                    return -1, "Email already registered"
                else:
                    return -1, "Username already taken"
            
            # Insert new user
            insert_query = "INSERT INTO quizo.sign_up (email, username, password) VALUES (%s, %s, %s)"
            cursor.execute(insert_query, (email, username, password))
            connection.commit()
            
            logger.info(f"Successfully registered user: {username}")
            return 1, "Registration successful"

    except mysql.connector.Error as err:
        logger.error(f"Database error during signup: {err}")
        return -1, f"Database error: {str(err)}"
    except Exception as e:
        logger.error(f"Unexpected error during signup: {e}")
        return -1, f"Unexpected error: {str(e)}"

def search_login_credentials(email: str, password: str) -> Tuple[bool, Dict[str, Any]]:
    """
    Search for login credentials
    Returns: (success, response_data)
    """
    try:
        with get_connection() as connection:
            cursor = connection.cursor(dictionary=True)
            
            query = """
                SELECT email, username 
                FROM quizo.sign_up 
                WHERE email = %s AND password = %s
            """
            cursor.execute(query, (email, password))
            user = cursor.fetchone()
            
            if user:
                logger.info(f"Successful login for user: {user['username']}")
                return True, {
                    "success": True,
                    "message": "Login successful",
                    "user": {
                        "email": user['email'],
                        "username": user['username']
                    }
                }
            else:
                logger.warning(f"Failed login attempt for email: {email}")
                return False, {
                    "success": False,
                    "message": "Invalid email or password"
                }

    except mysql.connector.Error as err:
        logger.error(f"Database error during login: {err}")
        return False, {
            "success": False,
            "message": f"Database error: {str(err)}"
        }
    except Exception as e:
        logger.error(f"Unexpected error during login: {e}")
        return False, {
            "success": False,
            "message": f"Unexpected error: {str(e)}"
        }

def get_all_users() -> List[Dict[str, Any]]:
    """Get all user details"""
    try:
        with get_connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT email, username FROM quizo.sign_up")
            users = cursor.fetchall()
            return users
    except mysql.connector.Error as err:
        logger.error(f"Error fetching users: {err}")
        return []

if __name__ == "__main__":
    # Test database connection
    try:
        with get_connection() as conn:
            logger.info("Database connection test successful")
    except Exception as e:
        logger.error(f"Database connection test failed: {e}")
    # print(get_all_details())
    # print(search_login_credentials('kumar1166@gmail.com', 'Kris@2223'))
    # insert_signup('kumar1166@gmail.com', 'kris6', 'Kris@2223')
    # print(get_all_details())