import requests



url = "http://localhost:8000/charter"
headers = {'Content-type': 'application/json'}

my_charter = {
    "name": "Gandalf",
    "level": "10",
    "role": "Wizzard",
    "charisma": "15",
    "strength": "10",
    "dexterity": "10",
}

response = requests.post(url, json=my_charter, headers=headers)
print(response.json())

response = requests.get(url + "?role=archer", headers=headers)
data = response.json()

print("Lista de personajes con el rol 'archer':")
for character in data:
    print(f"Nombre: {character['name']}, Nivel: {character['level']}, Rol: {character['role']}, Carisma: {character['charisma']}, Fuerza: {character['strength']}, Destreza: {character['dexterity']}")
