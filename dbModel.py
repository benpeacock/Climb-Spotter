from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base();
from sqlalchemy import Column, Integer, String, VARCHAR, Text, Date, DATETIME, DECIMAL, CHAR, INTEGER, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import Table

user_role_table = Table('user_role', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.user_id')),
    Column('role_id', Integer, ForeignKey('role.role_id'))
)

area_relationship_table = Table('area_relationship', Base.metadata,
    Column('ancestor', Integer, ForeignKey('area.area_id')),
    Column('descendent', Integer, ForeignKey('area.area_id'))
)

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

    roles = relationship("DbRole", secondary = user_role_table, backref="users")

class DbRole(Base):

    __tablename__ = 'role'
    role_id = Column(INTEGER, primary_key = True)
    name = Column(VARCHAR(25))
    privileges = relationship('DbRolePrivilege')

class DbPrivilege(Base):

    __tablename__ = 'privilege'
    privilege_id = Column(INTEGER, primary_key = True)
    name = Column(VARCHAR(25))

class DbRolePrivilege(Base):

    __tablename__ = 'role_privilege'
    role_id = Column(INTEGER, ForeignKey('role.role_id'), primary_key = True)
    privilege_id = Column(INTEGER, ForeignKey('privilege.privilege_id'), primary_key = True)

class DbArea(Base):

    __tablename__ = 'area'

    area_id = Column(Integer, primary_key = True)
    name = Column(VARCHAR(50))
    created = Column(DATETIME)
    latitude = Column(DECIMAL(10, 6))
    longitude = Column(DECIMAL(10, 6))

#    routes = relationship("DbRoute")

#    rs = relationship('DbRoute', secondary = area_relationship_table,
#        primaryjoin = area_id == area_relationship_table.c.ancestor,
#        secondaryjoin = "DbRoute.area_id == area_relationship_table.c.descendent")
#        foreign_keys=[area_relationship_table.c.descendent, area_relationship_table.c.ancestor])

#    tmp = relationship('DbRoute', primaryjoin = "DbArea.area_id == DbRoute.area_id")

    descendents = relationship('DbArea', backref = 'ancestors', secondary = area_relationship_table,
        primaryjoin = area_id == area_relationship_table.c.ancestor,
        secondaryjoin = area_id == area_relationship_table.c.descendent)

class DbRoute(Base):

    __tablename__ = 'route'

    route_id = Column(Integer, primary_key = True)
    area_id = Column(Integer, ForeignKey('area.area_id'))
    name = Column(VARCHAR(50))
    created = Column(DATETIME)

    area = relationship("DbArea")

    areas = relationship('DbArea', backref = backref('routes', order_by = 'DbRoute.name'),
        secondary = area_relationship_table,
        primaryjoin = area_id == area_relationship_table.c.descendent,
        secondaryjoin = DbArea.area_id == area_relationship_table.c.ancestor,
        innerjoin = True, order_by = DbArea.name,
        foreign_keys=[area_relationship_table.c.ancestor, area_relationship_table.c.descendent])

class DbRouteWork(Base):

    __tablename__ = 'route_work'

    route_work_id = Column(Integer, primary_key = True)
    route_id = Column(Integer, ForeignKey('route.route_id'))
    user_id = Column(Integer, ForeignKey('user.user_id'))
    who = Column(VARCHAR(100))
    work_date = Column(Date)
    bolts_placed = Column(Integer)
    anchor_replaced = Column(Integer)
    new_anchor = Column(Integer)
    created = Column(DATETIME)
    info = Column(VARCHAR(500))

    route = relationship('DbRoute', uselist = False, backref = 'route_work')
    notes = relationship('DbRouteWorkNote', order_by = 'DbRouteWorkNote.created')

class DbRouteWorkNote(Base):

    __tablename__ = 'route_work_note'

    route_work_note_id = Column(Integer, primary_key = True)
    route_work_id = Column(Integer, ForeignKey('route_work.route_work_id'))
    user_id = Column(Integer, ForeignKey('user.user_id'))
    note = Column(Text)
    created = Column(DATETIME)

class DbDeployScript(Base):

    __tablename__ = 'deploy_script'
    path = Column(VARCHAR(150), primary_key = True)
    start = Column(DATETIME)
    end = Column(DATETIME)


#class DbUserRole(Base):

#    __tablename__ = 'user_role'
#    user_id = Column(INTEGER, primary_key = True)
#    role_id = Column(INTEGER, primary_key = True)

#    user = relationship('DbUser', uselist = False, backref = 'user')
#    role = relationship('DbRole', uselist = False, backref = 'role')

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
