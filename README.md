# PlantName — serveur sécurisé

Passerelle entre PlantName et Pl@ntNet.

## Installation
python -m venv .venv
pip install -r requirements.txt

## Clé secrète
Définir la variable d'environnement `PLANTNET_API_KEY` avec ta clé Pl@ntNet. Ne jamais mettre cette clé dans l'application mobile, GitHub ou un fichier public.

## Lancer
python server.py

## API
GET /health
POST /identify avec un champ multipart `image`.

Exemple de réponse:
{"name":"Hibiscus","scientificName":"Hibiscus rosa-sinensis","score":0.93}

## Production
Utiliser HTTPS, une authentification/rate-limit sur /identify, et conserver la clé uniquement côté serveur.
