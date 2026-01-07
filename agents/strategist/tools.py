import os
import glob
import threading
import http.server
import socketserver
from io import BytesIO
from typing import Optional
from PIL import Image as PILImage
from agno.tools.function import ToolResult
from agno.media import Image
import yaml

with open("config.yaml") as f:
    port=f['IMAGE_SERVER_PORT']

class ImageServer:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, port=port):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self, port=8765):
        if self._initialized:
            return
        self.port = port
        self.serve_dir = "/tmp/agno_images"
        os.makedirs(self.serve_dir, exist_ok=True)
        self._start_server()
        self._initialized = True

    def _start_server(self):
        os.chdir(self.serve_dir)
        handler = http.server.SimpleHTTPRequestHandler
        socketserver.TCPServer.allow_reuse_address = True

        try:
            self.httpd = socketserver.TCPServer(("", self.port), handler)
            self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
            self.thread.start()
            print(f"Image server started on http://localhost:{self.port}")
        except OSError as e:
            print(self.port)

    def save_image(self, image_bytes: bytes, filename: str) -> str:
        filepath = os.path.join(self.serve_dir, filename)
        with open(filepath, 'wb') as f:
            f.write(image_bytes)
        return f"http://localhost:{self.port}/{filename}"


class StrategistTools:

    def __init__(self, db_path: str, ocr_folder: Optional[str] = None):
        self.db_path = db_path
        self.ocr_folder = ocr_folder
        self.image_server = ImageServer() if ocr_folder else None

    def view_page(self, page_number: int) -> ToolResult:
        """
        View a page image to understand document layout.

        Args:
            page_number: 1-based page number (matches database page_no column).

        Returns:
            The page image for visual analysis.
        """
        if not self.ocr_folder:
            return ToolResult(content="No OCR folder configured.")

        ocr_index = page_number - 1
        patterns = [f"*_{ocr_index}_ocr_res_img.png", f"*_{ocr_index}_ocr_res_img.jpg"]

        img_path = None
        for pattern in patterns:
            matches = glob.glob(os.path.join(self.ocr_folder, pattern))
            if matches:
                img_path = matches[0]
                break

        if not img_path:
            return ToolResult(content=f"No image for page {page_number}.")

        try:
            img = PILImage.open(img_path)
            img.thumbnail((1200, 1200))

            # Convert to JPEG bytes in memory
            buffer = BytesIO()
            img.convert('RGB').save(buffer, format='JPEG', quality=40)
            image_bytes = buffer.getvalue()

            # Save to local server and get URL
            filename = f"page_{page_number}.jpg"
            url = self.image_server.save_image(image_bytes, filename)

            # Return Image with URL - Gemini can fetch from localhost
            return ToolResult(
                content=f"Displaying page {page_number}",
                images=[Image(url=url)]
            )
        except Exception as e:
            return ToolResult(content=f"Error: {e}")
