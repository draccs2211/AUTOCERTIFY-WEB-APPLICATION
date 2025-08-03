# 📨 AUTOCERTIFY – Certificate Sender Web App (Flask)

A full-featured Flask web application to **generate**, **preview**, and **send customized certificates via email**. Ideal for college events, internships, hackathons, and workshop organizers.

---

### 📺 Demo Video

🎥 Watch here: [https://youtu.be/yg7hCHejFxU](https://youtu.be/yg7hCHejFxU?si=0dmPS6lUjANWVFhr)

---

### 🚀 Features

- Upload and use your **own certificate templates**
- Live **Canva-style preview** with editable fields (name, org, mentor, date, etc.)
- Send to single recipient or via **bulk Excel upload**
- **Download certificate preview**
- Email sending with **Gmail + yagmail**
- Sent history stored in **Excel**
- Clean, user-friendly UI (HTML + CSS)

---

### 🖼️ Certificate Preview

> Live preview on template before sending  
> Option to download certificate as image

---
├── app.py # Flask backend
├── requirements.txt # Python dependencies
├── sent_history.xlsx # Logs of sent certificates
├── static/
│ ├── certificate_templates/ # Uploaded templates
│ └── *.png # Generated previews
├── templates/
│ ├── index.html # Main certificate sender UI
│ └── history.html # Sent history viewer
└── temp_uploaded.xlsx # Last Excel upload

yaml
Copy
Edit

---

### 📥 How to Run Locally

#### 1. Clone the Repository
```bash
git clone https://github.com/draccs2211/AUTOCERTIFY-WEB-APPLICATION.git
cd AUTOCERTIFY-WEB-APPLICATION
2. Create a Virtual Environment (Recommended)
bash
Copy
Edit
python -m venv venv
venv\Scripts\activate   # On Windows
# OR
source venv/bin/activate  # On macOS/Linux
3. Install Requirements
bash
Copy
Edit
pip install -r requirements.txt
4. Run the Flask App
bash
Copy
Edit
python app.py
Open your browser and visit:
http://localhost:5000

🛠️ Built With
Backend: Flask

Frontend: HTML, CSS, Jinja2

Email Engine: Yagmail (SMTP)

Image Generation: Pillow (PIL)

Excel Support: OpenPyXL

📧 Gmail Setup
Use your Gmail ID and App Password:

python
Copy
Edit
yag = yagmail.SMTP(user="your-email@gmail.com", password="your-app-password")
Tip: Turn on 2FA and generate an App Password from Google settings.

💡 Future Plans
Drag-and-drop certificate designer

Authentication (Admin Login)

QR code or watermark support

Email delivery reports
🔗 Author & Contact
Divyansh Maurya
👨‍🎓 B.Tech CSE (AI) | University of Lucknow
## 🔗 Author

👨‍💻 [Divyansh Maurya on LinkedIn](https://www.linkedin.com/in/divyansh-maurya-42a25735b)

![Frontend Preview](https://github.com/user-attachments/assets/ff18d40c-2365-4037-af27-18099c90d340)
