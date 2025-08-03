from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import yagmail, os, re
import datetime

app = Flask(__name__)
app.secret_key = 'supersecret'

TEMPLATES_DIR =  "static/certificate_templates"
FONTS_DIR = "fonts"
OUTPUT_DIR = "generated_certificates"
HISTORY_PATH = "sent_history.xlsx"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(TEMPLATES_DIR, exist_ok=True)
os.makedirs(FONTS_DIR, exist_ok=True)

def get_available_templates():
    return [f for f in os.listdir(TEMPLATES_DIR) if f.lower().endswith(('.jpg', '.png'))]

def get_available_fonts():
    return [f for f in os.listdir(FONTS_DIR) if f.lower().endswith('.ttf')]

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

@app.route("/", methods=["GET", "POST"])
def index():
    template_list = get_available_templates()
    font_list = get_available_fonts()
    preview_path = None

    if request.method == "POST":
        sender_email = request.form["sender_email"].strip()
        sender_pass = request.form["sender_pass"].strip()
        selected_template = request.form.get("selected_template")
        selected_font = request.form.get("selected_font", "arial.ttf")
        excel_file = request.files["excel_file"]
        manual_name = request.form.get("manual_name", "").strip()
        manual_email = request.form.get("manual_email", "").strip()
        preview_only = request.form.get("preview") == "true"

        if not sender_email or not sender_pass:
            flash("Sender email and app password are required.")
            return redirect(url_for("index"))

        if not selected_template:
            flash("Please select a certificate template.")
            return redirect(url_for("index"))

        cert_template_path = os.path.join(TEMPLATES_DIR, selected_template)
        font_path = os.path.join(FONTS_DIR, selected_font)

        recipients = []

        if excel_file and excel_file.filename:
            try:
                excel_path = "temp_uploaded.xlsx"
                excel_file.save(excel_path)
                df = pd.read_excel(excel_path)
                if "NAME" not in df.columns or "GMAIL" not in df.columns:
                    flash("Excel must contain 'NAME' and 'GMAIL' columns.")
                    return redirect(url_for("index"))
                recipients = df[["NAME", "GMAIL"]].dropna().values.tolist()
            except:
                flash("Failed to read Excel file.")
                return redirect(url_for("index"))
        elif manual_name and manual_email:
            recipients = [[manual_name, manual_email]]
        else:
            flash("Either upload an Excel or enter name and Gmail manually.")
            return redirect(url_for("index"))

        history_rows = []

        for name, email in recipients:
            name = name.upper()
            email = email.strip()

            if not is_valid_email(email):
                flash(f"Invalid email format: {email}")
                continue

            try:
                image = Image.open(cert_template_path).convert("RGB")
                draw = ImageDraw.Draw(image)
                font = ImageFont.truetype(font_path, 60)
            except Exception as e:
                flash(f"Font or template error: {e}")
                return redirect(url_for("index"))

            bbox = draw.textbbox((0, 0), name, font=font)
            text_width = bbox[2] - bbox[0]
            position = ((image.width - text_width) // 2, 600)
            draw.text(position, name, fill="black", font=font)

            safe_name = re.sub(r'[^a-zA-Z0-9]', '_', name)
            output_path = os.path.join(OUTPUT_DIR, f"{safe_name}.pdf")
            image.save(output_path, "PDF")

            if preview_only:
                preview_image_path = os.path.join(OUTPUT_DIR, f"{safe_name}.png")
                image.save(preview_image_path)
                preview_path = preview_image_path.replace("\\", "/")
                break

            try:
                yag = yagmail.SMTP(user=sender_email, password=sender_pass)
                subject = "Your Certificate"
                body = f"Dear {name},\n\nPlease find your certificate attached.\n\nRegards."
                yag.send(to=email, subject=subject, contents=body, attachments=output_path)
                
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                history_rows.append([name, email, timestamp])

            except Exception as e:
                flash(f"Failed to send to {email}: {e}")

        if not preview_only:
            if os.path.exists(HISTORY_PATH):
                existing = pd.read_excel(HISTORY_PATH)
                new_history = pd.concat([existing, pd.DataFrame(history_rows, columns=["NAME", "GMAIL", "DATETIME"])])

            else:
                new_history = pd.DataFrame(history_rows, columns=["NAME", "GMAIL", "DATETIME"])

            new_history.to_excel(HISTORY_PATH, index=False)
            flash(f"Successfully sent {len(history_rows)} certificate(s).")

        return render_template("index.html", preview_path=preview_path, template_list=template_list, font_list=font_list)

    return render_template("index.html", preview_path=None, template_list=template_list, font_list=font_list)

@app.route("/upload_template", methods=["POST"])
def upload_template():
    file = request.files.get("new_template")
    if not file:
        flash("No file selected.")
        return redirect(url_for("index"))

    if not file.filename.lower().endswith((".jpg", ".png")):
        flash("Only JPG or PNG files are allowed.")
        return redirect(url_for("index"))

    safe_filename = re.sub(r'[^a-zA-Z0-9_.-]', '_', file.filename)
    save_path = os.path.join(TEMPLATES_DIR, safe_filename)
    file.save(save_path)
    flash(f"Template '{safe_filename}' uploaded successfully.")
    return redirect(url_for("index"))

@app.route("/download_preview")
def download_preview():
    path = request.args.get("path")
    if path and os.path.exists(path):
        return send_file(path, as_attachment=True)
    flash("No preview available.")
    return redirect(url_for("index"))

@app.route("/history")
def history():
    try:
        df = pd.read_excel(HISTORY_PATH)
        records = df.to_dict(orient="records")
    except:
        records = []
    return render_template("history.html", records=records)
@app.route("/delete_history", methods=["POST"])
def delete_history():
    if os.path.exists(HISTORY_PATH):
        os.remove(HISTORY_PATH)
        flash("History deleted successfully.")
    else:
        flash("No history file found.")
    return redirect(url_for("history"))


if __name__ == "__main__":
    app.run(debug=True)
