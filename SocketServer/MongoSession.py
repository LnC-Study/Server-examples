import pymongo, config
from Logger import Logger

class MongoSession:
    def __init__(self, _deviceId):
        self.client = pymongo.MongoClient( host=config.DATABASE['HOST'],
                                           port=config.DATABASE['PORT'])
        self.collection = 'Device' + str(_deviceId)
        self.database = self.client[ config.DATABASE['DB_NAME']][ self.collection]
        self.count, self.dataStack = 0, []

        Logger.logWriter.info(f'A session[{_deviceId}] connect to mongoDB')

    def create_index_on_database(self):
        pass

    def get_data_from_collection(self, _query):
        return self.database.find( _query)

    def _add_data(self, _data):
        if type( _data) is list:
            result = self.database.insert_many( _data)
        else:
            result = self.database.insert_one( _data)

        return result

    def add_data_in_collection(self, _data):

        if config.SAVE_DATA_PACKING:
            self.dataStack.append( _data)
            self.count += len(_data)
            if self.count > 100 :
                result = self._add_data( self.dataStack)
                Logger.logWriter.info(f'MongoDB session[{self.collection}] adds { self.count}')
                self.count, self.dataStack = 0, []
            # Logger.logWriter.info(f'\t{result.inserted_ids}')
        else :
            result = self._add_data( _data)
            Logger.logWriter.info(f'MongoDB session[{self.collection}] adds {self.len(_data)}')

        return result

    def delete_data_in_collection(self, _query):
        return self.database.delete_many( _query)

    def update_data_in_collection(self, _query, _newData):
        return self.database.update_many( _query, {"$set" : _newData})

    def close(self):
        self.client.close()