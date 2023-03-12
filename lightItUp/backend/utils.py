#   This function takes the query data and turns it to geoJson format
#   https://geojson.org/


def to_geoJson(json_data):
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