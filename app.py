from flask import Flask, render_template
import sys
application = Flask(__name__)

@application.route("/")
def hello():
  return "Hello my webpage!"
