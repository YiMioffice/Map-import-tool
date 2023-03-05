from flask import Flask, request
import requests
import json
from geopy.distance import geodesic
from chinacoordtran import gcj02towgs84

gcj02towgs84Instance = gcj02towgs84()
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        arg1 = request.form['arg1']
        arg2 = request.form['arg2']
        
        # 起点
        url1 = "https://apis.map.qq.com/ws/geocoder/v1/"
        params = {
            "address": arg1,
            "key": "填入腾讯地图key"
        }
        response = requests.get(url1, params=params)
        data = json.loads(response.text)
        lng = data["result"]["location"]["lng"]
        lat = data["result"]["location"]["lat"]
        location1 = f"{lng},{lat}"
        
        # 终点
        url2 = "https://apis.map.qq.com/ws/geocoder/v1/"
        params = {
            "address": arg2,
            "key": "填入腾讯地图key"
        }
        response = requests.get(url2, params=params)
        data = json.loads(response.text)
        lng1 = data["result"]["location"]["lng"]
        lat1 = data["result"]["location"]["lat"]
        location2 = f"{lng1},{lat1}"
        origin = location1
        destination = location2
        
        url3 = "https://restapi.amap.com/v3/direction/driving?key=填入高德地图的key&origin={}&destination={}&originid=&destinationid=&extensions=all&strategy=0&waypoints=&avoidpolygons=&avoidroad=".format(origin, destination)
        response = requests.get(url3)
        out_json = json.loads(response.content)
        all_list = []
        for b in range(len(out_json["route"]["paths"][0]["steps"])):
            one_list = out_json["route"]["paths"][0]["steps"][b]["polyline"].split(";")
            for a in range(len(one_list)):
                tmp_list = []
                two_list = one_list[a].split(",")
                tmp_list.append(float(two_list[0]))
                tmp_list.append(float(two_list[1]))
                all_list.append(tmp_list)
        
        def remove_duplicate_arrays(arrays_list):
            unique_arrays = []
            for array in arrays_list:
                if array not in unique_arrays:
                    unique_arrays.append(array)
            return unique_arrays
        
        arrays_list = all_list
        unique_arrays = remove_duplicate_arrays(arrays_list)
        input_arr = unique_arrays
        output_arr = []
        for arr in input_arr:
            new_arr = [arr[1], arr[0]]
            output_arr.append(new_arr)
        result=str(output_arr)
        return 'The result is: {}'.format(result)
    
    return '''
        <form method="post">
            <label for="arg1">起点:</label>
            <input type="text" id="arg1" name="arg1"><br><br>
            <label for="arg2">终点:</label>
            <input type="text" id="arg2" name="arg2"><br><br>
            <input type="submit" value="Submit">
        </form>
    '''
#Ver 1.0.1
if __name__ == '__main__':
    app.run(debug=False)
