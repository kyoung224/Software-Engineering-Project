import os
import flask
import random
from spotify import get_data, search_artist
from genius import get_lyrics
from flask_sqlalchemy import SQLAlchemy
import json

app = flask.Flask(__name__, static_folder='./build/static')
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.secret_key = b"Secret"

url = os.getenv("DATABASE_URL")
if url and url.startswith("postgres://"):
    url = url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# creating database table
class saved_artists(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    artist_ID = db.Column(db.String(50), nullable=False)

db.create_all()

# used to keep track of who is logged in
current_user = ""

# This tells our Flask app to look at the results of `npm build` instead of the 
# actual files in /templates when we're looking for the index page file. This allows
# us to load React code into a webpage. Look up create-react-app for more reading on
# why this is necessary.
bp = flask.Blueprint("bp", __name__, template_folder="./build")

@bp.route('/main', methods = ["GET", "POST"])
def main():
    # TODO: insert the data fetched by your app main page here as a JSON

    # variables are all set to blank in order to avoid getting errors when no artist in database
    artistName_list = []
    title = ""
    artist = ""
    image = ""
    url = ""
    lyrics = ""
    spotify_url = ""
    album_name = ""
    release_date = ""
    popularity = ""
    track_number = ""
    artist_img = ""
    artist_follower = ""
    artist_genre = ""
    artist_page = ""

    artistID_list = getDB("ID")

    length = len(artistID_list)

    if length > 0:

        # pick random artist id from the list
        artist_to_search = randomArtist(artistID_list)

        # reach the function named get_data in spotify.py by randomly chosen artist id and store
        song_data = get_data(artist_to_search)

        # reach the function named get_lyrics in genius.py by randomly chosen artist's top track title and store
        lyrics_data = get_lyrics(song_data["title"])

        title = song_data["title"]
        artist = song_data["artist"]
        image = song_data["image"]
        url = song_data["url"]
        lyrics = lyrics_data["lyrics"]

        # extra features
        spotify_url = song_data["spotify_url"]
        album_name = song_data["album_name"]
        release_date = song_data["release_date"]
        popularity = song_data["popularity"]
        track_number = song_data["track_number"]
        artist_img = song_data["artist_img"]
        artist_follower = song_data["artist_follower"]
        artist_genre = song_data["artist_genre"]
        artist_page = song_data["artist_page"]

        # store artists by name instead of ID for showing who is listed
        for i in artistID_list:
            data = get_data(i)
            artistName = data["artist"]
            artistName_list.append(artistName)

    DATA = {
        # basic requirements
        "title": title,
        "artist": artist,
        "image": image,
        "url": url,
        "lyrics": lyrics,
        # extra features
        "spotify_url": spotify_url,
        "album_name": album_name,
        "release_date": release_date,
        "popularity": popularity,
        "track_number": track_number,
        "artist_img": artist_img,
        "artist_follower": artist_follower,
        "artist_genre": artist_genre,
        "artist_page": artist_page,
        "length": length,
        "current_user": current_user,
        "artistName_list": artistName_list,
    }
    data = json.dumps(DATA)
    return flask.render_template(
        "index.html",
        data = data,
    )

app.register_blueprint(bp)

@app.route("/")
def index():
    if current_user == "":
        return flask.render_template("login.html")
    return flask.redirect("/main")

# returned from login.html to see if user is signed up
@app.route("/login", methods=["POST"])
def login():

    # saving input from user
    input_username = flask.request.form.get("username")

    user_list = getDB("User")

    # check if input username exists in db and if is, keep track of it and redirect to the main page
    # if not, warn user
    for i in user_list:
        if i == input_username:
            global current_user
            current_user = input_username
            return flask.redirect("/main")

    flask.flash("Invalid username!")
    return flask.redirect("/")

# returned from login.html to see if username is valid / create user
@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():

    input_username = flask.request.form.get("sign_up_username")

    user_list = getDB("User")

    # check if username already exists in db and if is, warn user
    for i in user_list:
        if i == input_username:
            flask.flash("Username already exists!")
            return flask.redirect("/")

    # if not, add user to the db
    user = saved_artists(username = input_username, artist_ID = "0")
    db.session.add(user)
    db.session.commit()

    # keep track of the user
    global current_user
    current_user = input_username

    return flask.redirect("/main")

def getDB(data):

    items = saved_artists.query.all()
    user_list = []
    artistID_list  = []

    # only add artistsID added by the user who is currently logged in
    for item in items:
        user_list.append(item.username)

        if item.artist_ID != "0" and item.username == current_user:
            artistID_list.append(item.artist_ID)

    if data == "User":
        return user_list
    elif data == "ID":
        return artistID_list
    elif data == "All":
        return (user_list, artistID_list)

# used for testing
def randomArtist(artistID_list):
        return random.choice(artistID_list)
        
@app.route("/addArtist", methods = ["POST"])
def addArtist():

    artistNameList = []

    if flask.request.method == "POST":
        artist_input = flask.request.json.get("artist_input")

        for i in artist_input:
            search_data = search_artist(i)
            if search_data["artistID"] == "-1":
                wrongArtist = True

            else:
                artists = saved_artists(
                    username = current_user, artist_ID = search_data["artistID"]
                )
                db.session.add(artists)
                db.session.commit()
                
                artistName = search_data["artistName"]
                artistNameList.append(artistName)

                wrongArtist = False

            if wrongArtist == True:
                return flask.jsonify({"input_server": False})

    return flask.jsonify({"input_server": artistNameList})

@app.route("/deleteArtist", methods = ["POST"])
def deleteArtist():

    artistNameList = []
    wrongArtist = True

    if flask.request.method == "POST":
        artist_input = flask.request.json.get("artist_input")

        artistID_list = getDB("ID")

        for artist in artistID_list:
            search_data = get_data(artist)
            artistNameList.append(search_data["artist"])
        
        for input in artist_input:
            for name in artistNameList:
                if (input == name):
                    search_data = search_artist(name)
                    saved_artists.query.filter_by(username=current_user, artist_ID = search_data["artistID"]).delete()
                    db.session.commit()
                    print("INPUT: ", input)
                    wrongArtist = False

        if wrongArtist == True:
            return flask.jsonify({"input_server": False})

    return flask.jsonify({"input_server": artistNameList})

# used to deploy webpage to heroku
app.run(
    # host="0.0.0.0", 
    # port=int(os.getenv("PORT", 8080)), 
    debug=True)
