//Project Id to use in Google Cloud Platform
gcp_project_id = "learn-streaming"
//Region to use in Google Cloud Platform
region = "us-central1"
//Zone to use in Google Cloud Platform
zone = "us-central1-a"
//GCP service list
GCP_service_list = ["bigquery.googleapis.com","dataproc.googleapis.com", "storage.googleapis.com"]
//Master Machine Type
master_machine_type = "n1-standard-2"
//Worker Machine Type
worker_machine_type = "n1-standard-2"
//Target Bigquery Dataset
bigquery_target_dataset = "ecommerce_analytics"
//Dataproc Staging Bucket
dataproc_staging_bucket = "gcloud-dataproc-stg-bkt-bkd"
//Dataproc Cluster_name
dataproc_cluster_name = "dp-cluster-bkd-supply-chain"
//Dataproc Software Image
dataproc_software_image = "2.1-debian11"
//Bucket Name
bucket_name = "gcp-dataproc-spark-code-bkd"
//Pub/Sub Topic name
pub_sub_topic_name = "ecommerce-orders"
//Pub/Sub Subscription name
pub_sub_subscription_name = "ecommerce-orders-sub"