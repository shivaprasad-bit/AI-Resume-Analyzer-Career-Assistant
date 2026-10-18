import unittest

from upload_validation import is_allowed_resume_file


class UploadValidationTests(unittest.TestCase):
    def test_accepts_pdf_filenames(self):
        self.assertTrue(is_allowed_resume_file("resume.pdf"))
        self.assertTrue(is_allowed_resume_file("Resume.PDF"))
        self.assertTrue(is_allowed_resume_file("my.resume.v2.pdf"))

    def test_rejects_non_pdf_filenames(self):
        self.assertFalse(is_allowed_resume_file("resume.docx"))
        self.assertFalse(is_allowed_resume_file("resume.png"))
        self.assertFalse(is_allowed_resume_file("resume.pdf.exe"))

    def test_rejects_blank_or_extensionless_filenames(self):
        self.assertFalse(is_allowed_resume_file(""))
        self.assertFalse(is_allowed_resume_file(None))
        self.assertFalse(is_allowed_resume_file("resume"))


if __name__ == "__main__":
    unittest.main()
