from queue_aux.queue import send_doc_file

ALLOWED_EXTENSIONS = {'txt', 'docx', 'doc'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def send_file_to_queue(filename):
    if send_doc_file(filename):
        return "Converting your file, await"
    return "Not possible right now to convert your file to pdf, try again later"