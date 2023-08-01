from MapInfo import MapInfo
from Game import Game
from DBManager import Base, osuMap
from flask import Flask, render_template, url_for
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, select, func, column


# TODO
# -Optimize AutoFill for the answer box
# -add support for wrong guesses (show user their guesses)
# -Add a language filter option

# -css

# -Figure out how to properly handle songs with long intros (2477069)
# -Replace #1 play with star ratings and length and other stuff

# -find a way to expand the db (adding more columns dynamically)
# -find a way to overwrite video files


app = Flask(__name__)
engine = create_engine("sqlite+pysqlite:///instance/db.sqlite3", echo=True, future=True)
Base.metadata.create_all(bind=engine, checkfirst=True)
Session = sessionmaker(bind=engine)
session = Session()
alltitles = [title for title, in session.query(osuMap.title)]




@app.route("/")
def index():
    result = session.query(osuMap).order_by(func.random()).first()
    newGame = Game(result)
    return render_template('index.html', game=newGame, maptitles=alltitles)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=False)
