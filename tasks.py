from werkzeug.utils import secure_filename
import os



def upload_file(file ,app):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

