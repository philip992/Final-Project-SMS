print("Starting server...")

from waitress import serve
from Home.wsgi import application

serve(application, host='0.0.0.0', port=8000)

print("Server has stopped")
