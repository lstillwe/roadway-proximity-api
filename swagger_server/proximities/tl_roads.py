import sys
from configparser import ConfigParser
from sqlalchemy import extract, func, cast
from geoalchemy2 import Geography

from swagger_server.controllers import Session
from flask import jsonify
from swagger_server.models.models import TlRoad
from enum import Enum


class MeasurementType(Enum):
    # lat: 0 to +/- 90, lon: 0 to +/- 180 as lat,lon

    LATITUDE = '^[+-]?(([1-8]?[0-9])(\.[0-9]+)?|90(\.0+)?)$'
    LONGITUDE = '^[+-]?((([1-9]?[0-9]|1[0-7][0-9])(\.[0-9]+)?)|180(\.0+)?)$'

    def isValid(self, measurement):
        import re
        if re.match(self.value, str(measurement)) is None:
            return False
        else:
            return True


parser = ConfigParser()
parser.read('swagger_server/ini/connexion.ini')
sys.path.append(parser.get('sys-path', 'proximities'))
sys.path.append(parser.get('sys-path', 'controllers'))

# Return the geometry of line between station and closest point on road network
		#for row in session.query(Stations.pkey.label('station'), 
			#Roads.gid.label('road'), 
			#make_link_line(Stations.the_geom, Roads.the_geom).\
				#label('the_geom')).\
			#order_by(Stations.pkey, 
				#func.ST_Distance(Roads.the_geom, Stations.the_geom)).\
			#distinct(Stations.pkey):
			# 
			 #print row.station, row.road, row.the_geom


class TLRoadProximity(object):

    def validate_parameters(self, **kwargs):
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == 'latitude':
                    if not MeasurementType.LATITUDE.isValid(value):
                        return False, ('Invalid parameter', 400, {'x-error': 'Invalid parameter: ' + key})
                elif key == 'longitude':
                    if not MeasurementType.LONGITUDE.isValid(value):
                        return False, ('Invalid parameter', 400, {'x-error': 'Invalid parameter: ' + key})
                else:
                    return True, ''
        else:
            return False, ('Invalid parameters', 400, {'x-error': 'No parameters provided'})


    def get_values(self, **kwargs):
        # latitude, logitude, limit_distance=500

        # validate input from user
        is_valid, message = self.validate_parameters(**kwargs)
        if not is_valid:
            return message

        lat = kwargs.get('latitude')
        lon = kwargs.get('longitude')
        limit = kwargs.get('limit_distance')

        # create data object
        data = {}
        session = Session()
        
        # select fullname, rttyp, st_distancesphere(geom, ST_GeomFromText('POINT(-72.1235 42.3521)', 4269)) as distance from TlRoad where st_dwithin(geom::geography, ST_SetSRID(ST_MakePoint(-72.1235, 42.3521),4269)::geography, 800) order by distance, rttyp;
        query = "select fullname, rttyp, st_distancesphere(geom, ST_GeomFromText('POINT(" + str(lon) + " " + str(lat) + ")',4269)) as distance from tl_roads where st_dwithin(geom::geography, ST_SetSRID(ST_MakePoint(" + str(lon) + ", " + str(lat) + "),4269)::geography," + str(limit) + ") order by distance, rttyp DESC"

        result = session.execute(query)
        #dist_func = func.ST_Distancesphere(TlRoad.geom, func.ST_GeomFromText('POINT(-72.1235 42.3521)', 4269)).label('distance')
        #result = session.query(TlRoad.fullname,
                               #TlRoad.rttyp,
                               #dist_func) \
                        #.filter(func.ST_DWithin(cast(TlRoad.geom, Geography),
                                                #cast(func.ST_SetSRID(func.ST_MakePoint(-72.1235, 42.3521), 4269), Geography), 800))
                        #.order_by('distance', TlRoad.rttyp)

        for query_return_values in result:

            data.update({'name': query_return_values[0],
                         'type': query_return_values[1],
                         'latitude': kwargs.get('latitude'),
                         'longitude': kwargs.get('longitude'),
                         'distance': query_return_values[2]})
            break
        session.close()

        return jsonify(data)
