import quart
from services import weather_service, sun_service, location_service

blueprint = quart.blueprints.Blueprint(__name__, __name__)


@blueprint.route("/api/events/<city>/<state>/<country>", methods=["GET"])
def events(city: str, state: str, country: str):
    player = {
        "name": "Jeff the player",
        "city": city,
        "state": state,
        "country": country,
    }
    if not player:
        quart.abort(404)
    # return quart.jsonify(player)
    return player


# @blueprint.route("/api/weather/<zip_code>/<country>", methods=["GET"])
# def weather(zip_code: str, country: str):
#     weather_data = weather_service.get_current(zip_code, country)
#     if not weather_data:
#         quart.abort(404)
#     return weather_data


@blueprint.route("/api/sun/<zip_code>/<country>", methods=["GET"])
async def sun(zip_code: str, country: str):
    lat, long = await location_service.get_lat_long(zip_code, country)
    sun_data = await sun_service.for_today(lat, long)
    if not sun_data:
        quart.abort(404)
    return sun_data
