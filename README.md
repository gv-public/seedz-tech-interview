# seedz-tech-interview
Technichal interview for Seedz company

The techinical challenge was divided in two steps

1. Answering some Data Science questions based on the SQL and JSON file provided.
2. Creating an API, documenting it and publishing it in some cloud plataform.

## Answering the Data Science Questions

A PostgreSQL database was created on the AWS RDS platform, then the scripts were executed in the database. Therefore the data is on a reliable cloud system.

After that, python was used to connect to the database using the psycopg2 library given it's lightweight and ease of use and the data was later manipulated using Pandas 
with the plots being made with matplotlib and seaborn.

The answers to each question with the relevant graphs and code can be found in the questions_python.ipynb file.

## The Creation of The API

The api was created using Flask. The choice was made given the amount of time avaiable to work on the challenge since Flask is easier to jump to the coding.

The structure of the API is very straight forward. With the main file being app.py where the routes and the logic is located. The secondary file called queries.py contains
only the SQL queries responsible for the inserts and selects on the database. The decision to keep it in another file was to avoid cluttering. The connection to the database is
made by a Connection Pool method, so it can be refreshed even when the service is deployed live.

As stated before, the database is hosted on AWS and is accessed by hidden credentials in the form of a .env file (like the example one). The actual credentials will be sent to the
interviewer if asked. After the documentation was made on Postman, it was also hosted on the AWS platform, in this case on S3, and can be acessed through this link: https://seedzbucket.s3.amazonaws.com/Seedz_doc.pdf. 

When the service was ready it was hosted on a free platform called "render.com" because it provides some good options to free hosting an API. The sidenote being that in the free plan it's common for them to reduce the process power of the machine after a long time unused, so in the few first calls it might take a bit longer to answer. The link to the deployed API is: https://seedz-api-70k9.onrender.com and the routes that can be used are shown in the documentation.

To run the API locally it's necessary to follow these steps:

1. Go to the api folder as your root folder
2. Run "python3.8 -m venv venv" to create the virtual environment
3. Install the dependencies using "pip install -r requirements.txt"
4. Create a .env file in the structure of the .env.example file but with the actual credentials
5. Run "flask run"

