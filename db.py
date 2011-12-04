from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import CsConfiguration

_engine = None
_session = None

def engine():

    global _engine
    if _engine == None:
       
        c = CsConfiguration.CsConfiguration()
        username = c.settings['database']['username']
        password = c.settings['database']['password']
        host = c.settings['database']['host']
        database = c.settings['database']['database']
        _engine = create_engine("mysql://{0}:{1}@{2}/{3}".format(username, password, host, database))
    return _engine

def session():

    global _session, engine
    if _session == None:

        engine = engine()
        Session = sessionmaker(bind=engine)
        _session = Session()

    return _session
