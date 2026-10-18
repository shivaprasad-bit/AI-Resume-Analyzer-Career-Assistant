ALLOWED_RESUME_EXTENSIONS = {"pdf"}


def is_allowed_resume_file(filename):

    if not filename or "." not in filename:

        return False

    extension = filename.rsplit(".", 1)[1].lower()

    return extension in ALLOWED_RESUME_EXTENSIONS
