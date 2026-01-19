provider "google" {
  project = var.gcp_project_id
  region  = var.region
}

# 1. GCS Bucket for Code & Temporary Spark Data
resource "google_storage_bucket" "spark_assets" {
  name     = var.bucket_name
  location = var.region
  force_destroy = true
}

# 2. Pub/Sub Topic for Job 2 (Orders)
resource "google_pubsub_topic" "orders_topic" {
  name = var.pub_sub_topic_name
}

resource "google_pubsub_subscription" "orders_sub" {
  name  = var.pub_sub_subscription_name
  topic = google_pubsub_topic.orders_topic.name
}

# 3. BigQuery Dataset & Tables
resource "google_bigquery_dataset" "ecommerce_ds" {
  dataset_id = var.bigquery_target_dataset
  location   = "US"
}

resource "google_bigquery_table" "clickstream_table" {
  dataset_id = google_bigquery_dataset.ecommerce_ds.dataset_id
  table_id   = "fact_clickstream"
  deletion_protection = false
}

//Create Dataproc staging bucket
resource "google_storage_bucket" "dataproc_staging_bucket" {
  project = var.gcp_project_id
  name = var.dataproc_staging_bucket
  location = var.region
}

# 4. Dataproc Cluster (Optimized for Streaming)
resource "google_dataproc_cluster" "dp_cluster" {
  project = var.gcp_project_id
  name = var.dataproc_cluster_name
  depends_on = [google_storage_bucket.dataproc_staging_bucket]
  region = var.region

  cluster_config {

    lifecycle_config {
      # The cluster will delete itself after being idle for 20 minutes
      idle_delete_ttl = "1200s"
    }

    master_config {
      num_instances = 1
      machine_type = var.master_machine_type
      disk_config {
        boot_disk_size_gb = 50
        boot_disk_type    = "pd-standard"
      }
    }

    worker_config {
      num_instances = 2
      machine_type  = var.worker_machine_type
      disk_config {
        boot_disk_size_gb = 50
        boot_disk_type    = "pd-standard"
      }
    }

    preemptible_worker_config {
      num_instances  = 3
      disk_config {
        boot_disk_size_gb = 50
        boot_disk_type    = "pd-standard"
      }
    }

    software_config {
      image_version = var.dataproc_software_image
    }
    staging_bucket = var.dataproc_staging_bucket
  }
}