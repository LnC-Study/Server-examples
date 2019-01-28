import pymongo, config, datetime
from SingletonCreator import SingletonCreater
from CustomLogger import CustomLogger

class DatabaseManager(SingletonCreater):
    client = pymongo.MongoClient(host=config.DATABASE['HOST'],
                                 port=config.DATABASE['PORT'])
    database = client[config.DATABASE['DB_NAME']]
    # logger = Logger().get_logger()

    def create_index_on_database(cls):
        pass

    def get_data_from_collection(cls, _collection, _query):
        assert (cls.database[_collection])
        return cls.database[_collection].find( _query)

    def add_data_in_collection(cls, _collection, _data):
        assert (cls.database[_collection])

        if type(_data) is list:
            result = cls.database[_collection].insert_many( _data)
        else:
            result = cls.database[_collection].insert_one(_data)

    def delete_data_in_collection(cls, _collection, _query):
        assert (cls.database[_collection])

        result = cls.database[_collection].delete_many( _query)
        print( result.deleted_count)

    def update_data_in_collection(cls, _collection, _query, _newData):
        assert (cls.database[_collection])

        result = cls.database[_collection].update_many(_query, { "$set" : _newData })
        print( result.upserted_id)