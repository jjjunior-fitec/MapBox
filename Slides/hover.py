import json
import os


def read_json(fileName):
    try:
        arquivo_json = open(fileName + '.json', 'r')
        dados_json = json.load(arquivo_json)
        return dados_json
    except:
        return {}

def create_json(fileName, data):
        
    data_dic = read_json(fileName)
    if (data_dic != {}):
        return "The JSON file" + fileName + "already exists, please insert a different name."
    
    data_dic = json.dumps((data), indent=4, sort_keys=False)

    arquivo_json = open(fileName + '.json', 'w')
    arquivo_json.write(data_dic)
    arquivo_json.close
    return

def latlongToDict(array):
    _list = []
    _id = 0
    for x in range(0, len(array), 2):
        _list.append([float(array[x]), float(array[x+1])])
        _id = _id + 1
    return _list


def findTalhao(features, filename):
    for i in range(len(features)):
        if features[i]["properties"]["TALHAO_NAME"] == filename:
            return True, i
    return False, len(features)


def getCoord(filename, path):
    data = open(path + filename, "r").read().split(',')
    return latlongToDict(data)


def geoJsonFy(path, jsonFileName):

    filenames = os.listdir(path)
    filenames.sort()
    GeoJson = {"type": "FeatureCollection", "features": []}

    id = 0
    for file in range(len(filenames)):

        coord = []
        geometry = "Polygon"
        hasMultTalhao = False
        idMultTalhao = 0
        filename = filenames[file]

        if(filenames[file].split('.')[-1] == "txt"):
            if(filenames[file].split('_')[-1] in ["top.txt", "bottom.txt", "left.txt", "right.txt"]):
                #print(filename, "_sub pass")
                filename = filenames[file].split('_')[0]
                hasMultTalhao, idMultTalhao = findTalhao(
                    GeoJson["features"], filename)
                if (hasMultTalhao):
                    #print(filename, hasMultTalhao)
                    coord = GeoJson['features'][idMultTalhao]["geometry"]["coordinates"]
                    if (GeoJson['features'][idMultTalhao]["geometry"]["type"] == "Polygon"):
                        coord = [coord]
                        GeoJson['features'][idMultTalhao]["geometry"]["type"] = "MultiPolygon"
                    coord.append( [getCoord(filenames[file], path)] )
                    id = id - 1
                else:
                    coord.append( getCoord(filenames[file], path) )

            else:
                coord.append(getCoord(filenames[file], path))
                filename = filenames[file].split('.')[0]

            if (hasMultTalhao):
                GeoJson['features'][idMultTalhao]["geometry"]["coordinates"] = coord

            else:
                GeoJson['features'].append( {"type": "Feature",
                                           "geometry": {"type": geometry,
                                           "coordinates": coord},
                                           "properties": {
                                               "TALHAO_ID": str(id),
                                               "TALHAO_NAME": filename},
                                           "id": id} )
            #print(filename,id)
            id = id + 1
    create_json(jsonFileName, GeoJson)
    return
