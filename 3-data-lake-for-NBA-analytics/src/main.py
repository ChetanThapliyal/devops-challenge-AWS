import boto3
import json
import time
import requests
import os
import logging
from dotenv import load_dotenv
from botocore.exceptions import ClientError

# Initialize logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load environment variables
load_dotenv()

# Constants and Configurations
REGION = os.getenv("AWS_REGION", "us-east-1")  # Default to 'us-east-1'
BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
GLUE_DATABASE_NAME = os.getenv("GLUE_DATABASE_NAME")
ATHENA_OUTPUT_LOCATION = f"s3://{BUCKET_NAME}/athena-results/"
API_KEY = os.getenv("SPORTS_DATA_API_KEY")
NBA_ENDPOINT = os.getenv("NBA_ENDPOINT")

# AWS clients
s3_client = boto3.client("s3", region_name=REGION)
glue_client = boto3.client("glue", region_name=REGION)
athena_client = boto3.client("athena", region_name=REGION)


def create_s3_bucket():
    try:
        s3_client.create_bucket(Bucket=BUCKET_NAME)
        logging.info(f"S3 bucket '{BUCKET_NAME}' created successfully.")
    except ClientError as e:
        logging.error(f"Failed to create S3 bucket: {e.response['Error']['Message']}") 


def create_glue_database():
    try:
        glue_client.create_database(
            DatabaseInput={
                "Name": GLUE_DATABASE_NAME,
                "Description": "Glue database for NBA sports analytics.",
            }
        )
        logging.info(f"Glue database '{GLUE_DATABASE_NAME}' created successfully.")
    except ClientError as e:
        logging.error(f"Failed to create Glue database: {e.response['Error']['Message']}")


def fetch_nba_data():
    try:
        headers = {"Ocp-Apim-Subscription-Key": API_KEY}
        response = requests.get(NBA_ENDPOINT, headers=headers)
        response.raise_for_status()
        logging.info("Fetched NBA data successfully.")
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Error fetching NBA data: {e}")
        return []


def convert_to_line_delimited_json(data):
    """Convert data to line-delimited JSON format."""
    return "\n".join(json.dumps(record) for record in data)


def upload_data_to_s3(data):
    """Upload NBA data to S3 in line-delimited JSON format."""
    try:
        file_key = "raw-data/nba_player_data.jsonl"
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=file_key,
            Body=convert_to_line_delimited_json(data)
        )
        logging.info(f"Data uploaded to S3 at '{file_key}'.")
    except ClientError as e:
        logging.error(f"Failed to upload data to S3: {e.response['Error']['Message']}")


def create_glue_table():
    """Create a Glue table for the NBA data."""
    try:
        glue_client.create_table(
            DatabaseName=GLUE_DATABASE_NAME,
            TableInput={
                "Name": "nba_players",
                "StorageDescriptor": {
                    "Columns": [
                        {"Name": "PlayerID", "Type": "int"},
                        {"Name": "FirstName", "Type": "string"},
                        {"Name": "LastName", "Type": "string"},
                        {"Name": "Team", "Type": "string"},
                        {"Name": "Position", "Type": "string"},
                        {"Name": "Points", "Type": "int"}
                    ],
                    "Location": f"s3://{BUCKET_NAME}/raw-data/",
                    "InputFormat": "org.apache.hadoop.mapred.TextInputFormat",
                    "OutputFormat": "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat",
                    "SerdeInfo": {
                        "SerializationLibrary": "org.openx.data.jsonserde.JsonSerDe"
                    },
                },
                "TableType": "EXTERNAL_TABLE",
            },
        )
        logging.info("Glue table 'nba_players' created successfully.")
    except ClientError as e:
        logging.error(f"Failed to create Glue table: {e.response['Error']['Message']}")


def configure_athena():
    """Set up Athena output location and create a database."""
    try:
        athena_client.start_query_execution(
            QueryString="CREATE DATABASE IF NOT EXISTS nba_analytics",
            QueryExecutionContext={"Database": GLUE_DATABASE_NAME},
            ResultConfiguration={"OutputLocation": ATHENA_OUTPUT_LOCATION},
        )
        logging.info("Athena output location configured successfully.")
    except ClientError as e:
        logging.error(f"Failed to configure Athena: {e.response['Error']['Message']}")


def main():
    """Main function to orchestrate data lake setup."""
    logging.info("Starting data lake setup for NBA analytics...")
    create_s3_bucket()
    time.sleep(5)  # Allow time for bucket creation
    create_glue_database()
    nba_data = fetch_nba_data()
    if nba_data:
        upload_data_to_s3(nba_data)
    create_glue_table()
    configure_athena()
    logging.info("Data lake setup completed successfully.")


if __name__ == "__main__":
    main()
