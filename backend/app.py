from ai_agent import create_app, db
from flask_cors import CORS

from ai_agent.api.llm import llm_bp

app = create_app()
CORS(app, origins=["http://localhost:8080"], supports_credentials=True)

app.register_blueprint(llm_bp, url_prefix='/llm')

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()


if __name__ == '__main__':
    app.run(debug=True)

