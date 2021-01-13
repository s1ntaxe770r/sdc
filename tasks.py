from main import app
from werkzeug.utils import secure_filename
import os
from celery import make_celery

ALLOWED_EXTENSIONS = set([ 'png', 'jpg', 'jpeg','webp'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

celery = make_celery(app)

@celery.task
def upload_file(file ,app):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

