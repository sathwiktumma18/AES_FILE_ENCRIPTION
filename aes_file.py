import tkinter as tk
from tkinter import messagebox, filedialog
from cryptography.fernet import Fernet
import os
import smtplib
import tempfile
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import webbrowser

# -------------------- UI Setup --------------------
root = tk.Tk()
root.title("AES File Encryptor/Decryptor")
root.geometry("500x500")
root.configure(bg="#1c1c1c")

title_label = tk.Label(root, text="File Encrypt & Decrypt", font=("Helvetica", 18, "bold"), bg="#1c1c1c", fg="#ff4d4d")
title_label.pack(pady=15)

# File path entry
filepath_entry = tk.Entry(root, width=50, font=("Arial", 10))
filepath_entry.pack(pady=5)

browse_btn = tk.Button(root, text="Browse", bg="#333", fg="white", font=("Arial", 10, "bold"),
                       command=lambda: filepath_entry.insert(0, filedialog.askopenfilename()))
browse_btn.pack(pady=5)

# Sender Email Entry
sender_email_entry = tk.Entry(root, width=50, font=("Arial", 10))
sender_email_entry.insert(0, "Sender Email (Gmail)")
sender_email_entry.pack(pady=5)

# Recipient Email Entry
receiver_email_entry = tk.Entry(root, width=50, font=("Arial", 10))
receiver_email_entry.insert(0, "Recipient Email (Gmail)")
receiver_email_entry.pack(pady=5)

# App Password Entry (hidden)
app_password_entry = tk.Entry(root, width=50, font=("Arial", 10), show="*")
app_password_entry.insert(0, "App Password")
app_password_entry.pack(pady=5)

# Key Entry
password_entry = tk.Entry(root, width=50, font=("Arial", 10))
password_entry.insert(0, "Enter decryption key here")
password_entry.pack(pady=10)

# -------------------- Encrypt Function --------------------
def encrypt_file():
    filepath = filepath_entry.get()
    sender_email = sender_email_entry.get()
    receiver_email = receiver_email_entry.get()
    smtp_password = app_password_entry.get()

    if '' in [filepath, sender_email, receiver_email, smtp_password] or not os.path.exists(filepath):
        messagebox.showerror("Error", "Please fill all fields correctly and select a valid file.")
        return

    key = Fernet.generate_key()
    fernet = Fernet(key)

    try:
        with open(filepath, 'rb') as file:
            data = file.read()
        encrypted_data = fernet.encrypt(data)
        with open(filepath, 'wb') as file:
            file.write(encrypted_data)
    except Exception as e:
        messagebox.showerror("Error", f"Encryption failed: {str(e)}")
        return

    subject = 'Encryption Key for File'
    message = f'The key for decrypting the file "{os.path.basename(filepath)}" is:\n\n{key.decode()}'

    try:
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, smtp_password)
        server.send_message(msg)
        server.quit()

        messagebox.showinfo("Success", "File encrypted and key sent via email.")
    except Exception as e:
        messagebox.showerror("Email Error", f"Failed to send email.\nReason: {str(e)}")

# -------------------- Decrypt Function --------------------
def decrypt_file():
    filepath = filepath_entry.get()
    key_text = password_entry.get()

    if filepath == '' or not os.path.exists(filepath):
        messagebox.showerror("Error", "Please select a valid file path.")
        return
    if key_text == '':
        messagebox.showerror("Error", "Please enter the encryption key.")
        return

    try:
        key = key_text.encode()
        fernet = Fernet(key)

        with open(filepath, 'rb') as file:
            encrypted_data = file.read()

        decrypted_data = fernet.decrypt(encrypted_data)

        with open(filepath, 'wb') as file:
            file.write(decrypted_data)

        messagebox.showinfo("Success", "File decrypted successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Decryption failed.\nReason: {str(e)}")

# -------------------- Project Info Function --------------------
import os
def open_project_info():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <title>Project Information</title>
      <style>
        body {
          font-family: 'Segoe UI', sans-serif;
          margin: 0;
          padding: 0;
          background: linear-gradient(to right, #1e3c72, #2a5298);
          color: #fff;
          animation: fadeIn 1s ease-in-out;
        }

        @keyframes fadeIn {
          from { opacity: 0; }
          to { opacity: 1; }
        }

        .container {
          padding: 30px;
          max-width: 900px;
          margin: auto;
          background-color: rgba(0, 0, 0, 0.6);
          border-radius: 15px;
          box-shadow: 0 0 15px rgba(0,0,0,0.5);
          animation: slideUp 0.7s ease-out;
        }

        @keyframes slideUp {
          from { transform: translateY(30px); opacity: 0; }
          to { transform: translateY(0); opacity: 1; }
        }

        h1 {
          text-align: center;
          font-size: 32px;
          margin-bottom: 20px;
          color: #00e6e6;
        }

        table {
          width: 100%;
          border-collapse: collapse;
          margin-top: 20px;
        }

        th, td {
          padding: 12px;
          border: 1px solid #ddd;
          text-align: left;
          background-color: rgba(255, 255, 255, 0.1);
        }

        th {
          background-color: #00b3b3;
          color: black;
        }

        .section-title {
          font-size: 24px;
          margin-top: 30px;
          color: #ffcc00;
        }

        .logo {
          float: right;
          height: 60px;
        }

        .footer {
          text-align: center;
          margin-top: 40px;
          font-size: 14px;
          color: #ccc;
        }

        .logo-animated {
          animation: pulse 2s infinite;
        }

        @keyframes pulse {
          0% { transform: scale(1); }
          50% { transform: scale(1.05); }
          100% { transform: scale(1); }
        }
      </style>
    </head>
    <body>
      <div class="container">
        <img src="https://i.ibb.co/3WmY0s7/supraja-logo.png" alt="Logo" class="logo logo-animated">
        <h1>Project Information</h1>

        <p>This project was developed by <strong>Anonymous</strong> as part of a <strong>Cyber Security Internship</strong>.
           It is designed to <strong>Secure the Organizations in Real World from Cyber Frauds performed by Hackers</strong>.</p>

        <table>
          <tr><th>Project Details</th><th>Value</th></tr>
          <tr><td>Project Name</td><td>File Encryption Using AES</td></tr>
          <tr><td>Project Description</td><td>Developing a tool FOR File Encryption and decryption using AES encryption and decryption standards</td></tr>
          <tr><td>Project Start Date</td><td>08-JULY-2025</td></tr>
          <tr><td>Project End Date</td><td>09-AUGUST-2025</td></tr>
          <tr><td>Project Status</td><td>Completed</td></tr>
        </table>

        <div class="section-title">Developer Details</div>
        <table>
          <tr><th>Name</th><th>Employee ID</th><th>Email</th></tr>
          <tr><td>GURAJA HEMANTH RAMA SURYA SAI</td><td>ST#IS#7763</td><td>ghramasuryasai@gmail.com</td></tr>
          tr><td>TUMMA SATHWIK</td><td>ST#IS#7744</td><td>sathwiktumma18@gmail.com</td></tr>
          tr><td>KAMATHAM UDAY KIRAN</td><td>ST#IS#7745</td><td>udaykirankamatham22@gmail.com</td></tr>
        </table>

        <div class="section-title">Company Details</div>
        <table>
          <tr><th>Company</th><th>Value</th></tr>
          <tr><td>Name</td><td>Supraja Technologies</td></tr>
          <tr><td>Email</td><td>contact@suprajatechnologies.com</td></tr>
        </table>

        <div class="footer">© 2024 Supraja Technologies | Cyber Security Internship Project</div>
      </div>
    </body>
    </html>
    """

    # Create a temporary file and open it in the browser
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".html") as f:
        f.write(html_content)
        webbrowser.open(f"file://{f.name}")




# Encrypt Button
encrypt_btn = tk.Button(root, text="Encrypt File", bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), command=encrypt_file)
encrypt_btn.pack(pady=10, ipadx=10, ipady=2)

# Decrypt Button
decrypt_btn = tk.Button(root, text="Decrypt File", bg="#f44336", fg="white", font=("Arial", 12, "bold"), command=decrypt_file)
decrypt_btn.pack(pady=5, ipadx=10, ipady=2)

# Project Info Button
info_btn = tk.Button(root, text="ℹ Project Info", bg="#2196F3", fg="white", font=("Arial", 10, "bold"), command=open_project_info)
info_btn.pack(pady=20)

root.mainloop()
