from flask import Flask, jsonify, request
from flask_cors import CORS
from bson.son import SON
from pymongo import MongoClient
import random
from utils import to_geoJson


app = Flask(__name__)
app.secret_key=  b't\x08\xe3u\x12\x93\xc5r\xf3\xa6;\xb7|@\x003'
app.config['TEMPLATES_AUTO_RELOAD'] = True  
CORS(app)

client = MongoClient("mongodb+srv://lightitupsfhmmy:CusRl1o8V9yWyZ9W@cluster0.bwo4ond.mongodb.net/?retryWrites=true&w=majority")
db = client.LightItUp






@app.route('/', methods=['GET'])
def home():
    return '<h1>Hello World</h1>'




@app.route('/get-traffic/', methods=['GET'])
def get_traffic():
    #   this query finds nearest coordinates to the point:
    #   long = 23.727539, lat = 37.983810
    max_distance = 3*1000
    latitude = 37.983810
    longitude = 23.727539
    query = {'coordinates': {'$near': SON([('$geometry', SON([('type', 'Point'), ('coordinates', [longitude, latitude])])), ('$maxDistance', max_distance)])}}
    # query = {}
    traffic_data = db.light.find(query, {'_id': 0})
    return jsonify(to_geoJson(list(traffic_data)))




@app.route('/update-light-traffic/', methods=['POST'])
def update_light_traffic():
    traffic_number = request.form.get('traffic')
    
    if not traffic_number or not traffic_number.isdigit():
        return "expected digit as traffic number"
    
    traffic_number = int(traffic_number)

    if traffic_number < 0 or traffic_number > 3:
        return "error: traffic number not within exprected limits"
    

    traffic_light_id = request.form.get('traffic_light_id')
    if not traffic_light_id:
        return "error: expected traffic light id"
    
    
    db.collection.update_one({"_id": traffic_light_id}, {"traffic": traffic_number})

    if traffic_number == 0:
        print("Green")
    if traffic_number == 1:
        print("Yellow")
    if traffic_number == 2:
        print("Red")    
    return '<h1>Completed Update</h1>'


# this route populates db with 10K random points near Athens.
# PLEASE DON'T ACCESS IT 
@app.route('/populate-database/', methods=['GET'])
def populate_db_random_points():
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
    return '<h1>Done</h1>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)