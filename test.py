import math

def distance():
    lat1, lon1 = 28.339714, 77.319887
    lat2, lon2 = 28.715567, 77.100122
    radius = 6371 # km

    print(type(lat1))

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d

dis = distance()
print(dis)


districts = ['Lombardy', 'Non Valley']

districts_dict = {
    'Lombardy': {
        'latitude': 45.585556,
        'longitude': 9.930278,
    },
    'Non Valley': {
        'latitude': 46.337353,
        'longitude': 11.057293
    }
}

print(districts_dict['Lombardy'])
print(districts_dict['Lombardy']['latitude'])

if 'Non Valley' in districts_dict:
    print('Yes')
else:
    print('No')
