from starlette.config import Config
import os

config = Config(".env")

# address of Google matrix API
API_ADDRESS = "https://maps.googleapis.com/maps/api/distancematrix/json"
# google maps API KEY (used to create distance matrix for real locations)
API_KEY = os.environ['API_KEY'] #config("API_KEY", cast=str)
