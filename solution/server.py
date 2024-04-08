from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class Charter:
    def __init__(self):
        self.id = None
        self.name = None
        self.level = None
        self.role = None
        self.charisma = None
        self.strength = None
        self.dexterity = None

    def __str__(self):
        return f"name: {self.name}, level: {self.level}, role: {self.role}, charisma: {self.charisma}, strength: {self.strength}, dexterity: {self.dexterity}"

class CharterBuilder:
    def __init__(self):
        self.charter = Charter()

    def set_name(self, name):
        self.charter.name = name

    def set_level(self, level):
        self.charter.level = level

    def set_role(self, role):
        self.charter.role = role

    def set_charisma(self, charisma):
        self.charter.charisma = charisma

    def set_strength(self, strength):
        self.charter.strength = strength

    def set_dexterity(self, dexterity):
        self.charter.dexterity = dexterity

    def get_charter(self):
        return self.charter

class Player:
    def __init__(self, builder):
        self.builder = builder

    def create_charter(self, name, level, role, charisma, strength, dexterity):
        self.builder.set_name(name)
        self.builder.set_level(level)
        self.builder.set_level(role)
        self.builder.set_level(charisma)
        self.builder.set_level(strength)
        self.builder.set_level(dexterity)
        return self.builder.get_charter()

class CharterCreator:
    def __init__(self):
        self.builder = CharterBuilder()
        self.player = Player(self.builder)

    def handle_post_request(self, post_data):
        name = post_data.get('name', None)
        level = post_data.get('level', None)
        role = post_data.get('role', None)
        charisma = post_data.get('charisma', None)
        strength = post_data.get('strength', None)
        dexterity = post_data.get('dexterity', None)

        charter = self.player.create_charter(name, level, role, charisma, strength, dexterity)

        return {
            'name': charter.name,
            'level': charter.level,
            'role': charter.role,
            'charisma': charter.charisma,
            'strength': charter.strength,
            'dexterity': charter.dexterity,
        }

class HTTPDataHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))
    @staticmethod
    def handle_reader(handler):
        content_length = int(handler.headers['Content-Length'])
        post_data = handler.rfile.read(content_length)
        return json.loads(post_data.decode('utf-8'))
    
class CharterHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.controller = CharterCreator()
        super().__init__(*args, **kwargs)
        
    def do_POST(self):
        if self.path == '/charter':
            
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.controller.handle_post_request(data)
            
            HTTPDataHandler.handle_response(self, 201, response_data)
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})


def run(server_class=HTTPServer, handler_class=CharterHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Iniciando servidor HTTP en puerto {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
