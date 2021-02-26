from starlette.config import Config

config = Config(".env")

# address of Google matrix API
API_ADDRESS = "https://maps.googleapis.com/maps/api/distancematrix/json"
# google maps API KEY (used to create distance matrix for real locations)
API_KEY = config("API_KEY", cast=str)
