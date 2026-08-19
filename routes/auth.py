
from flask import Flask, request, jsonify
from db import db, cursor
from utils.password_utils import hash_password, verify_password
from utils.jwt_utils import generate_token, verify_token
from utils.otp_utils import generate_otp
import jwt
from flask import Blueprint
from utils.email_utils import send_otp
from datetime import datetime, timedelta

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    name = data["name"]
    email = data["email"]
    password = data["password"]

    # Check if email already exists
    cursor.execute(
        "SELECT * FROM users WHERE email=%s",
        (email,)
    )

    existing_user = cursor.fetchone()

    if existing_user:
        return {"message": "Email already registered"}, 409

    # Hash password
    hashed_password = hash_password(password)

    # Insert new user
    query = """
    INSERT INTO users(name,email,password)
    VALUES(%s,%s,%s)
    """

    values = (
        name,
        email,
        hashed_password
    )

    cursor.execute(query, values)
    db.commit()

    return {"message": "User Registered Successfully"}

@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data["email"]
    password = data["password"]

    query = "SELECT * FROM users WHERE email=%s"

    cursor.execute(query, (email,))

    user = cursor.fetchone()

    if user is None:
        return {"message": "User not found"}, 404

    stored_password = user[3]

    if verify_password(password, stored_password):

        token = generate_token(email)

        return {
    "message":"Login Successful",
    "token": token
}

    else:
        return {"message": "Invalid Password"}, 401
    
@auth_bp.route("/profile", methods=["GET"])

def profile():

    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return jsonify({"message": "Token Missing"}), 401

    try:

        token = auth_header.split(" ")[1]

        decoded = verify_token(token)

        email = decoded["email"]

        cursor.execute(
            "SELECT name,email FROM users WHERE email=%s",
            (email,)
        )

        user = cursor.fetchone()

        return jsonify({
            "name": user[0],
            "email": user[1]
        })

    except jwt.ExpiredSignatureError:
        return jsonify({"message":"Token Expired"}),401

    except jwt.InvalidTokenError:
        return jsonify({"message":"Invalid Token"}),401

@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():

    data = request.get_json()

    email = data["email"]

    # Check if user exists
    cursor.execute(
        "SELECT * FROM users WHERE email=%s",
        (email,)
    )

    user = cursor.fetchone()

    if user is None:
        return {"message": "User not found"}, 404

    # Generate OTP
    otp = generate_otp()

    # Remove old OTP if it exists
    cursor.execute(
    "DELETE FROM otp_table WHERE email=%s",
    (email,)
)

    # Store OTP
    cursor.execute(
        "INSERT INTO otp_table(email,otp) VALUES(%s,%s)",
        (email,otp)
    )

    db.commit()

    send_otp(email, otp)

    return {

"message":"OTP sent successfully"

} 

@auth_bp.route("/verify-otp", methods=["POST"])
def verify_otp():

    data = request.get_json()

    email = data["email"]
    otp = data["otp"]

    cursor.execute(
        """
        SELECT created_at
        FROM otp_table
        WHERE email=%s AND otp=%s
        """,
        (email, otp)
    )

    result = cursor.fetchone()

    if result is None:
        return {
            "message": "Invalid OTP"
        }, 401

    created_time = result[0]

    if datetime.now() - created_time > timedelta(minutes=5):

        cursor.execute(
            "DELETE FROM otp_table WHERE email=%s",
            (email,)
        )

        db.commit()

        return {
            "message": "OTP Expired"
        }, 401

    # OTP is valid → delete it so it can't be reused
    cursor.execute(
        "DELETE FROM otp_table WHERE email=%s",
        (email,)
    )

    db.commit()

    return {
        "message": "OTP Verified"
    }

@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():

    data = request.get_json()

    email = data["email"]
    otp = data["otp"]
    new_password = data["new_password"]

    # Verify OTP
    cursor.execute(
        """
        SELECT created_at
        FROM otp_table
        WHERE email=%s AND otp=%s
        """,
        (email, otp)
    )

    result = cursor.fetchone()

    if result is None:
        return {
            "message": "Invalid OTP"
        }, 401

    created_time = result[0]

    # Check OTP expiry
    if datetime.now() - created_time > timedelta(minutes=5):

        cursor.execute(
            "DELETE FROM otp_table WHERE email=%s",
            (email,)
        )

        db.commit()

        return {
            "message": "OTP Expired"
        }, 401

    # Hash new password
    hashed_password = hash_password(new_password)

    # Update password
    cursor.execute(
        """
        UPDATE users
        SET password=%s
        WHERE email=%s
        """,
        (hashed_password, email)
    )

    # Delete OTP after successful reset
    cursor.execute(
        "DELETE FROM otp_table WHERE email=%s",
        (email,)
    )

    db.commit()

    return {
        "message": "Password Reset Successfully"
    }

@auth_bp.route("/update-profile", methods=["PUT"])
def update_profile():

    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return {"message": "Token Missing"}, 401

    token = auth_header.split(" ")[1]

    try:

        decoded = verify_token(token)

        email = decoded["email"]

        data = request.get_json()

        name = data["name"]

        cursor.execute(
            """
            UPDATE users
            SET name=%s
            WHERE email=%s
            """,
            (name, email)
        )

        db.commit()

        return {
            "message": "Profile Updated Successfully"
        }

    except jwt.InvalidTokenError:

        return {
            "message": "Invalid Token"
        }, 401
