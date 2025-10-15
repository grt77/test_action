#!/bin/bash
# ------------------------------------------------------------
# Script Name: run_reprocess.sh
# Purpose: To upload reprocess files, run Impala and Spark jobs
# Author: Raviteja
# ------------------------------------------------------------

# --- Variable section ---
key=keyvalue
need_to_reprocess_file_date="2025-01-01"
todays_date=$(date +%Y-%m-%d)

# --- Paths ---
base_path=""
impala_table=".ffi_temp_table_${todays_date}"

# --- HDFS Operations ---
echo "Uploading reprocess files to HDFS..."
hdfs dfs -put ${key}_prod_${need_to_reprocess_file_date}.csv ${base_path}/
hdfs dfs -put ${key}_prod_${todays_date}.csv ${base_path}/
hdfs dfs -put ${key}_prod_${todays_date}_backup.csv ${base_path}/

# --- Impala Table Creation ---
echo "Creating Impala temporary table..."
impala-shell -k -ssl -B --output_delimiter=',' -q "
CREATE TABLE ${impala_table} AS
SELECT * FROM wrk_081_uwa.ffi_temp_table_${need_to_reprocess_file_date};
"

# --- Spark Job Execution ---
echo "Running Spark job..."
spark3-submit Force_Fast_Lane_2.0_V2/main.py \
    "${key}" "PROD" "force-run" "${key}_prod_${todays_date}.csv"

# --- HDFS Cleanup ---
echo "Cleaning up HDFS..."
hdfs dfs -rm ${base_path}/${key}_prod_${todays_date}.csv

echo "Script completed successfully."
