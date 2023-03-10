from flask import Flask, jsonify
from flask_cors import CORS
from bson.son import SON
from pymongo import MongoClient
import random
app = Flask(__name__)
app.secret_key=  b't\x08\xe3u\x12\x93\xc5r\xf2\xa9;\xb7|@\x003'
app.config['TEMPLATES_AUTO_RELOAD'] = True  
CORS(app)

client = MongoClient("mongodb+srv://lightitupsfhmmy:CusRl1o8V9yWyZ9W@cluster0.bwo4ond.mongodb.net/?retryWrites=true&w=majority")
db = client.LightItUp






@app.route('/', methods=['GET'])
def home():
    lat_min = 37.937497
    lon_min = 23.639687
    lat_max = 38.001657
    lon_max = 23.963229
    coords_list = []
    for _ in range(10000):
        lat = random.uniform(lat_min, lat_max)
        long = random.uniform(lon_min, lon_max)
        traffic = random.randint(0,2)
        coords_list.append({"type":"Point",'coordinates':[long, lat],'traffic':traffic})
    db.light.insert_many(coords_list)
    return '<h1>Hello World</h1>'


def to_geoJson(json_data):
    print(json_data[0]['type'])
    geoJson = {
        'type':'FeatureCollection',
        'features':[{
        
        'type':'Feature',
        'properties': {
        'traffic':i['traffic']
        },
        'geometry':{
        'type':i['type'],
        'coordinates':i['coordinates'] 
        }}
         for i in json_data]
    }
    return geoJson


@app.route('/get-traffic/', methods=['GET'])
def get_traffic():
    #   this query finds nearest coordinates to the point:
    #   long = 23.727539, lat = 37.983810
    max_distance = 1000
    latitude = 37.983810
    longitude = 23.727539
    query = {'coordinates': {'$near': SON([('$geometry', SON([('type', 'Point'), ('coordinates', [longitude, latitude])])), ('$maxDistance', max_distance)])}}
    # query = {}
    traffic_data = db.light.find(query, {'_id': 0})
    return jsonify(to_geoJson(list(traffic_data)))
