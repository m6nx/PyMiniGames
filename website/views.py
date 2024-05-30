from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
import subprocess


views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/profile', methods=["GET","POST"])
@login_required
def profile():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('You didn\'t add a note!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("profile.jinja", user=current_user)

@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            flash('Note Deleted!', category='success')
           
    return jsonify({})

@views.route('/start-game', methods=['POST'])
def start_game():
    subprocess.Popen(["python", 'Defender/beach_defender.py'], creationflags=subprocess.CREATE_NO_WINDOW)
    return 'Game started', 200

@views.route('/start-game2', methods=['POST'])
def start_game2():
    subprocess.Popen(["python", 'Cowboy/Monkey_Hates_Cowboy.py'], creationflags=subprocess.CREATE_NO_WINDOW)
    return 'Game started', 200
