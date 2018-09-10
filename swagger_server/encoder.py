from connexion.apps.flask_app import FlaskJSONEncoder
import six

#from models.base_model_ import Model
from swagger_server.models.models import Hpms2016MajorRoad


class JSONEncoder(FlaskJSONEncoder):
    include_nulls = False

    def default(self, o):
        if isinstance(o, Hpms2016MajorRoad):
            dikt = {}
            for attr, _ in six.iteritems(o.swagger_types):
                value = getattr(o, attr)
                if value is None and not self.include_nulls:
                    continue
                attr = o.attribute_map[attr]
                dikt[attr] = value
            return dikt
        return FlaskJSONEncoder.default(self, o)
