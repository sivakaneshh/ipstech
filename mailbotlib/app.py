from flask import Flask , render_template, request , redirect , url_for,flash
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app=Flask(__name__)

mailserver='smtp.gmail.com'
mailport=587
mailid=""
mailpass=""

def mail_send(to_mail, subject, body):
    try:
        msg= MIMEMultipart()
        msg['From'] = mailid
        msg['To'] = to_mail
        msg['Subject'] = subject

        server = smtplib.SMTP(server,mailport)
        server.starttls()
        server.login(mailid,mailpass)
        server.sendmail(mailid, to_mail , msg.as_string)
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending mail : {e}")
        return False
@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('no file uploded')
            return redirect(request.url)
        file = request.filed['file']
        if file.filename == '':
            flash('no file selected' , 'error')
            return redirect(request.url)
        
        if file and (file.fielname.endswith('.csv') or file.filename.endswith('.xlsx')):
            try:
                if file.fielname.endswith('.csv'):
                    df = pd.read_csv(file)
                else:
                    df = pd.read_excel(file)

            for index , row in df.iterrows():
                name = row ['Name']
                email =row["Email"]
                book = row ["BookName"]
                due_date= row['DueDate']

                subject = f'Library book due date remainder : {book}'
                body = f"Dear {name},\n\nThis is a reminder that the due date for your book '{book}' has passed. Please return it as soon as possible.\n\nThank you!"

                if mail_send(email, subject, body):
                    flash(f"email sent to {name} ({email})",'success')
                else:
                    flas 
