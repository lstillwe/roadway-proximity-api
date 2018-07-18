#import connexion
#import six
import sys

#from swagger_server.models.roadway_data import RoadwayData  # noqa: E501
from swagger_server.models.models import TlRoad  # noqa: E501
from swagger_server import util

from configparser import ConfigParser
from sqlalchemy import exists, or_, func

from swagger_server.controllers import Session
from flask import jsonify

parser = ConfigParser()
parser.read('swagger_server/ini/connexion.ini')
sys.path.append(parser.get('sys-path', 'proximities'))
sys.path.append(parser.get('sys-path', 'controllers'))

def get_distance(latitude, longitude, limit_distance=None):  # noqa: E501
    """retrieves distance

    By passing in the appropriate options, you can get the distance to the closest roadway  # noqa: E501

    :param latitude: latitude of point from which to retrieve the closest distance to a roadway (decimal format - WGS84 assumed)
    :type latitude: float
    :param longitude: longitude of point from which to retrieve the closest distance to a roadway (decimal format - WGS84 assumed)
    :type longitude: float
    :param limit_distance: limit the search distance - provide number in meters
    :type limit_distance: float

    :rtype: RoadwayData
    """

    
    session = Session()
    #variable = "".join(variable.split()).lower()
    #lat_lon = "".join(lat_lon.split())
    #var_set = variable.split(';')
    #for var in var_set:
        #if not session.query(exists().where(ExposureList.variable == var)).scalar():
            #return 'Invalid parameter', 400, {'x-error': 'Invalid parameter: variable'}
    #session.close()
    from swagger_server.proximities.tl_roads import TLRoadProximity
    roads = TLRoadProximity()
    kwargs = locals()
    data = roads.get_values(**kwargs)

    return data
