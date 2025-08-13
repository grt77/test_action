from ..maino import sm

def test_sm():
    assert sm(2,4)==6
    assert sm(2, 7) == 9
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, col, map_from_arrays
from pyspark.sql.types import StringType

spark = SparkSession.builder.appName("demo").getOrCreate()

df = spark.read.json("/usrwrk/twe/db/twe_1h/schemas/twe_1h_wrkccvt4_uwa.db/ffl_sampling_ids/temp123.json")

# Explode the JSON structure
n_df = df.withColumn("test", explode(col("results"))) \
         .withColumn("T", explode(col("test.T"))) \
         .select("T")

# Convert struct to Map<String, String>
# First get keys and values separately, then create a map
attr_cols = [c for c in n_df.select("T.attributes.*").columns]
n_df = n_df.select(
    col("T.v_id").alias("v_id"),
    col("T.v_type").alias("v_type"),
    map_from_arrays(
        array([lit(c) for c in attr_cols]), 
        array([col(f"T.attributes.{c}").cast(StringType()) for c in attr_cols])
    ).alias("attributes")
)

# Now you can explode the map
r = n_df.withColumn("new", explode(col("attributes")))
r.show(truncate=False)


def exe_cmd_to_file(cmd, output_file, check_status=True):
    try:
        with open(output_file, "wb") as f:
            p = sp.Popen(cmd, stdout=f, stderr=sp.PIPE, shell=True)
            _, errors = p.communicate()

        if p.returncode != 0 and check_status:
            raise Exception(f"cmd: {cmd} failed to execute: {errors.decode('utf-8')}")
        
        return output_file  # Path to saved file
    except Exception as e:
        raise Exception(f"Error executing cmd: {repr(e)}")
