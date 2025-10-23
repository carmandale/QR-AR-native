#!/usr/bin/env python3
"""
Custom HTTP server with proper MIME types for AR content.
Serves USDZ, GLB, and other AR file formats with correct Content-Type headers.
"""

import http.server
import socketserver
import mimetypes
import os

# Register custom MIME types for AR content
mimetypes.add_type('model/vnd.usdz+zip', '.usdz')
mimetypes.add_type('model/vnd.reality', '.reality')
mimetypes.add_type('model/gltf-binary', '.glb')
mimetypes.add_type('model/gltf+json', '.gltf')

class ARHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom request handler with AR-specific MIME types."""

    def guess_type(self, path):
        """Override to use our custom MIME types."""
        base, ext = os.path.splitext(path)
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        ext = ext.lower()
        if ext in self.extensions_map:
            return self.extensions_map[ext]

        # Use mimetypes module for everything else
        guess = mimetypes.guess_type(path)[0]
        return guess or 'application/octet-stream'

    def end_headers(self):
        """Add CORS headers and cache control."""
        # CORS headers (for development)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')

        # Cache control for models (1 hour)
        if self.path.endswith(('.usdz', '.glb', '.gltf', '.reality')):
            self.send_header('Cache-Control', 'public, max-age=3600')

        super().end_headers()

if __name__ == '__main__':
    PORT = 8000
    DIRECTORY = "public"

    # Change to the public directory
    os.chdir(DIRECTORY)

    # Create server
    Handler = ARHTTPRequestHandler

    with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
        print(f"🚀 AR Content Server running at:")
        print(f"   Local:   http://localhost:{PORT}/")
        print(f"   Network: http://192.168.3.141:{PORT}/")
        print(f"\n📱 Serving from: {os.getcwd()}")
        print(f"\n✅ MIME types configured:")
        print(f"   .usdz    → model/vnd.usdz+zip")
        print(f"   .reality → model/vnd.reality")
        print(f"   .glb     → model/gltf-binary")
        print(f"   .gltf    → model/gltf+json")
        print(f"\n⏹️  Press Ctrl+C to stop\n")

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 Server stopped")
