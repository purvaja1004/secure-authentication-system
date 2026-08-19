import smtplib

from email.mime.text import MIMEText

from config import EMAIL_USER, EMAIL_PASSWORD


def send_otp(email, otp):

    subject = "Password Reset OTP"

    body = f"""

Hello,

Your OTP is:

{otp}

It is valid for 5 minutes.

"""

    msg = MIMEText(body)

    msg["Subject"] = subject

    msg["From"] = EMAIL_USER

    msg["To"] = email

    server = smtplib.SMTP("smtp.gmail.com",587)

    server.starttls()

    server.login(
        EMAIL_USER,
        EMAIL_PASSWORD
    )

    server.sendmail(
        EMAIL_USER,
        email,
        msg.as_string()
    )

    server.quit()