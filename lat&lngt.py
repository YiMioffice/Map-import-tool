from math import radians, sin, cos, sqrt, atan2
from flask import Flask, request
import ast
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        arg1 = request.form.get('arg1')
        arg2_text = request.form.get('arg2')
        locations = ast.literal_eval(arg2_text)
        input_location = list(map(float, arg1.split(',')))
        locations = [[float(coord) for coord in loc] for loc in locations]
        nearest_location = find_nearest_location(input_location[0], input_location[1], locations)
        return 'The nearest location is: {},{}'.format(nearest_location[0], nearest_location[1])
    return '''
        <form method="post">
            <label for="arg1">输入标记经纬度（格式：纬度,经度）</label>
            <input type="text" id="arg1" name="arg1"><br><br>
            <label for="arg2">输入路线标记数组(lat.mikuos.com上输出的数组)</label>
            <textarea id="arg2" name="arg2" rows="5" cols="50"></textarea><br><br>
            <input type="submit" value="Submit">
        </form>
    '''

def distance(lat1, lon1, lat2, lon2):
    R = 6371e3  
    lat1_rad, lat2_rad = radians(lat1), radians(lat2)
    delta_lat = radians(lat2 - lat1)
    delta_lon = radians(lon2 - lon1)
    a = sin(delta_lat / 2) * sin(delta_lat / 2) + cos(lat1_rad) * cos(lat2_rad) * sin(delta_lon / 2) * sin(delta_lon / 2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def find_nearest_location(lat, lon, locations):
    min_dist = float('inf')
    nearest_location = None
    for location in locations:
        dist = distance(lat, lon, location[0], location[1])
        if dist < min_dist:
            min_dist = dist
            nearest_location = location
    return nearest_location

if __name__ == '__main__':
    app.run(debug=False)
    app.run(host='0.0.0.0', port=8000)
