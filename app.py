from flask import Flask, render_template, request
import pandas as pd
import boto3
from botocore.exceptions import NoCredentialsError

app = Flask(__name__, template_folder='templates')

# Function to download the dataset from S3
def download_dataset_from_s3(bucket_name, object_key, destination_path):
    s3 = boto3.client('s3')
    try:
        s3.download_file(bucket_name, object_key, destination_path)
        print(f"Dataset downloaded from S3 to {destination_path}")
        return True
    except NoCredentialsError:
        print("Credentials not available")
        return False

# Replace these values with your S3 bucket and object key
s3_bucket_name = 'cloudassignment202'
s3_object_key = 'Cloud_Data.csv'

# Specify the local path where you want to download the dataset
local_dataset_path = 'dataset.csv'

# Download the dataset from S3
download_success = download_dataset_from_s3(s3_bucket_name, s3_object_key, local_dataset_path)

# Load your dataset
if download_success:
    dataset = pd.read_csv(local_dataset_path)
else:
    dataset = pd.DataFrame()  # Empty DataFrame if download fails

@app.route('/', methods=['GET', 'POST'])
def index():
    # Get unique values for dropdowns
    cities = dataset['city'].unique()
    costs = dataset['cost'].unique()
    veg_or_non_vegs = dataset['veg_or_non_veg'].unique()

    top_rated_restaurants = pd.DataFrame()  # Initialize an empty DataFrame

    if request.method == 'POST':
        # Get user selections from the form
        selected_city = request.form['city']
        selected_cost = request.form['cost']
        selected_veg_or_non_veg = request.form['veg_or_non_veg']

        # Filter the dataset based on user selections
        filtered_data = dataset[
            (dataset['city'] == selected_city) &
            (dataset['cost'] == selected_cost) &
            (dataset['veg_or_non_veg'] == selected_veg_or_non_veg)
        ]

        # Get the top-rated restaurants
        top_rated_restaurants = filtered_data.sort_values(by='rating', ascending=False).head(10)

    return render_template('cloudassignment2.html', cities=cities, costs=costs, veg_or_non_vegs=veg_or_non_vegs,
                           top_rated_restaurants=top_rated_restaurants)

if __name__ == '__main__':
    app.run(debug=True)
