# Test Google Cloud Storage Bucket as Volume Mount with GCS FUSE

This is a simple test to see if we can use google cloud storage bucket as a volume for google cloud run job.

clone the project here

```bash
git clone https://github.com/bhanu-fyi/gcs-fuse-test.git
```

For this test, I have setup a bucket named `rail-segmentation` which has a folder `rs19_val` which consists files of RailSem19 Dataset.

You can setup any folder with files in the bucket and use it as a volume for this test.

This bucket is created in `us-east1` region.

I needed access data from this bucket but downloading then to In memory or local disk was not an option due to the size of the dataset. So I decided to use GCS FUSE to mount the bucket as a volume to the google cloud run job.

So Test it out, I created a simple python script that counts the number of files in the mounted bucket and uploads the count to gcs bucket `rs_val20` It creates the bucket if doesn't exist. For this to happen you need to make sure that you have neccessary permissions. 

To get a clear picture of permissions that I need for resources that are used in this test. I have created a service account with following roles [here](https://console.cloud.google.com/iam-admin/serviceaccounts/create)

* Artifact Registry Administrator
* Cloud Run Admin
* Cloud Run Jobs Executor
* Logs Writer
* Service Account User
* Storage Object Admin

![service account](/imgs/service-account.png)

Now download the service account key and save it as `local-dev.json` in the root of the project.

In cmd activate the service account using the following command

```bash
gcloud auth activate-service-account --key-file=local-dev.json
```

activate the required services using the following command ( activate these using your admin account)

```bash
gcloud services enable run.googleapis.com artifactregistry.googleapis.com compute.googleapis.com serviceusage.googleapis.com
```

create a repository in artifact registry using the following command

```bash
gcloud artifacts repositories create bhanufyi --repository-format=docker --location=us-east1
```

configure the docker to push the image to the artifact registry using the following command

```bash
gcloud auth configure-docker us-east1-docker.pkg.dev
```

create virtual environment and install the required packages using the following command

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

enable buildx for multi platform builds

```bash
docker buildx create --use
docker buildx inspect --bootstrap
```

build the docker image for multi plaform using buildx and push it to the artifact registry using the following command

```bash
docker buildx build --platform linux/amd64,linux/arm64 -t us-east1-docker.pkg.dev/bhanufyi/bhanufyi/count-files-job:latest --push .
```
![Artifact Registry](/imgs/artifact-registry.png)

Create a VPC connector using the following command. [Why ?](https://cloud.google.com/run/docs/configuring/jobs/cloud-storage-volume-mounts#network-bandwidth)

```bash
gcloud compute networks vpc-access connectors create useast1-vpc-connector \
    --region=us-east1 \
    --network=default \
    --range=10.8.0.0/28
```

Build and push the image to the artifact registry using the following command. Read this for more information [here](https://cloud.google.com/run/docs/configuring/jobs/cloud-storage-volume-mounts)

```bash
gcloud beta run jobs create count-files-job \
    --image=us-east1-docker.pkg.dev/bhanufyi/bhanufyi/count-files-job:latest \
    --region=us-east1 \
    --add-volume=name=rail_segmentation_volume,type=cloud-storage,bucket=rail-segmentation \
    --vpc-egress=all-traffic \
    --vpc-connector=useast1-vpc-connector \
    --add-volume-mount=volume=rail_segmentation_volume,mount-path=/data \
    --memory=512Mi \
```

![cloud run jobs](/imgs/cloudrun-jobs.png)

execute the following job to count the files in the folder `rs19_val` and save the count to the bucket `rs_val20`

```bash
gcloud beta run jobs execute count-files-job --region=us-east1
```

creating this job in `us-east1` region is important because the bucket is also created in the same region.

You can check the saved file in the bucket `rs_val20` to see the count of files in the folder `rs19_val`

![Image](/imgs/buckets.png)


```bash
gsutil cp gs://rs_val20/count.txt count.txt
```

The script counts files for 30 times to check the time for each run. From my observation, there isn't much difference for 1st access to 30th access. I did this to check if there is any difference because of caching from 2nd run onwards. But I didn't see any difference. It was more or less uniform.

There's another service from gcp `filestore` which can be used as mount but the minimum size is 1TB and the cost is high. So I decided to go with GCS FUSE.
If you don't have restrictions on price and your data is considerably high, you can go with `filestore` as well.
