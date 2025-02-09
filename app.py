from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import os
from werkzeug.utils import secure_filename
from pillow_heif import register_heif_opener
from PIL import Image

app = Flask(__name__)

# MySQL Config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Change this if needed
app.config['MYSQL_PASSWORD'] = ''  # Change this if needed
app.config['MYSQL_DB'] = 'photodb'

# File Upload Config
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'your_secret_key'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'heic'}  # Added .heic support

mysql = MySQL(app)

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Register HEIF format for Pillow
register_heif_opener()

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_heic_to_jpg(heic_path):
    """Convert .heic to .jpg and return new filename."""
    img = Image.open(heic_path)
    new_filename = os.path.splitext(heic_path)[0] + ".jpg"
    img.convert("RGB").save(new_filename, "JPEG")
    os.remove(heic_path)  # Remove original .heic file
    return os.path.basename(new_filename)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        photo = request.files['photo']
        
        if name and photo and allowed_file(photo.filename):
            filename = secure_filename(photo.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            # Check for duplicate name or photo
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM photos WHERE name = %s OR photo = %s", (name, filename))
            existing = cur.fetchone()

            if existing:
                flash('Name or Photo already exists!', 'danger')
            else:
                # Save file first
                photo.save(filepath)

                # Convert HEIC to JPG if necessary
                if filename.lower().endswith(".heic"):
                    filename = convert_heic_to_jpg(filepath)
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

                # Insert into MySQL
                cur.execute("INSERT INTO photos (name, photo) VALUES (%s, %s)", (name, filename))
                mysql.connection.commit()
                flash('Photo uploaded successfully!', 'success')

            cur.close()
            return redirect(url_for('index'))
        else:
            flash('Invalid file type!', 'danger')

    return render_template('index.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    photos = None
    name = None
    if request.method == 'POST':
        name = request.form['name']
        cur = mysql.connection.cursor()
        cur.execute("SELECT photo FROM photos WHERE name = %s", (name,))
        photos = cur.fetchall()
        cur.close()

    return render_template('display.html', photos=photos, name=name)


@app.route('/all_photos')
def all_photos():
    """Display all photos stored in the database."""
    cur = mysql.connection.cursor()
    cur.execute("SELECT name, photo FROM photos")
    photos = cur.fetchall()
    cur.close()
    return render_template('all_photos.html', photos=photos)


@app.route('/delete/<name>', methods=['POST'])
def delete(name):
    """Delete photos by name from the database and storage."""
    cur = mysql.connection.cursor()
    cur.execute("SELECT photo FROM photos WHERE name = %s", (name,))
    photos = cur.fetchall()

    if photos:
        # Delete each photo file from storage
        for photo in photos:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], photo[0])
            if os.path.exists(filepath):
                os.remove(filepath)

        # Delete from MySQL
        cur.execute("DELETE FROM photos WHERE name = %s", (name,))
        mysql.connection.commit()
        flash(f'Photos with name "{name}" deleted successfully!', 'success')
    else:
        flash(f'No photos found for "{name}".', 'danger')

    cur.close()
    return redirect(url_for('all_photos'))


if __name__ == '__main__':
    app.run(debug=True)
