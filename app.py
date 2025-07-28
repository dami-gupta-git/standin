import os
from flask import Flask, jsonify, request, send_file
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# The following imports will cause an error initially.
# You need to create the files first, then this will work.
from models.file_model import db, FileMetadata
from services.db_service import get_all_files_metadata, get_file_metadata_by_id, create_file_metadata
from services.s3_service import download_file_from_s3, generate_presigned_url

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create database tables if they don't exist
with app.app_context():
    db.create_all()


@app.route('/files', methods=['GET'])
def list_files():
    """
    Endpoint to list all file metadata from the database.
    Returns: JSON array of file metadata objects.
    """
    files = get_all_files_metadata()
    return jsonify([file.to_dict() for file in files])


@app.route('/files/<int:file_id>', methods=['GET'])
def get_file_details(file_id):
    """
    Endpoint to get metadata for a single file.
    Returns: JSON object of file metadata.
    """
    file_metadata = get_file_metadata_by_id(file_id)
    if not file_metadata:
        return jsonify({"error": "File not found"}), 404

    return jsonify(file_metadata.to_dict())


@app.route('/files/<int:file_id>/download', methods=['GET'])
def download_file(file_id):
    """
    Endpoint to download a file from S3 using its ID.
    Returns: The file content as a response.
    """
    file_metadata = get_file_metadata_by_id(file_id)
    if not file_metadata:
        return jsonify({"error": "File not found"}), 404

    file_content = download_file_from_s3(file_metadata.s3_key)
    if file_content is None:
        return jsonify({"error": "File could not be downloaded from S3"}), 500

    # You might need to set a proper mimetype
    return send_file(
        file_content,
        mimetype='application/octet-stream',
        as_attachment=True,
        download_name=file_metadata.filename
    )


@app.route('/files/<int:file_id>/url', methods=['GET'])
def get_file_presigned_url(file_id):
    """
    Endpoint to get a presigned S3 URL for a file.
    Returns: A JSON object with the presigned URL.
    """
    file_metadata = get_file_metadata_by_id(file_id)
    if not file_metadata:
        return jsonify({"error": "File not found"}), 404

    url = generate_presigned_url(file_metadata.s3_key)
    if not url:
        return jsonify({"error": "Could not generate presigned URL"}), 500

    return jsonify({"url": url})


@app.route('/files', methods=['POST'])
def add_file_metadata():
    """
    Endpoint to add new file metadata to the database.
    This doesn't upload the file, just creates a database entry.
    """
    data = request.json
    if not data or 'filename' not in data or 's3_key' not in data:
        return jsonify({"error": "Missing 'filename' or 's3_key' in request body"}), 400

    new_file = create_file_metadata(
        filename=data['filename'],
        s3_key=data['s3_key'],
        description=data.get('description', '')
    )

    return jsonify(new_file.to_dict()), 201


if __name__ == '__main__':
    app.run()