from ai_agent import create_app, db
from flask_cors import CORS


app = create_app()
CORS(app, origins=["http://localhost:8080"], supports_credentials=True)
CORS(app, resources={r"/rag/*": {"origins": "*"}})



@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)

