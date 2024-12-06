import os
import unittest
from http import HTTPStatus
from io import BytesIO
from dotenv import load_dotenv
from fastapi.testclient import TestClient

# Assuming the FastAPI app is defined in a module named app
from podcast_storage.routers.file_storage_router import file_storage_router

load_dotenv()

class TestFileUpload(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """ This method is called once before all tests """
        # Set up the TestClient with the FastAPI router
        cls.client = TestClient(file_storage_router)
        cls.storage_dir = os.getenv("STORAGE_DIR")

    def setUp(self):
        """ This method is called before each test """
        # Clean up storage dir
        for file in os.listdir(self.storage_dir):
            os.remove(os.path.join(self.storage_dir, file))
    
    @classmethod
    def tearDownClass(cls):
        """ This method is called once after all tests """
        # Clean up storage dir
        for file in os.listdir(cls.storage_dir):
            os.remove(os.path.join(cls.storage_dir, file))

    def test_upload_large_file(self):
        # Generate a 10 MB in-memory file
        file_size = 10 * 1024 * 1024  # 10 MB
        file_content = BytesIO(b"x" * file_size)
        file_content.name = "test_file.dat"

        # Perform the POST request to the /file_storage/ endpoint
        response = self.client.post(
            "/",
            files={"file": (file_content.name, file_content, "application/octet-stream")}
        )

        # Assert that the request was successful
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response_data = response.json()

        # Check that the response contains the correct filename and size
        self.assertEqual(response_data["filename"], "test_file.dat")
        self.assertEqual(response_data["size"], file_size)

if __name__ == "__main__":
    unittest.main()