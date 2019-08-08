from app import app
from flask import Flask, request

@app.route('/')
def index():
	return 'Hello, world!'