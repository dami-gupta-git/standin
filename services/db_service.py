from models.file_model import FileMetadata, db

def get_all_files_metadata():
    """Fetches all file metadata from the database."""
    return FileMetadata.query.all()

def get_file_metadata_by_id(file_id):
    """Fetches metadata for a single file by its ID."""
    return FileMetadata.query.get(file_id)

def create_file_metadata(filename, s3_key, description):
    """Creates a new metadata entry in the database."""
    new_file = FileMetadata(filename=filename, s3_key=s3_key, description=description)
    db.session.add(new_file)
    db.session.commit()
    return new_file