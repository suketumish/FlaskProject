# Flask Photo Storage App

## 📌 Overview
This is a **Flask-based web application** that allows users to **upload, store, retrieve, and delete images** in a **MySQL database**. The app supports common image formats (**JPG, PNG, JPEG, GIF**) and **automatically converts .HEIC images to JPG** for better compatibility.

---
## 🚀 Features
- ✅ Upload images with a **name** and store them in a MySQL database.
- ✅ Supports **JPG, PNG, JPEG, GIF, and HEIC** files.
- ✅ **Automatic conversion of HEIC to JPG**.
- ✅ Prevents duplicate **name or photo** uploads.
- ✅ **Search photos by name**.
- ✅ **View all uploaded photos**.
- ✅ **Delete photos by name** (removes from database and storage).

---
## 🛠️ Technologies Used
- **Flask** (Python web framework)
- **MySQL** (Database to store photos)
- **Pillow & pillow-heif** (Image processing and HEIC conversion)
- **HTML, CSS, JavaScript** (Frontend UI)
- **Werkzeug** (File security handling)

---
## 📂 Project Structure
```
📁 flask-photo-storage-app
│-- 📁 static/uploads        # Uploaded photos folder
│-- 📁 templates             # HTML templates
│   │-- index.html           # Upload & search page
│   │-- display.html         # Search result page
│   │-- all_photos.html      # All photos display page
│-- app.py                   # Flask app backend
│-- README.md                # Project documentation
│-- requirements.txt         # Required dependencies
```

---
## ⚙️ Installation & Setup
### 1️⃣ Clone the Repository
```sh
git clone https://github.com/yourusername/flask-photo-storage-app.git
cd flask-photo-storage-app
```

### 2️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 3️⃣ Configure MySQL Database
1. Open **MySQL** and create a database:
   ```sql
   CREATE DATABASE photodb;
   ```
2. Create the `photos` table:
   ```sql
   USE photodb;
   CREATE TABLE photos (
       id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(255) UNIQUE NOT NULL,
       photo VARCHAR(255) NOT NULL
   );
   ```
3. Update **MySQL credentials** in `app.py`:
   ```python
   app.config['MYSQL_USER'] = 'your_mysql_username'
   app.config['MYSQL_PASSWORD'] = 'your_mysql_password'
   ```

### 4️⃣ Run the Flask App
```sh
python app.py
```
- Open **http://127.0.0.1:5000/** in your browser.

---
## 📸 Usage Guide
### Upload a Photo
1. Enter a **name** and choose a **photo**.
2. Click **Upload**.
3. If successful, the image is stored in `static/uploads/` and MySQL.

### Search for a Photo
1. Enter a **name** in the search box.
2. Click **Search**.
3. The photo(s) with that name will be displayed.

### View All Photos
1. Navigate to `/all_photos`.
2. All uploaded photos are listed.

### Delete a Photo
1. Click **Delete** next to a photo.
2. The photo is removed from MySQL and storage.

---
## 🔥 Troubleshooting
### 1. MySQL Connection Issues
- Check if MySQL is running and the credentials are correct.
- Ensure the `photodb` database and `photos` table exist.

### 2. HEIC Files Not Converting
- Install `pillow-heif` if not installed:
  ```sh
  pip install pillow-heif
  ```
- Ensure **Pillow** is registered to handle HEIC:
  ```python
  from pillow_heif import register_heif_opener
  register_heif_opener()
  ```

---
## 📜 License
This project is open-source and free to use. Modify it as needed!

---
## 💡 Future Enhancements
- 📌 Add **user authentication**.
- 📌 Implement **image resizing** to save space.
- 📌 Support **drag & drop uploads**.
- 📌 Improve **UI with Bootstrap or Tailwind CSS**.

---
## 🤝 Contributing
- Fork the repository and submit a **pull request** with improvements.
- Report issues or suggest features in the **Issues** section.

---
## 🎯 Author
Created by **[Your Name]** 🚀

![saket21](https://github.com/user-attachments/assets/30fab554-0e7c-48f4-8bb8-43c5461cc9b8)
