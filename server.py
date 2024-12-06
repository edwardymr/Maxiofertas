import json
import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer

HOST = "localhost"
PORT = 8000

class ShoppingCartHandler(BaseHTTPRequestHandler):

    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json" if self.path == "index" else "text/html")
        self.end_headers()

    def do_GET(self):
        if self.path == "/":
            self._set_headers()
            with open("index.html", "r") as file:
                self.wfile.write(file.read().encode())
        elif self.path == "index":
            self._set_headers()
            conn = sqlite3.connect("db.sqlite3")
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, description, price, image_url FROM products")
            products = cursor.fetchall()
            conn.close()
            products_list = [
                {"id": row[0], "name": row[1], "description": row[2], "price": row[3], "image_url": row[4]}
                for row in products
            ]
            self.wfile.write(json.dumps(products_list).encode())
        else:
            self.send_error(404, "File Not Found")
    
    def do_POST(self):
        self.send_error(405, "Method Not Allowed")

if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), ShoppingCartHandler)
    print(f"Server running on http://{HOST}:{PORT}")
    server.serve_forever()