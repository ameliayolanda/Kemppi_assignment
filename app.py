from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import app

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
 
class Sport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sports = db.Column(db.String(100))
    team = db.Column(db.String(100))
    complete = db.Column(db.Boolean)
    against = db.Column(db.String(100))
    score = db.Column(db.String(100))
 
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    sport_list = db.session.query(Sport).all()
    #return "Hello World!"
    return render_template("index.html", sport_list=sport_list) 
 
@app.route("/add", methods=["POST"])
def add():
    sports = request.form.get("sports")
    team = request.form.get("team")
    against = request.form.get("against")
    score = request.form.get("score")
    new_sport = Sport(sports=sports, team=team, against=against, score=score, complete=False)
    db.session.add(new_sport)
    db.session.commit()
    return redirect(url_for("home"))
 
@app.route("/update/<int:sport_id>")
def update(sport_id):
    sport = db.session.query(Sport).filter(Sport.id == sport_id).first()
    sport.complete = not sport.complete
    db.session.commit()
    return redirect(url_for("home"))
 
@app.route("/delete/<int:sport_id>")
def delete(sport_id):
    sport = db.session.query(Sport).filter(Sport.id == sport_id).first()
    db.session.delete(sport)
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(debug=True)


    


