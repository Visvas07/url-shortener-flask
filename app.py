from flask import Flask, request, render_template, redirect,url_for,session,flash,jsonify
from flask_sqlalchemy import SQLAlchemy
import string,random,os
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET_KEY")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///urls.db'

db = SQLAlchemy(app)

'''
Table definition of URL
ID: Unique URL ID
Original URL: The original URL that we need to shorten
Short URL Code: The short url code that would be generated
'''
class URL(db.Model):
    id = db.Column('url_id',db.Integer,primary_key=True)
    original_url=db.Column(db.String(550),nullable=False)
    short_url_code = db.Column(db.String(15),unique=True,nullable=False)
    
'''
Args: length: integer argument default is set as 10.
Returns: a randomized string of characters containing ASCII letters and digits.
'''
def generate_short_code_url(length=10):
    characters = string.ascii_letters + string.digits
    return "".join(random.choices(characters,k=length))
    
'''
Creates the table before sending the request
'''    
@app.before_request
def create_table():
    db.create_all()

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        original_url = request.form['url']
        custom_alias = request.form['alias']
        if custom_alias:
            existing_alias = URL.query.filter_by(short_url_code=custom_alias).first()
            if existing_alias:
                return render_template("index.html",msg="Custom alias already taken, try another one!")
            short_code = custom_alias
        else:
            short_code = generate_short_code_url()
        search_url_if_exists = URL.query.filter_by(original_url=original_url).first()
        if search_url_if_exists and not custom_alias:
            print("Already exisiting original url")
            short_code = search_url_if_exists.short_url_code
            print(short_code)
            session['short_url'] = short_code
            return redirect(url_for('index'))     
        new_url = URL(original_url=original_url,short_url_code=short_code)
        db.session.add(new_url)
        db.session.commit()
        session['short_url'] = short_code
        return redirect(url_for('index'))
    short_url = session.pop('short_url',None)
    return render_template("index.html",short_url=short_url)

@app.route('/<short_code_url>')
def redirect_url(short_code_url):
    url_entry = URL.query.filter_by(short_url_code=short_code_url).first()
    if url_entry:
        return redirect(url_entry.original_url)
    else:
        return render_template("not_found.html")
    
@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('admin_db'))
        else:
            return render_template("login.html",error='Invalid Credentials')
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('logged_in',False)
    return redirect(url_for('login'))

@app.route('/admin/db')
def admin_db():
    headers = ['Shortened code','Original URL','Appended shortened URL','Actions']
    if not session['logged_in']:
        return redirect(url_for('login'))
    urls = URL.query.all()
    return render_template("results.html",headers=headers,urls=urls)

@app.route('/reset')
def reset():
    session.pop('short_url',None)
    session.pop('msg',None)
    return redirect(url_for('index'))

@app.route('/login_reset')
def login_reset():
    return redirect(url_for('login'))

@app.route('/delete/<int:url_id>',methods=['POST'])
def delete(url_id):
    url = URL.query.get_or_404(url_id)
    if url:   
        db.session.delete(url)
        db.session.commit()
        flash("DB entry successfully deleted",'success')
        #return jsonify({"msg":"URL deleted successfully"}),200
    else:
        flash("URL not found! failed to delete URL",'error')
        # return jsonify({"msg":"Failed to delete URL"}),404
    return redirect(url_for('admin_db'))
    
if __name__ == '__main__':
    app.run(debug=True)