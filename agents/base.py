from socket import SO_VM_SOCKETS_BUFFER_SIZE
import time,os,glob,sqlite3,threading, http.server,socketserver,base64
from io import BytesIO
from typing import Optional
from PIL import Image as PILImage
from agno.tools.function import ToolResult
from agno.media import Image


class ImageServer:
    _instance=None
    _lock=threading.lock()

    def __new__(cls,port=8899):
        with cls._lock:
            if cls._instance is None:
                cls._instance=super()
                cls._instance._initialized=False
            return cls._instance
    
    def __init__(self, port=8899):
        if self._initialized:
            return
        self.port = port
        self.serve_dir = "/tmp/agno_images"
        os.makedirs(self.serve_dir, exist_ok=True)
        self._start_server()
        self._initialized = True

    def _start_server(self):

        os.chdir(self.serve_dir)
        handler=http.server.SimpleHTTPRequestHandler
        socketserver.TCPServer.allow_reuse_address=True

