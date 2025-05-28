from google.cloud import storage
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from django.conf import settings
import uuid
import mimetypes
import os
import json
from google.oauth2 import service_account

@deconstructible
class UniqueFilenameGoogleCloudStorage(Storage):
    def __init__(self, bucket_name=None):
        try:
            # Get credentials from Django settings
            credentials = service_account.Credentials.from_service_account_info(settings.GCP_CREDENTIALS)
            self.client = storage.Client(credentials=credentials, project=settings.GCP_PROJECT_ID)
            self.bucket_name = bucket_name or settings.GCP_BUCKET_NAME
            self.bucket = self.client.bucket(self.bucket_name)
        except Exception as e:
            import logging
            logging.error(f"Error initializing GCS storage: {str(e)}")
            raise

    def _save(self, name, content):
        """Save a file to Google Cloud Storage with a unique name."""
        # Generate a unique filename using UUID
        file_extension = os.path.splitext(name)[1] if name else ''
        unique_name = f"{uuid.uuid4()}{file_extension}"
        blob = self.bucket.blob(unique_name)

        # Try to get content_type from the content object, or guess it from the filename
        content_type = getattr(content, 'content_type', None)
        if not content_type:
            content_type = mimetypes.guess_type(name)[0] or 'application/octet-stream'

        # Upload file to GCS
        try:
            # If content is a file-like object, use upload_from_file
            if hasattr(content, 'seek'):
                content.seek(0)
                blob.upload_from_file(content, content_type=content_type)
            else:
                # If content is bytes or string, use upload_from_string
                blob.upload_from_string(content.read(), content_type=content_type)
        except Exception as e:
            import logging
            logging.error(f"Error uploading file to GCS: {str(e)}")
            raise

        return unique_name

    def exists(self, name):
        """Check if a file exists in Google Cloud Storage."""
        blob = self.bucket.blob(name)
        return blob.exists()

    def url(self, name):
        """Generate a public URL for the file."""
        return f"https://storage.googleapis.com/{self.bucket_name}/{name}"

    def get_valid_name(self, name):
        """Return a valid name for the file."""
        return name

    def get_available_name(self, name, max_length=None):
        """Return a filename that's free on the target storage system."""
        # Since we're using UUID, we don't need to check for duplicates
        return name

    def delete(self, name):
        """Delete the specified file from storage."""
        try:
            self.bucket.blob(name).delete()
        except Exception:
            pass  # If the file doesn't exist, just ignore the error

    def size(self, name):
        """Return the total size, in bytes, of the file."""
        blob = self.bucket.blob(name)
        return blob.size if blob.exists() else 0

    def generate_filename(self, filename):
        """Generate filename for storage."""
        return os.path.join(settings.MEDIA_ROOT, filename)