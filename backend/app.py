from flask import Flask
from routes.auth import auth_bp
from routes.issues import issues_bp
from routes.comments import comments_bp
from routes.votes import votes_bp
from routes.analytics import analytics_bp
from routes.upload import upload_bp
from flask import send_from_directory
from flask_cors import CORS
app=Flask(__name__)
CORS(app)
app.register_blueprint(auth_bp)
app.register_blueprint(issues_bp)
app.register_blueprint(comments_bp)
app.register_blueprint(votes_bp)
app.register_blueprint(analytics_bp)
app.register_blueprint(upload_bp)
@app.route("/")
def home():
    return "CitiFix V2 Backend Running"
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)
if __name__=="__main__":
    app.run(debug=True)
