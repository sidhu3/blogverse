from flask import Flask,render_template,request,redirect,flash,url_for,jsonify,send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,login_user,UserMixin,logout_user,login_required
import datetime
from flask_migrate import Migrate
from textblob import TextBlob
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import os
import pandas as pd

app = Flask(__name__)

#Database
db=SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'
db.init_app(app)
migrate = Migrate(app, db)


# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
# login_manager.login_view = 'login'  # View to redirect unauthorized users
class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    email = db.Column(db.String) 

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(50), nullable=False)    
    content = db.Column(db.Text(), nullable=False)
    sentiment = db.Column(db.String(50), nullable=True)  # New column for sentiment
    pub_date = db.Column(db.DateTime,nullable=False,default = datetime.datetime.now().replace(microsecond=0))


@app.before_request
def update_existing_data():
    records=Blog.query.all()

    for record in records:
        if record.pub_date:
            record.pub_date= record.pub_date.replace(microsecond=0)

    db.session.commit()        

@app.route('/')
def temp_view():
    return render_template('home.html')


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

login_manager.login_view = "login" 
# Optional: Customize the unauthorized handler
@login_manager.unauthorized_handler
def unauthorized():
    # Redirect to the login page
    return redirect(url_for('login'))  # Replace 'login' with the name of your login route

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=='POST':
        print('start')
        name=request.form.get('uname')
        pwd=request.form.get('upassword')
        user = User.query.filter_by(username=name).first()

        if user and pwd == user.password:
            login_user(user)
             # Redirect to the original page or a default page
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/')  # 'home' is your default route

            # flash('Login success', ' info')
            # return redirect('/')
        else:
            flash('Invalid user name or password!')
            return redirect('/login')
    return render_template('login.html')


@app.route('/signup',methods=['GET','POST'])
def signup_view():
    if request.method=='POST':
        name=request.form.get('uname')
        pwd=request.form.get('upassword')
        fname=request.form.get('fname')
        print(fname)
        lname=request.form.get('lname')
        print(lname)
        email=request.form.get('email')
        print(email)
        user=User(username=name,password=pwd,firstname=fname,lastname=lname,email=email)
        db.session.add(user)
        db.session.commit()
        flash('User updated successfully!', 'success')
        return redirect('/login')
    return render_template('signup.html')
with app.app_context():
    db.create_all() 


@app.route('/blog', methods=['GET', 'POST'])
@login_required
def add_blog():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')

        # Perform Sentiment Analysis on Content
        if content and content.strip() != "":
            analysis = TextBlob(content)
            sentiment = "Positive" if analysis.sentiment.polarity > 0 else "Negative" if analysis.sentiment.polarity < 0 else "Neutral"
        else:
            sentiment = "No content to analyze."

        # Create and save the blog post
        blog = Blog(title=title, author=author, content=content, sentiment=sentiment)
        db.session.add(blog)
        db.session.commit()
        flash('Post added successfully!', 'success')
        return redirect('/bloglist')
    return render_template('blogform.html')


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')  # Get the search query
    page = request.args.get('page', 1, type=int)  # Get the current page for pagination
    per_page = 12  # Number of blogs per page

    # Filter blogs based on the query
    blogs = Blog.query.filter(
        Blog.title.ilike(f'%{query}%') |
        Blog.author.ilike(f'%{query}%') |
        Blog.content.ilike(f'%{query}%')
    ).paginate(page=page, per_page=per_page)

    return render_template('bloglist.html', query=query, blogs=blogs)


@app.route('/bloglist')
def blog_list():
    page = request.args.get('page', 1, type=int)  # Get the current page from URL, default to 1
    per_page = 12  # Number of blogs per page
    blogs = Blog.query.paginate(page=page, per_page=per_page)
    return render_template('bloglist.html', blogs=blogs)


@app.route('/edit/<int:id>',methods=['GET','POST'])
@login_required
def edit_blog(id):
    b=Blog.query.get(id)
    if request.method=='POST':
        b.title=request.form.get('title')
        b.author=request.form.get('author')
        b.content=request.form.get('content')
        # b.pub_date=datetime.datetime.now()
        db.session.commit()
        flash('Post updated successfully!')
        return redirect('/bloglist')
    return render_template('blogedit.html',b=b)


@app.route("/detail/<int:id>")
def blog_detail(id):
    b=Blog.query.get_or_404(id)

    # Summarization
    try:
        summary = summarize_text(b.content, sentence_count=3)
    except Exception as e:
        summary = "Content is too short to summarize."

    return render_template('blogdetail.html',b=b,summary=summary)

# Function to summarize text
def summarize_text(content, sentence_count=3):
    if len(content.split()) < 50:  # Minimum 50 words
        return "Content is too short to summarize!"  # Return content as-is if it's too short
    
    try:
        # Parse the content and summarize using LSA (Latent Semantic Analysis)
        parser = PlaintextParser.from_string(content, Tokenizer("english"))
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, sentence_count)
        return " ".join([str(sentence) for sentence in summary])
    except Exception as e:
        return f"Error during summarization: {str(e)}"


@app.route("/del/<int:id>")
@login_required
def blog_del(id):
    b=Blog.query.get(id)
    db.session.delete(b)
    db.session.commit() 
    return redirect('/bloglist')


@app.route("/logout")
def logout():
    logout_user()
    return redirect('/')    


# Export data from Blog model for R
@app.route('/export_data')
def export_data():
    try:
        # Query all blog posts
        blog_posts = Blog.query.all()

        # Convert to a list of dictionaries
        blog_data = [
            {
                "author": post.author,
                "content": post.content,
                "sentiment": post.sentiment,
                "date": post.pub_date.strftime("%Y-%m-%d")  # Format date as string
            }
            for post in blog_posts
        ]
        
        # Create a DataFrame
        df = pd.DataFrame(blog_data)

        # Ensure the static directory exists
        static_folder = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static')
        if not os.path.exists(static_folder):
            os.makedirs(static_folder)

        # Define file path
        file_path = os.path.join(static_folder, 'blog_data.csv')

        # Export to CSV
        df.to_csv(file_path, index=False)

        # Return success message
        return jsonify({"message": "Data exported to CSV!", "file_link": f"/static/blog_data.csv"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "Failed to export data", "error": str(e)}), 500
    
import subprocess


@app.route('/sentiment_plot')
def sentiment_plot():
    return send_from_directory('static', 'sentiment_plot.png')

@app.route('/cluster_plot')
def cluster_plot():
    return send_from_directory('static', 'cluster_plot.png')



if __name__=='__main__':
    app.run(debug=True)
