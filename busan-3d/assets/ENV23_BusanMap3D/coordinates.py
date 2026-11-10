"""VERSION v1.0. Local tangent-plane approximation; inputs must be supplied by the user."""
import math,json
from pathlib import Path
EARTH_RADIUS_M=6371008.8  # approximation setting; not a surveyed map projection
METERS_PER_UNIT=10000.0  # FACTS design setting: 1m model=10km real
HEIGHT_EXAGGERATION=3.0
def latlon_to_xy(lat,lon,origin_lat,origin_lon,altitude_m=0):
    if not (-90<=lat<=90 and -90<=origin_lat<=90 and -180<=lon<=180 and -180<=origin_lon<=180):raise ValueError('invalid coordinates')
    east=math.radians(lon-origin_lon)*EARTH_RADIUS_M*math.cos(math.radians(origin_lat))
    north=math.radians(lat-origin_lat)*EARTH_RADIUS_M
    return east/METERS_PER_UNIT,-north/METERS_PER_UNIT,altitude_m*HEIGHT_EXAGGERATION/METERS_PER_UNIT
def load_pins(path=None):
    data=json.loads(Path(path or Path(__file__).with_name('pins.json')).read_text())
    if not data['pins']:return []
    if data.get('origin') is None:raise ValueError('origin latitude and longitude required')
    return [(p['id'],latlon_to_xy(p['lat'],p['lon'],*data['origin'],p.get('altitude_m',0))) for p in data['pins']]
def build_route(points,steps_per_segment=24):
    if steps_per_segment<1:raise ValueError('positive steps required')
    if not points:return []
    if len(points)==1:return [tuple(points[0])]
    out=[]
    for a,b in zip(points,points[1:]):
        for k in range(steps_per_segment):
            t=k/steps_per_segment;out.append(tuple(a[i]*(1-t)+b[i]*t for i in range(3)))
    return out+[tuple(points[-1])]
if __name__=='__main__':
    assert latlon_to_xy(0,0,0,0)==(0.,-0.,0.)
    assert latlon_to_xy(.01,0,0,0)[1]<0
    assert latlon_to_xy(0,.01,0,0)[0]>0
    assert latlon_to_xy(0,0,0,0,100)[2]==.03
    assert build_route([(0,0,0),(1,2,3)])[-1]==(1,2,3)
    assert load_pins()==[]
    print('MAP_SELFTEST PASS; no invented coordinates')
