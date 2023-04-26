import pymongo
import certifi


con_str = "mongodb+srv://jcano22:password22@jorgec22.6avhlq7.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(con_str, tlsCAFile=certifi.where())
db = client.get_database('menu')