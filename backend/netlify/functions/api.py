"""Netlify serverless function handler"""
from mangum import Mangum
from app.main import app

# Create the handler for Netlify Functions
handler = Mangum(app, lifespan="off")
