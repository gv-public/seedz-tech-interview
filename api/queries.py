TEST_QUERY = "SELECT * from weather.grid_weather_data LIMIT 1;"

GET_WEATHER = "SELECT * FROM weather.grid_weather_data WHERE cod_city = %s and date = %s;"

INSERT_WEATHER = """INSERT INTO weather.grid_weather_data (cod_city,"date","hour",precipitation,dry_bulb_temperature,wet_bulb_temperature,high_temperature,low_temperature,relative_humidity,
relative_humidity_avg,pressure,sea_pressure,wind_direction,wind_speed_avg,cloud_cover,evaporation) VALUES
(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""

GET_WEATHER_CITY = """SELECT * FROM weather.grid_weather_data WHERE cod_city = %s;"""

GET_WEATHER_CITY_DATE = """SELECT * FROM weather.grid_weather_data WHERE cod_city = %s AND date = %s"""

GET_WEATHER_CITY_BETWEEN_DATES = """SELECT * 
from weather.grid_weather_data gwd 
WHERE (date between %s and %s) and cod_city = %s;"""

GET_CITIES_LIST = """SELECT distinct cod_city FROM weather.grid_weather_data;;"""

DELETE_WEATHER_DATA = """DELETE FROM weather.grid_weather_data WHERE cod_city = %s and date = %s;"""
