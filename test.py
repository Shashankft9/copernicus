from pyorbital.orbital import Orbital
from datetime import datetime, timedelta
import folium
# PYORBITAL DOCUMENTATION
# https://pyorbital.readthedocs.io/en/latest/
# PyOrbital get_position and get_lonlatalt cases
# Use current TLEs from Celestrak: http://celestrak.com/NORAD/elements/

# SATELLITE
sat = "SENTINEL-3A"

#orb = Orbital('SENTINEL-3A', tle_file='./EO_Sat.txt')
orb = Orbital(sat)

now = datetime.utcnow()

# Get position and velocity of the satellite:
print(orb.get_position(now, normalize=False))

# Get longitude, latitude and altitude of the satellite:
print(orb.get_lonlatalt(now))

# Create a new Map centered on position [0,0]
m = folium.Map(location=[10, 0],zoom_start = 1)

# Function to get position with a deltatime from now(). (Default deltatime is 0)
def getsatpos(DeltaTiming=0):
    now = datetime.utcnow() + timedelta(seconds = DeltaTiming)

    # Get longitude, latitude and altitude of the satellite:
    lon,lat,alt = orb.get_lonlatalt(now)
    return(lat,lon)
    
# Function to get an orbit over an specified period of time. (Default period is 101 min)
def getoneorbit(period=6060):
    prd = period/2
    orbital = []
    orbit = []
    alt_lon = 0
    for t in range(-int(prd),int(prd)):
        lat,lon = getsatpos(t)
        # Divide orbit in two multilines at transition from lon -180 to lon 180.
        if (abs(alt_lon-lon)) > 359: 
            orbital.append(orbit)
            orbit = []
        orbit.append(getsatpos(t))
        alt_lon = lon

    orbital.append(orbit)
    return orbital
    
orbits = getoneorbit(13000)
# Set an satellite Icon and set position for the icon at time=now()
sat_icon = folium.features.CustomIcon("./S3_small.png",icon_size=(30, 30))
lon_marker,lat_marker,alt = orb.get_lonlatalt(now)
# Create Satellite position Marker
folium.Marker([lat_marker,lon_marker], popup="<i>" + sat + "</i>", tooltip=sat, icon=sat_icon).add_to(m)
# Create multiline with all segments of the orbit between lon -180 and 180
for orb_single in orbits:
    my_PolyLine=folium.PolyLine(locations=orb_single,weight=5)
    m.add_child(my_PolyLine)   
# Plot map with all elements
m.save("index.html")
