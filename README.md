# Secure Authentication System

A secure user authentication system built with Flask and MySQL. It supports user registration, login with JWT authentication, profile management, and email-based OTP password reset.

## Features

User registration with bcrypt password hashing

Secure login with JWT tokens

Protected user profile endpoint

Update user profile details

Forgot-password flow with email OTP

OTP validation with a 5-minute expiry

Secure password reset

MySQL database integration

## Tech Stack

Python

Flask

MySQL

JWT

bcrypt

python-dotenv

## API Endpoints

Method

Endpoint

Description

POST

/register

Register a new user

POST

/login

Login and receive a JWT token

GET

/profile

Get authenticated user profile

PUT

/update-profile

Update authenticated user profile

POST

/forgot-password

Send password-reset OTP by email

POST

/verify-otp

Verify a password-reset OTP

POST

/reset-password

Reset password using an OTP

## Security Notes

Passwords are hashed with bcrypt before storage.

JWT tokens expire after one hour.

Password-reset OTPs expire after five minutes.

Sensitive credentials are stored in .env and excluded from GitHub.
