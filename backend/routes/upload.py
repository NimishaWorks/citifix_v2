import os

from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

upload_bp = Blueprint('upload', __name__)

UPLOAD_FOLDER = "uploads"

ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "gif"
}


def allowed_file(filename):

    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@upload_bp.route('/upload-image', methods=['POST'])
def upload_image():

    try:

        if "image" not in request.files:

            return jsonify({
                "message": "No image provided"
            }), 400

        file = request.files["image"]

        if file.filename == "":

            return jsonify({
                "message": "No file selected"
            }), 400

        if not allowed_file(file.filename):

            return jsonify({
                "message": "Invalid file type"
            }), 400

        filename = secure_filename(file.filename)

        filepath = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        file.save(filepath)

        return jsonify({
            "message": "Image uploaded successfully",
            "filename": filename
        }), 201

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500