# coding: utf-8
from sqlalchemy import ARRAY, Boolean, CheckConstraint, Column, Float, Integer, String, Table, Text, text
from geoalchemy2.types import Geometry
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


t_geography_columns = Table(
    'geography_columns', metadata,
    Column('f_table_catalog', String),
    Column('f_table_schema', String),
    Column('f_table_name', String),
    Column('f_geography_column', String),
    Column('coord_dimension', Integer),
    Column('srid', Integer),
    Column('type', Text)
)


t_geometry_columns = Table(
    'geometry_columns', metadata,
    Column('f_table_catalog', String(256)),
    Column('f_table_schema', String),
    Column('f_table_name', String),
    Column('f_geometry_column', String),
    Column('coord_dimension', Integer),
    Column('srid', Integer),
    Column('type', String(30))
)


class Hpms2016MajorRoad(Base):
    __tablename__ = 'hpms2016_major_roads'

    gid = Column(Integer, primary_key=True)
    route_id = Column(String)
    through_lanes = Column(Integer)
    lane_width = Column(Integer)
    aadt = Column(Integer)
    fips = Column(String(5))
    roadtype = Column(String(2))
    speed = Column(Integer)
    geom = Column(Geometry, index=True)


t_raster_columns = Table(
    'raster_columns', metadata,
    Column('r_table_catalog', String),
    Column('r_table_schema', String),
    Column('r_table_name', String),
    Column('r_raster_column', String),
    Column('srid', Integer),
    Column('scale_x', Float(53)),
    Column('scale_y', Float(53)),
    Column('blocksize_x', Integer),
    Column('blocksize_y', Integer),
    Column('same_alignment', Boolean),
    Column('regular_blocking', Boolean),
    Column('num_bands', Integer),
    Column('pixel_types', ARRAY(Text())),
    Column('nodata_values', ARRAY(Float(precision=53))),
    Column('out_db', Boolean),
    Column('extent', Geometry),
    Column('spatial_index', Boolean)
)


t_raster_overviews = Table(
    'raster_overviews', metadata,
    Column('o_table_catalog', String),
    Column('o_table_schema', String),
    Column('o_table_name', String),
    Column('o_raster_column', String),
    Column('r_table_catalog', String),
    Column('r_table_schema', String),
    Column('r_table_name', String),
    Column('r_raster_column', String),
    Column('overview_factor', Integer)
)


class SpatialRefSy(Base):
    __tablename__ = 'spatial_ref_sys'
    __table_args__ = (
        CheckConstraint('(srid > 0) AND (srid <= 998999)'),
    )

    srid = Column(Integer, primary_key=True)
    auth_name = Column(String(256))
    auth_srid = Column(Integer)
    srtext = Column(String(2048))
    proj4text = Column(String(2048))


class TlRoad(Base):
    __tablename__ = 'tl_roads'

    gid = Column(Integer, primary_key=True, server_default=text("nextval('tl_roads_gid_seq'::regclass)"))
    linearid = Column(String(22))
    fullname = Column(String(100))
    rttyp = Column(String(1))
    mtfcc = Column(String(5))
    geom = Column(Geometry('MULTILINESTRING', 4269), index=True)
