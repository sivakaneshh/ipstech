from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)

mailserver = 'smtp.gmail.com'
mailport = 587
mailid = ""
mailpass = ""

def mail_send(to_mail, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = mailid
        msg['To'] = to_mail
        msg['Subject'] = subject

        server = smtplib.SMTP(mailserver, mailport)
        server.starttls()
        server.login(mailid, mailpass)
        server.sendmail(mailid, to_mail, msg.as_string())  # Fixed the method call
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending mail: {e}")
        return False

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file uploaded')
            return redirect(request.url)
        file = request.files['file']  # Fixed typo here
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        if file and (file.filename.endswith('.csv') or file.filename.endswith('.xlsx')):
            try:
                if file.filename.endswith('.csv'):
                    df = pd.read_csv(file)
                else:
                    df = pd.read_excel(file)

                for index, row in df.iterrows():
                    name = row['Name']
                    email = row["Email"]
                    book = row["BookName"]
                    due_date = row['DueDate']

                    subject = f'Library book due date reminder: {book}'
                    body = f"Dear {name},\n\nThis is a reminder that the due date for your book '{book}' has passed. Please return it as soon as possible.\n\nThank you!"

                    if mail_send(email, subject, body):
                        flash(f"Email sent to {name} ({email})", 'success')
                    else:
                        flash(f"Failed to send mail", 'error')
            except Exception as e:
                flash(f"Error processing file: {e}", 'error')
        else:
            flash("Invalid file type, please upload CSV or Excel.")
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
