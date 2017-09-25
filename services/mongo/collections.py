from collegeevents.mongo_settings import MongoConnection
from services.mongo.events import EventsSerializer
from services.mongo.institutes import AllInstituteSerializer


class InstituteCollection(MongoConnection):

    def __init__(self):
        super(InstituteCollection, self).__init__()
        self.get_collection('institutes')

    def save_and_update(self, obj):
        if self.collection.find({'id': str(obj.id)}).count():
            self.collection.update({ "id": str(obj.id)}, AllInstituteSerializer(obj).data)
        else:
            self.collection.insert_one(AllInstituteSerializer(obj).data)

    def remove(self, obj):
        if self.collection.find({'id': str(obj.id)}).count():
            self.collection.delete_one({ "id": str(obj.id)})


class EventCollection(MongoConnection):

    def __init__(self):
        super(EventCollection, self).__init__()
        self.get_collection('events')

    def save_and_update(self, obj):
        if self.collection.find({'id': str(obj.id)}).count():
            self.collection.update({ "id": str(obj.id)}, EventsSerializer(obj).data)
        else:
            self.collection.insert_one(EventsSerializer(obj).data)

    def remove(self, obj):
        if self.collection.find({'id': str(obj.id)}).count():
            self.collection.delete_one({ "id": str(obj.id)})
