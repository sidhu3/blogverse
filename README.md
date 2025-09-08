# 📝 Blog Application with Sentiment Analysis & Summarization

A Flask-based Blog Application that allows users to create, edit, search, and manage blog posts with built-in **sentiment analysis** and **text summarization** features.  
The project also integrates authentication, data export, and visualization.

---

## 🚀 Features
- 🔑 User Authentication (Signup, Login, Logout)
- ✍️ Add, Edit, Delete Blog Posts
- 🧠 Sentiment Analysis of blog content (Positive, Negative, Neutral)
- 📑 Automatic Text Summarization (using Sumy LSA)
- 🔍 Search Functionality with Pagination
- 📊 Data Export to CSV for further analysis in R
- 📈 Visualization plots (Sentiment Distribution, Clustering)
- ⏰ Blog post publication date tracking
- Flash messages for better UX

---

## 🛠 Tech Stack
- **Backend**: Flask, Flask-Login, Flask-SQLAlchemy, Flask-Migrate  
- **Frontend**: HTML, Bootstrap (templates)  
- **Database**: SQLite (default)  
- **Machine Learning / NLP**:  
  - [TextBlob](https://textblob.readthedocs.io/en/dev/) for Sentiment Analysis  
  - [Sumy](https://pypi.org/project/sumy/) for Text Summarization  
- **Data Export**: Pandas  
- **Visualization**: Matplotlib (plots saved as PNG)

---

## 📂 Project Structure
```
.
├── app.py                # Main Flask application
├── templates/            # HTML templates
│   ├── home.html
│   ├── login.html
│   ├── signup.html
│   ├── blogform.html
│   ├── bloglist.html
│   ├── blogedit.html
│   ├── blogdetail.html
├── static/               # CSS, JS, images, exported CSV & plots
│   ├── blog_data.csv
│   ├── sentiment_plot.png
│   ├── cluster_plot.png
└── README.md             # Project documentation
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/yoursidhu3/blogverse.git
cd blogverse
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate   # For Linux/Mac
venv\Scripts\activate      # For Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

If you don’t have a `requirements.txt` yet, generate one:
```bash
pip freeze > requirements.txt
```

### 4. Setup the database
```bash
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```

Or simply:
```bash
python app.py
```
This will auto-create `project.db`.

### 5. Run the application
```bash
python app.py
```
Go to: **http://127.0.0.1:5000/**

---

## 📊 Data Export
- Export blog posts to CSV:  
  Visit: **/export_data**  
  File will be saved in `/static/blog_data.csv`

- Sentiment & Cluster plots are available at:  
  - `/sentiment_plot`  
  - `/cluster_plot`

---

## 🔐 Authentication
- Signup with name, email, and password  
- Login using your username & password  
- Secure routes: Adding, Editing, and Deleting blogs requires login

---

## 👨‍💻 Author 
Siddhu

---

## 📜 License
This project is for educational purposes only (college project).
