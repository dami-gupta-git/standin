from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class FileMetadata(db.Model):
    __tablename__ = 'file_metadata'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False, unique=True)
    s3_key = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)

    def __repr__(self):
        return f"<FileMetadata(filename='{self.filename}', s3_key='{self.s3_key}')>"

    def to_dict(self):
        return {
            "id": self.id,
            "filename": self.filename,
            "s3_key": self.s3_key,
            "description": self.description
        }