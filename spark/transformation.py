import argparse
from os.path import join

from pyspark.sql import SparkSession
from pyspark.sql import functions as f
from pyspark.sql.functions import to_date


def get_tweets_data(df):
    print("***************[LOG VINI] Transformation - get_tweets_data - 1")
    return df.select(
            f.explode("data").alias("tweets")
            ).select(
                "tweets.author_id",
                "tweets.conversation_id",
                "tweets.created_at",
                "tweets.id",
                "tweets.in_reply_to_user_id",
                "tweets.public_metrics.*",
                "tweets.text"
            )


def get_users_data(df):
    print("***************[LOG VINI] Transformation - get_users_data - 1")
    return df.select(
                f.explode("includes.users").alias("users")
            ).select(
                "users.*"
            )


def export_json(df, dest):
    print("***************[LOG VINI] Transformation - export_json - 1")
    df.printSchema()
    print("***************[LOG VINI] Transformation - export_json - 2", dest)
    df.coalesce(1).write.mode("overwrite").json(dest)


def twitter_transform(spark, src, dest, process_date):
    print("***************[LOG VINI] Transformation - twitter_transform - 1")
    df = spark.read.json(src)
    print("***************[LOG VINI] Transformation - twitter_transform - 2")
    tweet_df = get_tweets_data(df)
    print("***************[LOG VINI] Transformation - twitter_transform - 3")
    user_df = get_users_data(df)
    print("***************[LOG VINI] Transformation - twitter_transform - 4")
    '''
    tweet_df.printSchema()
    #tweet_df.write.mode("overwrite").option("header", True).csv("/opt/bitnami/datalake/export")
    #tweet_df.repartition(5).coalesce(2).write.mode("overwrite").option("header", True).csv("/opt/bitnami/datalake/export2")
    tweet_df.rdd.getNumPartitions()
    tweet_df.groupBy(to_date("created_at")).count().show()
    export_df = tweet_df.withColumn("created_date", to_date("created_at")).repartition("created_date")
    export_df.write.mode("overwrite").partitionBy("created_date").json("/opt/bitnami/datalake/silver/export_json")
    read_df = spark.read.json("/opt/bitnami/datalake/export_json")
    read_df.where("created_date = '2021-07-19'").explain()
	'''

    table_dest = join(dest, "{table_name}", f"process_date={process_date}")
    print("***************[LOG VINI] Transformation - twitter_transform - 5")
    export_json(tweet_df, table_dest.format(table_name="tweet"))
    print("***************[LOG VINI] Transformation - twitter_transform - 6")
    export_json(user_df, table_dest.format(table_name="user"))


if __name__ == "__main__":
    print("***************[LOG VINI] Transformation - 1")
    parser = argparse.ArgumentParser(
        description="Spark Twitter Transformation"
    )
    print("***************[LOG VINI] Transformation - 2")
    parser.add_argument("--src", required=True)
    parser.add_argument("--dest", required=True)
    parser.add_argument("--process-date", required=True)
    args = parser.parse_args()
    print("***************[LOG VINI] Transformation - 3")
    spark = SparkSession.builder.master("local").appName("twitter_transformation").getOrCreate()
    print("***************[LOG VINI] Transformation - 4")
    twitter_transform(spark, args.src, args.dest, args.process_date)

'''
if __name__=="__main__":
	spark = SparkSession.builder.appName("twitter_transformation").getOrCreate()
	df = spark.read.json("/opt/bitnami/datalake/twitter_aluraonline")
	df.printSchema()
	df.show()
'''