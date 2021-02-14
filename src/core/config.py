from starlette.config import Config

config = Config(".env")

# google maps API KEY (used to create distance matrix for real locations)
API_KEY = config("API_KEY", cast=str)
