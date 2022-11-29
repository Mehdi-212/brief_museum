import pytest
import sqlite3
import requests
from datetime import date


def test_add_gear(auth, client):

	"""NON TERMINÉ : ce test unitaire ne fonctionne pas (un problème d'authtification, visiblement)"""
	auth.login()
	assert client.get('/museum/add').status_code == 200

	with open("test_image.png", "rb") as image:
		image_blob = image.read()

	params = {"name": "test",
			"benefits": "test",
			"drawbacks": "test",
			"image": image_blob}


	r = requests.post("http://127.0.0.1:5000/museum/add", data=params)
	print(r.status_code)

	conn = sqlite3.connect('../flaskr/Data/gears.db')
	cursor = conn.cursor() 
	select_query = "SELECT * FROM gears ORDER BY id DESC LIMIT 1;"
	inserted_data = cursor.execute(select_query).fetchall()[0]
	print(r.content)
	assert inserted_data == (inserted_data[0], "test", "test", "test", image_blob, date.today(), "test")

	    
	

def test_edit_gear():

	...

def test_delete_gear():

	...
