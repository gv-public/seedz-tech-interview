import os
from datetime import datetime

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_file

from queries import (
    DELETE_WEATHER_DATA,
    GET_CITIES_LIST,
    GET_WEATHER_CITY,
    GET_WEATHER_CITY_BETWEEN_DATES,
    GET_WEATHER_CITY_DATE,
    INSERT_WEATHER,
)

load_dotenv()
app = Flask(__name__)

connection = psycopg2.connect(
    host=os.getenv('HOST'),
    database=os.getenv('DATABASE'),
    user=os.getenv('DATABASE_USER'),
    password=os.getenv('PASSWORD')
)

required_fields = ['cod_city', 'date', 'hour']
non_required_fields = [
    "precipitation",
    "dry_bulb_temperature",
    "wet_bulb_temperature",
    "high_temperature",
    "low_temperature",
    "relative_humidity",
    "relative_humidity_avg",
    "pressure",
    "sea_pressure",
    "wind_direction",
    "wind_speed_avg",
    "cloud_cover",
    "evaporation"
]


def check_dict_keys(dictionary, keys_list):
    for key in keys_list:
        if key not in dictionary:
            dictionary[key] = None

    return dictionary


@app.get('/')
def home():
    return 'Home of the Api please check documentation on /docs.'


@app.get('/health')
def health():
    return f'API is live @ {datetime.now()}'


@app.get('/docs')
def docs():
    return 'https://seedzbucket.s3.amazonaws.com/Seedz_doc.pdf'


@app.post('/weather/create')
def create_weather():
    data = request.get_json()

    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400

    # Set non-required fields to None if they arrive empty
    data = check_dict_keys(data, non_required_fields)

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_WEATHER, (data['cod_city'], data['date'], data['hour'], data['precipitation'], data['dry_bulb_temperature'], data['wet_bulb_temperature'], data['high_temperature'], 
                                            data['low_temperature'], data['relative_humidity'], data['relative_humidity_avg'], data['pressure'], data['sea_pressure'], data['wind_direction'], 
                                            data['wind_speed_avg'], data['cloud_cover'], data['evaporation']))

    return jsonify({'success': 'Grid Weather created successfully', 'data': data}), 201


@app.get('/cities/list')
def list_cities():

    try:
        with connection:
            with connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute(GET_CITIES_LIST, ())

                data = cursor.fetchmany(200)
    except Exception as e:
        print(e)
        return jsonify({'error': 'ERROR querying the database'}), 400

    return jsonify({'success': 'List of cities retrieved sucessfully', 'data': data}), 200


@app.get('/weather/list')
def list_weather():
    try:
        cod_city = str(request.args.get('cod_city'))

        try:
            with connection:
                with connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                    cursor.execute(GET_WEATHER_CITY, (cod_city,))

                    data = cursor.fetchmany(200)
        except Exception as e:
            print(e)
            return jsonify({'error': 'ERROR querying the database'}), 400

    except Exception as e:
        print(e)
        return jsonify({'error': 'The paramn "cod_city" must me sent on the request'}), 400

    return jsonify({'success': 'Weather from the city retrieved sucessfully', 'data': data}), 200


@app.get('/weather/date')
def get_weather_by_date():
    try:
        first_date = str(request.args.get('first_date'))
        cod_city = str(request.args.get('cod_city'))
        second_date = str(request.args.get('second_date'))

        try:
            with connection:
                with connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:

                    if second_date == 'None':
                        cursor.execute(GET_WEATHER_CITY_DATE, (cod_city, first_date))
                    else:
                        cursor.execute(GET_WEATHER_CITY_BETWEEN_DATES, (first_date, second_date, cod_city))
                    data = cursor.fetchmany(200)
            return jsonify({'success': 'Weather from the city retrieved sucessfully', 'data': data}), 200

        except Exception as e:
            print(e)
            return jsonify({'error': 'ERROR querying the database'}), 400

    except Exception as e:
        print(e)
        return jsonify({'error': 'At least the paramns "cod_city" and "first_date" must me sent on the request'}), 400       


@app.delete('/weather')
def delete_weather():
    try:
        first_date = str(request.args.get('first_date'))
        cod_city = str(request.args.get('cod_city'))

        try:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(DELETE_WEATHER_DATA, (cod_city, first_date))

            return jsonify({'success': 'Weather from the city on this date were deleted sucessfully'}), 204

        except Exception as e:
            print(e)
            return jsonify({'error': 'ERROR querying the database'}), 400

    except Exception as e:
        print(e)
        return jsonify({'error': 'At least the paramns "cod_city" and "first_date" must me sent on the request'}), 400       
