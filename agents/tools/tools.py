
from io import BytesIO
from typing import Optional
from agno.media import Image
from PIL import Image as PILImage
from agno.tools.function import ToolResult
import os, glob, threading, http.server, socketserver, time, base64, sqlite3


class ImageServer:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, port=8765):
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
            print(f"{e}\n {self.port}")

    def save_image(self, image_bytes: bytes, filename: str) -> str:
        filepath = os.path.join(self.serve_dir, filename)
        with open(filepath, 'wb') as f:
            f.write(image_bytes)
        return f"http://localhost:{self.port}/{filename}"


class StrategistTools:

    def __init__(self, db_path: str, ocr_folder: Optional[str] = None, use_base64: bool = False):
        """
        Initialize the toolkit.

        Args:
            db_path: Path to the SQLite database with OCR rows
            ocr_folder: Folder containing page images from OCR
            use_base64: If True, embed images as base64 (for OpenAI)
                        If False, serve via HTTP (for Gemini)
        """
        self.db_path = db_path
        self.ocr_folder = ocr_folder
        self.use_base64 = use_base64
        self.image_server = ImageServer() if (ocr_folder and not use_base64) else None
        self.images_viewed = 0

    def _find_image(self, page_num: int) -> Optional[str]:
        """Find the image file for a given page number."""
        if not self.ocr_folder:
            return None

        ocr_index = page_num - 1

        patterns = [
            f"{ocr_index}.png",                       # Simple: 0.png, 1.png, etc.
            f"*_{ocr_index}_ocr_res_img.png",         # Generic: anything_0_ocr_res_img.png
            f"*_{ocr_index}_ocr_res_img.jpg",         # Same but JPG
            f"page_{ocr_index}_ocr_res_img.png",      # Explicit: page_0_ocr_res_img.png
            f"page_{ocr_index}_ocr_res_img.jpg",      # Same but JPG
        ]

        for pattern in patterns:
            matches = glob.glob(os.path.join(self.ocr_folder, pattern))
            if matches:
                return matches[0]

        return None

    def view_page(self, page_number: int) -> ToolResult:
        """
        View a page image to understand document layout.

        Args:
            page_number: 1-based page number (matches database page_no column).

        Returns:
            The page image for visual analysis.
        """
        time.sleep(10)

        if not self.ocr_folder:
            return ToolResult(content="No OCR folder configured.")

        img_path = self._find_image(page_number)
        if not img_path:
            return ToolResult(content=f"No image for page {page_number}. Note: pages are 1-based (matching database).")

        try:
            img = PILImage.open(img_path)
            img.thumbnail((1200, 1200))

            buffer = BytesIO()
            img.convert('RGB').save(buffer, format='JPEG', quality=40)
            image_bytes = buffer.getvalue()

            self.images_viewed += 1

            if self.use_base64:
                b64_data = base64.b64encode(image_bytes).decode('utf-8')
                data_url = f"data:image/jpeg;base64,{b64_data}"
                return ToolResult(
                    content=f"Displaying page {page_number}",
                    images=[Image(url=data_url)]
                )
            else:
                filename = f"strategist_page_{page_number}.jpg"
                url = self.image_server.save_image(image_bytes, filename)
                return ToolResult(
                    content=f"Displaying page {page_number}",
                    images=[Image(url=url)]
                )
        except Exception as e:
            return ToolResult(content=f"Error: {e}")



class AssignerTools:

    def __init__(self, db_path: str, ocr_folder: Optional[str] = None, use_base64: bool = False):
        """
        Initialize the toolkit.

        Args:
            db_path: Path to the SQLite database with OCR rows
            ocr_folder: Folder containing page images from OCR
            use_base64: If True, embed images as base64 (for OpenAI)
                        If False, serve via HTTP (for Gemini)
        """
        self.db_path = db_path
        self.ocr_folder = ocr_folder
        self.use_base64 = use_base64

        self.image_server = ImageServer() if (ocr_folder and not use_base64) else None

        self.images_viewed = 0

    def _find_image(self, page_num: int) -> Optional[str]:
        if not self.ocr_folder:
            return None

        ocr_index = page_num - 1

        patterns = [
            f"{ocr_index}.png",                       # Simple: 0.png, 1.png, etc.
            f"*_{ocr_index}_ocr_res_img.png",         # Generic: anything_0_ocr_res_img.png
            f"*_{ocr_index}_ocr_res_img.jpg",         # Same but JPG
            f"page_{ocr_index}_ocr_res_img.png",      # Explicit: page_0_ocr_res_img.png
            f"page_{ocr_index}_ocr_res_img.jpg",      # Same but JPG
        ]

        for pattern in patterns:
            matches = glob.glob(os.path.join(self.ocr_folder, pattern))
            if matches:
                return matches[0]  # Return the first match

        return None

    
    def view_page(self, page_number: int) -> ToolResult:
        """
        View a page image.

        Args:
            page_number: 1-based page number (same as database page_no)

        Returns:
            ToolResult with image for visual analysis
        """
        time.sleep(10)

        if not self.ocr_folder:
            return ToolResult(content="No OCR folder.")

        img_path = self._find_image(page_number)
        if not img_path:
            return ToolResult(content=f"No image for page {page_number}. Note: pages are 1-based (matching database).")

        try:
            img = PILImage.open(img_path)

            img.thumbnail((1200, 1200))

            buffer = BytesIO()
            img.convert('RGB').save(buffer, format='JPEG', quality=40)  # Low quality = smaller size
            image_bytes = buffer.getvalue()

            self.images_viewed += 1

            if self.use_base64:
                b64_data = base64.b64encode(image_bytes).decode('utf-8')
                data_url = f"data:image/jpeg;base64,{b64_data}"
                return ToolResult(
                    content=f"Displaying page {page_number}",
                    images=[Image(url=data_url)]
                )
            else:
                filename = f"assigner_page_{page_number}.jpg"
                url = self.image_server.save_image(image_bytes, filename)
                return ToolResult(
                    content=f"Displaying page {page_number}",
                    images=[Image(url=url)]
                )

        except Exception as e:
            return ToolResult(content=f"Error: {e}")


    def runsql(self, sql: str) -> str:
        """
        Execute any SQL statement on the database.

        Handles both read (SELECT) and write (UPDATE, INSERT, DELETE) operations.

        Args:
            sql: The SQL statement to execute

        Returns:
            For SELECT: formatted results as a string
            For UPDATE/INSERT/DELETE: number of rows affected
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute(sql)

            sql_upper = sql.strip().upper()

            # CTEs start with WITH but are still read queries
            is_read_query = sql_upper.startswith('SELECT') or sql_upper.startswith('WITH')

            if is_read_query:
                rows = cursor.fetchall()

                if not rows:
                    conn.close()
                    return "No results found."

                columns = [desc[0] for desc in cursor.description]

                result_lines = [" | ".join(columns)]              # Column names
                result_lines.append("-" * len(result_lines[0]))   # Separator line
                for row in rows:
                    result_lines.append(" | ".join(str(val) for val in row))

                conn.close()
                return "\n".join(result_lines)

            else:
                rows_affected = cursor.rowcount

                conn.commit()
                conn.close()

                return f"Success: {rows_affected} row(s) affected."

        except Exception as e:
            return f"Error executing SQL: {e}"



class RCATools:
    """Read-only tools for Root Cause Analysis agent."""

    def __init__(self, db_path: str):
        self.db_path = db_path

    def runsql(self, sql: str) -> str:
        """
        Execute read-only SQL queries on the database.

        Only SELECT and WITH (CTE) queries are allowed.

        Args:
            sql: The SQL query to execute (SELECT or WITH only)

        Returns:
            Formatted query results as a string
        """
        try:
            sql_upper = sql.strip().upper()
            is_read_query = sql_upper.startswith('SELECT') or sql_upper.startswith('WITH')

            if not is_read_query:
                return "Error: RCA agent only has read-only access. Use SELECT or WITH queries."

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(sql)

            rows = cursor.fetchall()
            if not rows:
                conn.close()
                return "No results found."

            columns = [desc[0] for desc in cursor.description]
            result_lines = [" | ".join(columns)]
            result_lines.append("-" * len(result_lines[0]))
            for row in rows:
                result_lines.append(" | ".join(str(val) for val in row))

            conn.close()
            return "\n".join(result_lines)
        except Exception as e:
            return f"Error executing SQL: {e}"


class ReconstructorTools:

    def __init__(self, db_path: str):
        self.db_path = db_path

    def runsql(self, sql: str) -> str:
        """
        Execute any SQL statement on the database.

        Handles both read (SELECT) and write (CREATE, INSERT, UPDATE, DELETE) operations.

        Args:
            sql: The SQL statement to execute

        Returns:
            For SELECT: formatted results as a string
            For other statements: success message with rows affected
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(sql)

            sql_upper = sql.strip().upper()
            is_read_query = sql_upper.startswith('SELECT') or sql_upper.startswith('WITH')

            if is_read_query:
                rows = cursor.fetchall()
                if not rows:
                    conn.close()
                    return "No results found."

                columns = [desc[0] for desc in cursor.description]
                result_lines = [" | ".join(columns)]
                result_lines.append("-" * len(result_lines[0]))
                for row in rows:
                    result_lines.append(" | ".join(str(val) for val in row))

                conn.close()
                return "\n".join(result_lines)
            else:
                rows_affected = cursor.rowcount
                conn.commit()
                conn.close()
                return f"Success: {rows_affected} row(s) affected."
        except Exception as e:
            return f"Error executing SQL: {e}"
