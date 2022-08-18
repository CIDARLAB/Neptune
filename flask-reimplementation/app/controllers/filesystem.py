class FileSystem:
    
    def upload_file(self, file, filename):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return True
    
    def download_file(self, filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    
    
    def delete_file(self, filename):
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return True
    
    def copy_file(self, filename):
        shutil.copy(os.path.join(app.config['UPLOAD_FOLDER'], filename), app.config['UPLOAD_FOLDER'])
        return True
    
    def move_file(self, filename, destination):
        shutil.move(os.path.join(app.config['UPLOAD_FOLDER'], filename), os.path.join(app.config['UPLOAD_FOLDER'], destination))
        return True