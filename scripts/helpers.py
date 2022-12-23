import os, json

def get_all_resources(collection, **kwargs):
    resources = []
    resources.extend(collection)
    while collection.has_next_page():
        collection = collection.next_page()
        resources.extend(collection)
    return resources

def load_config() -> dict:
    fn = "config.json" 
    if not os.path.isfile(fn):
        fn = "../config.json"
        if not os.path.isfile(fn):
            raise Exception("Unable to find config.json.")

    with open(fn, "r") as f:
        return json.load(f)