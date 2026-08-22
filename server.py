import os
from flask import Flask, request, jsonify
import requests
app=Flask(__name__)
URL='https://my-api.plantnet.org/v2/identify/all'
@app.get('/health')
def health(): return jsonify(ok=True, service='PlantName API')
@app.post('/identify')
def identify():
    key=os.getenv('PLANTNET_API_KEY')
    if not key: return jsonify(error='PLANTNET_API_KEY is not configured'),500
    image=request.files.get('image')
    if not image: return jsonify(error='No image provided'),400
    if image.mimetype not in ('image/jpeg','image/png'): return jsonify(error='Only JPEG and PNG images are accepted'),400
    try:
        r=requests.post(URL,params={'api-key':key,'lang':'fr','nb-results':1},files={'images':(image.filename or 'plant.jpg',image.stream,image.mimetype)},data={'organs':'auto'},timeout=45)
        r.raise_for_status(); data=r.json(); result=data.get('results',[{}])[0]; species=result.get('species',{}); names=species.get('commonNames',[])
        return jsonify(name=(names[0] if names else data.get('bestMatch')),scientificName=species.get('scientificNameWithoutAuthor'),score=result.get('score'))
    except requests.HTTPError: return jsonify(error='Pl@ntNet rejected the request',details=r.text[:500]),r.status_code
    except requests.RequestException as e: return jsonify(error='Unable to contact Pl@ntNet',details=str(e)),502
if __name__=='__main__': app.run(host='0.0.0.0',port=int(os.getenv('PORT','8080')))
