import os
import time
from google.cloud import storage


def count_files_in_directory(directory):
    """Counts the number of files in a directory recursively."""
    total_files = 0
    try:
        for root, dirs, files in os.walk(directory):
            total_files += len(files)
    except Exception as e:
        print(f"Error while counting files in {directory}: {e}")
    return total_files


def write_results_to_file(results, output_file):
    """Writes results (file count and timing) to a text file."""
    try:
        with open(output_file, "w") as f:
            for run, (count, duration) in enumerate(results, start=1):
                f.write(
                    f"Run {run}: Total files = {count}, Time taken = {duration:.2f} seconds\n"
                )
        print(f"Results written to {output_file}")
    except Exception as e:
        print(f"Error while writing to file {output_file}: {e}")


def create_bucket_if_not_exists(bucket_name, location="US"):
    """Creates a GCS bucket if it doesn't already exist."""
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    try:
        client.get_bucket(bucket_name)
        print(f"Bucket {bucket_name} already exists.")
    except Exception as e:
        print(f"Bucket {bucket_name} does not exist. Creating it...")
        try:
            bucket = client.create_bucket(bucket_name, location=location)
            print(f"Bucket {bucket_name} created successfully in location {location}.")
        except Exception as create_error:
            print(f"Failed to create bucket {bucket_name}. Error: {create_error}")
            raise


def upload_file_to_gcs(local_file, bucket_name, gcs_destination, max_retries=3):
    """Uploads a file to a GCS bucket with retry logic."""
    create_bucket_if_not_exists(bucket_name)  # Ensure the bucket exists

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(gcs_destination)

    for attempt in range(1, max_retries + 1):
        try:
            blob.upload_from_filename(local_file)
            print(
                f"Successfully uploaded {local_file} to gs://{bucket_name}/{gcs_destination}"
            )
            return
        except Exception as e:
            print(
                f"Attempt {attempt}: Failed to upload {local_file} to GCS. Error: {e}"
            )
            if attempt == max_retries:
                print("Max retries reached. Upload failed.")
            else:
                time.sleep(2**attempt)  # Exponential backoff


if __name__ == "__main__":
    # Mounted bucket path
    bucket_mount_path = "/data"
    subfolder = "rs19_val"  # Subfolder within the bucket
    subfolder_path = os.path.join(bucket_mount_path, subfolder)

    output_file = "/tmp/count_results.txt"
    gcs_bucket_name = "rs_val20"
    gcs_destination = "count_results.txt"
    print("Hello World")

    # Check if the subfolder exists
    if not os.path.exists(subfolder_path):
        print(f"Subfolder path {subfolder_path} does not exist!")
        print(f"Contents of /data: {os.listdir(bucket_mount_path)}")
    else:
        results = []  # To store file count and time taken for each run

        for i in range(30):
            print(f"Starting run {i + 1} on subfolder {subfolder_path}...")
            start_time = time.time()
            file_count = count_files_in_directory(subfolder_path)
            duration = time.time() - start_time
            results.append((file_count, duration))
            print(
                f"Run {i + 1}: Total files = {file_count}, Time taken = {duration:.2f} seconds"
            )

        # Write the results to a text file
        write_results_to_file(results, output_file)

        # Upload the text file to the specified GCS bucket
        upload_file_to_gcs(output_file, gcs_bucket_name, gcs_destination)
