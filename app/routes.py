# Placeholder for route definitions like login, dashboard, cert management
from flask import render_template, redirect, url_for, request, flash
from app import app, db
from app.models import Client, HCP, Residence
