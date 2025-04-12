from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
import string,random

app = Flask(__name__)
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
            return render_template("index.html",short_code_url=short_code)     
        new_url = URL(original_url=original_url,short_url_code=short_code)
        db.session.add(new_url)
        db.session.commit()
        return render_template("index.html",short_code_url = short_code)
    return render_template("index.html")

@app.route('/<short_code_url>')
def redirect_url(short_code_url):
    url_entry = URL.query.filter_by(short_url_code=short_code_url).first()
    if url_entry:
        return redirect(url_entry.original_url)
    else:
        return render_template("not_found.html")
    
if __name__ == '__main__':
    app.run(debug=True)