"""
Abdullah Mohammed 2022-12-22

Shuffles a CUSTOM Shopify collection randomly. DOES NOT work on Smart Collections

Get collection ID from https://<shopify_url>/admin/collections/<collection_id>

"""
import time
import random
import secrets
from progressbar import progressbar
from helpers import get_all_resources, load_config
from shopify import Session, ShopifyResource, Shop, Product, GraphQL, CustomCollection

CONFIG = load_config()
shop_url = CONFIG["shop_url"]
token = CONFIG["token"]
api_ver = CONFIG["api_ver"]
##################
session = Session(shop_url, api_ver, token)
ShopifyResource.activate_session(session)
shop = Shop.current()  # Get the current shop

collect_id = input("Enter custom collection id >> ")
is_backup = True if input(
    "Backup Collection? (y/n) >> ").lower() == "y" else False
# get collection
collection = CustomCollection.find(collect_id)

print(f"Found collection '{collection.title}'")
# get all the products from the collection
products = get_all_resources(CustomCollection(
    attributes={"id": collection.id}).products())
print(f"Found {len(products)} products")
if is_backup:
    # backup the products to a new collection
    backup = CustomCollection()
    backup.title = f"{collection.handle}-backup-{secrets.token_hex(2)}"
    backup.save()
    print(f"Backing up collection to {backup.title}")
    for product in progressbar(products, redirect_stdout=True):
        backup.add_product(product)
        time.sleep(0.4)
    backup.save()

print("Deleting products in collection")
# delete all existign products
for product in progressbar(products, redirect_stdout=True):
    collection.remove_product(product)
    time.sleep(0.4)
collection.save()

# randomize the order
random.shuffle(products)
print("Re-adding products back to collection")
for product in progressbar(products, redirect_stdout=True):
    collection.add_product(product)
    time.sleep(0.5)
    print("Added product " + product.handle)
collection.save()

ShopifyResource.clear_session()
