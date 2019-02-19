from pyspark.sql import SparkSession

filename = '/home/noel/spark-2.4.0/README.md'
with SparkSession.builder.appName("SimpleApp").getOrCreate() as spark:
    file_data = spark.read.text(filename).cache()

    a_count = file_data.filter(file_data.value.contains('a')).count()
    b_count = file_data.filter(file_data.value.contains('b')).count()

    print("Lines with a: %i, lines with b: %i" % (a_count, b_count))
