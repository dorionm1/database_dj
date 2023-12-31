from flask import Flask, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Playlist, Song, PlaylistSong
from forms import NewSongForPlaylistForm, SongForm, PlaylistForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///playlist_app"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

connect_db(app)

with app.app_context():
    # Create database tables
    db.create_all()

app.config["SECRET_KEY"] = "I'LL NEVER TELL!!"

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route("/")
def root():
    """Homepage: redirect to /playlists."""

    return redirect("/playlists")


##############################################################################
# Playlist routes


@app.route("/playlists")
def show_all_playlists():
    """Return a list of playlists."""

    playlists = Playlist.query.all()
    return render_template("playlists.html", playlists=playlists)


@app.route("/playlists/<int:playlist_id>")
def show_playlist(playlist_id):
    """Show detail on specific playlist."""
    playlist = Playlist.query.get(playlist_id)
    songs = PlaylistSong.query.get(playlist_id)

    playlist_songs = (
        db.session.query(Song.title)
        .join(PlaylistSong, Song.id == PlaylistSong.song_id)
        .filter(PlaylistSong.playlist_id == playlist_id)
        .all()
    )

    return render_template(
        "playlist.html", playlist=playlist, playlist_songs=playlist_songs
    )
    # ADD THE NECESSARY CODE HERE FOR THIS ROUTE TO WORK


@app.route("/playlists/add", methods=["GET", "POST"])
def add_playlist():
    """Handle add-playlist form:

    - if form not filled out or invalid: show form
    - if valid: add playlist to SQLA and redirect to list-of-playlists
    """
    form = PlaylistForm()

    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data

        new_playlist = Playlist(name=name, description=description)

        db.session.add(new_playlist)
        db.session.commit()

        return redirect("/playlists")

    else:
        return render_template("new_playlist.html", form=form)


##############################################################################
# Song routes


@app.route("/songs")
def show_all_songs():
    """Show list of songs."""

    songs = Song.query.all()
    return render_template("songs.html", songs=songs)


@app.route("/songs/<int:song_id>")
def show_song(song_id):
    """return a specific song"""
    song = Song.query.get(song_id)
    playlists = PlaylistSong.query.get(song_id)

    # ADD THE NECESSARY CODE HERE FOR THIS ROUTE TO WORK
    return render_template("song.html", song=song, playlists=playlists)


@app.route("/songs/add", methods=["GET", "POST"])
def add_song():
    """Handle add-song form:

    - if form not filled out or invalid: show form
    - if valid: add playlist to SQLA and redirect to list-of-songs
    """
    form = SongForm()

    if form.validate_on_submit():
        title = form.title.data
        artist = form.artist.data

        new_song = Song(title=title, artist=artist)

        db.session.add(new_song)
        db.session.commit()

        return redirect("/songs")

    else:
        return render_template("new_song.html", form=form)
    # ADD THE NECESSARY CODE HERE FOR THIS ROUTE TO WORK


@app.route("/playlists/<int:playlist_id>/add-song", methods=["GET", "POST"])
def add_song_to_playlist(playlist_id):
    """Add a playlist and redirect to list."""

    playlist = Playlist.query.get_or_404(playlist_id)

    form = NewSongForPlaylistForm()
    choices = []

    curr_on_playlist = [s.id for s in playlist.songs]
    results = (
        db.session.query(Song.id, Song.title)
        .filter(Song.id.notin_(curr_on_playlist))
        .all()
    )

    for r in results:
        choices.append((r.id, r.title))

    form.song.choices = choices

    if form.validate_on_submit():
        playlist_song = PlaylistSong(song_id=form.song.data, playlist_id=playlist_id)
        db.session.add(playlist_song)
        db.session.commit()

        return redirect(f"/playlists/{playlist_id}")

    return render_template("add_song_to_playlist.html", playlist=playlist, form=form)
