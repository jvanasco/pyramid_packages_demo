import pymongo
from gridfs import GridFS

def initialize_mongo_db( config, settings ):
    if ( 'mongodb_use' in settings ) and ( settings['mongodb_use'] == 'true' ):
        conn = pymongo.Connection( settings['mongodb_uri'] )
        config.registry.settings['mongodb_conn'] = conn
        config.add_subscriber(add_mongo_db, 'pyramid.events.NewRequest')


def add_mongo_db(event):
    settings = event.request.registry.settings
    db = settings['mongodb_conn'][settings['mongodb_name']]
    event.request.mongodb = db
    event.request.gridfs = GridFS(db)
