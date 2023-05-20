import pymongo

if __name__ == '__main__':

    # ------------------------------ Connect to MongoDB
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    db_src = myclient["TIKI"]
    db_src_col = db_src["product"]

    db_dest = myclient["TIKI_HUY"]
    db_dest_col = db_dest["product"]

    with open('data/MY_CATEGORIES', 'r') as f:
        list_my_cat = [x.strip() for x in f.readlines()]

    data = list(db_src_col.find({"category": {"$in": list_my_cat}}))
    db_dest_col.insert_many(data)

    print("DONE")
