from base64 import b64encode
import functools
import sqlite3
from datetime import date
from io import BytesIO

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import abort

from flaskr.auth import login_required

from flaskr.db import get_db
from flaskr.auth import login_required

bp = Blueprint('museum', __name__, url_prefix='/museum')


@bp.route('/')
def index():
    """Correspond à la page d'accueil du musée qui affiche la liste des engrenages enregistrés"""

    conn = sqlite3.connect('flaskr/Data/gears.db')
    cursor = conn.cursor() 
    query = "SELECT * FROM gears" 
    gears_data = cursor.execute(query).fetchall()

    # Après avoir récupéré toutes les données dans la BDD, il faut réaliser une étape supplémentaire.
    # Les images sont stockées sous forme de blob (des chaînes en hexadécimal), et il faut donc les
    # décoder pour que Flask les affiche correctement.

    image_blobs = [gears_data[i][4] for i in range(len(gears_data))]
    images = []
    for i in image_blobs: images.append(b64encode(i).decode("utf-8"))
    gears = []
    for i in range(len(gears_data)):
        gears.append([gears_data[i][0],
                     gears_data[i][1],
                     gears_data[i][2],
                     gears_data[i][3],
                     images[i],
                     gears_data[i][5],
                     gears_data[i][6]])

    return render_template('gears_museum/gears_list.html', gears=gears)


@bp.route('/add', methods=('GET', 'POST'))
@login_required
def add():
    """Backend pour la page d'ajout d'un engrenage"""

    if request.method == 'POST':

        # Cette ligne récupère l'image entrée par l'utilisateur et la convertit en hexadécimal
        # pour pouvoir l'enregistrer dans une base de données ensuite
        image_blob = request.files["image"].read()

        name = request.form['name']
        benefits = request.form['benefits']
        drawbacks = request.form['drawbacks']
        current_date = date.today()
        conn = sqlite3.connect('flaskr/Data/gears.db') 
        cursor = conn.cursor() 
        query = """INSERT INTO gears (name, benefits, drawbacks, image, date, user) 
                VALUES (?, ?, ?, ?, ?, ?)""" 

        cursor.execute(query, (name, benefits, drawbacks, image_blob, current_date, g.user['username']))
        conn.commit()
        flash("""The item has been added to the database""")
    return render_template('gears_museum/add.html')
    
@bp.route('/<int:id>/edit', methods=('GET', 'POST'))
@login_required
def edit(id):
    """Page d'édition d'un engrenage. Son URL est dynamique, elle est générée automatiquement en fonction
    de l'id de l'engrenage en question"""
    if request.method == 'POST':

        name = request.form['name']
        benefits = request.form['benefits']
        drawbacks = request.form['drawbacks']

        image_blob = request.files["image"].read()

        conn = sqlite3.connect('flaskr/Data/gears.db')
        cursor = conn.cursor() 
        query = """UPDATE gears SET name=?, benefits=?, drawbacks=?, image=? WHERE id=?"""
        cursor.execute(query, (name, benefits, drawbacks, image_blob, id))
        conn.commit()
        flash("""The item has been edited successfully""")

        return redirect(url_for('museum.index'))

    conn = sqlite3.connect('flaskr/Data/gears.db')
    cursor = conn.cursor() 
    query = f"""SELECT * FROM gears WHERE id={id}"""
    existing_values = cursor.execute(query).fetchall()[0]
    return render_template('gears_museum/edit.html', existing_values=existing_values)

@bp.route('/<int:id>/delete')
@login_required
def delete(id):
    """Page de suppression d'un engrenage. Son URL est dynamique, elle est générée automatiquement en fonction
    de l'id de l'engrenage en question"""

    query = f"""DELETE FROM gears WHERE id={id}"""
    conn = sqlite3.connect('flaskr/Data/gears.db')
    cursor = conn.cursor() 
    cursor.execute(query)
    conn.commit()
    flash("""The item has been deleted successfully""")
    return redirect(url_for('museum.index'))

