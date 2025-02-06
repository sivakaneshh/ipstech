from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import secrets
import os

# Generate a secret key for session management
secret_key = secrets.token_hex(16)

app = Flask(__name__)
app.secret_key = secret_key

# Gmail SMTP Configuration
MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 587  # Correct port for TLS
MAIL_ID = "sksivakanesh12@gmail.com"  # Replace with your Gmail
MAIL_PASS = "qsnx pnox hveu chia"  # Replace with your App Password

def mail_send(to_email, subject, body):
    """Send an email using Gmail's SMTP server."""
    try:
        msg = MIMEMultipart()
        msg['From'] = MAIL_ID
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Connect to Gmail SMTP Server
        server = smtplib.SMTP(MAIL_SERVER, MAIL_PORT)
        server.starttls()  # Secure the connection
        server.login(MAIL_ID, MAIL_PASS)
        server.sendmail(MAIL_ID, to_email, msg.as_string())
        server.quit()

        return True
    except Exception as e:
        print(f"Error sending mail to {to_email}: {e}")
        return False

@app.route('/', methods=['GET', 'POST'])
def index():
    """Home route to upload and process the Excel file."""
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file uploaded.', 'error')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No file selected. Please upload an Excel or CSV file.', 'error')
            return redirect(request.url)
        
        if file and (file.filename.endswith('.csv') or file.filename.endswith('.xlsx')):
            try:
                # Read Excel or CSV file
                if file.filename.endswith('.csv'):
                    df = pd.read_csv(file)
                else:
                    df = pd.read_excel(file)

                # Ensure required columns exist
                required_columns = {'Name', 'Email', 'BookName', 'DueDate'}
                if not required_columns.issubset(df.columns):
                    flash("Invalid file format! Ensure the file has columns: Name, Email, BookName, DueDate.", 'error')
                    return redirect(request.url)

                # Process each student
                for index, row in df.iterrows():
                    name = row['Name']
                    email = row["Email"]
                    book = row["BookName"]
                    due_date = row['DueDate']

                    # Construct email subject and body
                    subject = f'Library Book Due Date Reminder: {book}'
                    body = f"""
                    Dear {name},

                    This is a reminder that the due date for your book '{book}' is {due_date}. 
                    Please ensure it is returned on time to avoid any penalties.

                    Thank you!
                    Library Management Team
                    """

                    # Send email
                    if mail_send(email, subject, body):
                        flash(f"Email sent to {name} ({email})", 'success')
                    else:
                        flash(f"Failed to send email to {name} ({email})", 'error')

            except Exception as e:
                flash(f"Error processing file: {e}", 'error')
        else:
            flash("Invalid file type. Please upload a CSV or Excel file.", 'error')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
