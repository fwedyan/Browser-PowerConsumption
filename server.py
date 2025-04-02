#!/usr/bin/env python3
import os
import http.server
import socketserver
import threading
import tempfile
from pathlib import Path
import html_templates
from config import VIDEO_SERVER_PORT, VIDEO_FILES
from utils import log_message

def start_local_test_server():
    temp_dir = tempfile.mkdtemp()
    
    for video_format, video_path in VIDEO_FILES.items():
        if video_path.exists():
            video_filename = video_path.name
            os.symlink(video_path, Path(temp_dir) / video_filename)
        else:
            log_message(f"Warning: Video file not found: {video_path}")
    
    video_html = html_templates.get_video_html()
    
    video_source_html = ""
    for video_format, video_path in VIDEO_FILES.items():
        video_filename = video_path.name
        video_source_html += f'    <source src="{video_filename}" type="video/{video_format}">\n'
    
    video_html = video_html.replace('<!-- Video sources will be added dynamically -->', video_source_html)
    
    with open(Path(temp_dir) / "video.html", "w") as f:
        f.write(video_html)
    
    with open(Path(temp_dir) / "animation.html", "w") as f:
        f.write(html_templates.ANIMATION_HTML)
    
    with open(Path(temp_dir) / "jscomputation.html", "w") as f:
        f.write(html_templates.JS_COMPUTATION_HTML)
    
    with open(Path(temp_dir) / "index.html", "w") as f:
        f.write("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Browser Power Test</title>
            <meta http-equiv="refresh" content="0; url=video.html">
        </head>
        <body>
            <p>Redirecting to <a href="video.html">video test</a>...</p>
        </body>
        </html>
        """)
    
    os.chdir(temp_dir)
    
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", VIDEO_SERVER_PORT), handler)
    
    log_message(f"Starting HTTP server at port {VIDEO_SERVER_PORT}")
    
    thread = threading.Thread(target=httpd.serve_forever)
    thread.daemon = True
    thread.start()
    
    return httpd, temp_dir