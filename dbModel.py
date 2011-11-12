from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base();
from sqlalchemy import Column, Integer, String, VARCHAR, Text, Date, DATETIME, DECIMAL, CHAR, INTEGER, ForeignKey
from sqlalchemy.orm import relationship, backref

class DbUser(Base):

    __tablename__ = 'user'

    user_id = Column(INTEGER, primary_key = True)
    created = Column(DATETIME)
    last_login = Column(DATETIME)
    username = Column(VARCHAR(30))
    password = Column(CHAR(40))
    email = Column(VARCHAR(100))
    active = Column(INTEGER)
    display_name = Column(VARCHAR(30))

class DbRole(Base):

    __tablename__ = 'role'
    role_id = Column(INTEGER, primary_key = True)
    name = Column(VARCHAR(25))

class DbPrivilege(Base):

    __tablename__ = 'privilege'
    privilege_id = Column(INTEGER, primary_key = True)
    name = Column(VARCHAR(25))

class DbRolePrivilege(Base):

    __tablename__ = 'role_privilege'
    role_id = Column(INTEGER, primary_key = True)
    privilege_id = Column(INTEGER, primary_key = True)

class DbUserRole(Base):

    __tablename__ = 'user_role'
    user_id = Column(INTEGER, primary_key = True)
    role_id = Column(INTEGER, primary_key = True)

#
#class MpArea(Base):
#
#    __tablename__ = 'mp_area'
#
#    area_code = Column(Integer, ForeignKey('area.mp_code'), primary_key = True)
#    name = Column(String)
#    parent_code = Column(Integer)
#    latitude = Column(String)
#    longitude = Column(String)
#    url = Column(String)
#    routes = Column(Integer)
#    path = Column(String)
#    depth = Column(Integer)
#    geo_areas = Column(Integer)
#    in_cw = Column(Integer)
#    views = Column(Integer)
#
#    area = relationship('Area', uselist = False, backref = 'area')
#
#class State(Base):
#
#    __tablename__ = 'state'
#    state_id = Column(INTEGER, primary_key = True)     
#    name = Column(VARCHAR(100))
#    state_code = Column(VARCHAR(5))  
#    gmap_lat = Column(VARCHAR(25)) 
#    gmap_long = Column(VARCHAR(25)) 
#    gmap_zoom = Column(INTEGER)
#    sw_latitude = Column(DECIMAL(8,5))
#    sw_longitude = Column(DECIMAL(8,5))
#    ne_latitude = Column(DECIMAL(8,5))
#    ne_longitude = Column(DECIMAL(8,5))
#    aspect_ratio = Column(DECIMAL(5,3))
#
#class Area(Base):
#
#    __tablename__ = 'area'
#
#    area_id = Column(INTEGER, primary_key=True)
#    name = Column(VARCHAR(100))
#    latitude = Column(DECIMAL(10,6))
#    longitude = Column(DECIMAL(10,6))
#    state_code = Column(CHAR(2))
#    city = Column(VARCHAR(100))
#    mp_code = Column(VARCHAR(50))
#    mp_abbr = Column(VARCHAR(50))
#    elevation = Column(VARCHAR(25))
#    data_last_updated = Column(DATETIME)
#    description = Column(Text)
#    show_weather = Column(INTEGER)
#    area_size_id = Column(INTEGER)
#    rc_url = Column(VARCHAR(255))
#    wikipedia_tag = Column(VARCHAR(100))
#    drtopo_url = Column(VARCHAR(150))
#    front_page = Column(INTEGER)
#    clim81_station_id = Column(INTEGER)
#    clim81_station_distance = Column(INTEGER)
#    zip_code = Column(VARCHAR(5))
#    zip_code_indexed = Column(INTEGER)
#    gmt_offset = Column(INTEGER)
#    name_search = Column(VARCHAR(50))
#    video_count = Column(INTEGER)
#    photo_count = Column(INTEGER)
#    user_id = Column(INTEGER)
#    setup_log = Column(Text)
#    setup = Column(DATETIME)
#    created = Column(DATETIME)
#    pageview = Column(INTEGER)
#    favorite = Column(INTEGER)
#    rank = Column(INTEGER)
#    widget = Column(INTEGER)
#    api = Column(INTEGER)
#
#    mp_area = relationship('MpArea', uselist = False, backref = 'mp_area')
