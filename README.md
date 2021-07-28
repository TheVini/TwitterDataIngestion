# Twitter Data Ingestion

## 1. Fluxogram Purpose

<details><summary>Show Fluxogram</summary>
<p align="center">
  <img src="https://github.com/TheVini/TwitterDataIngestion/blob/master/src_imgs/flow.png" width="350">
</p>
</details>

## 2. How to Use It?

### 2.1. Setup your Twitter API and Account
<details><summary>Show me How To Setup the Twitter API</summary>
	<ul>
	<li> 1. Create a Twitter Account at: https://twitter.com
	<li> 2. Access https://developer.twitter.com/en and fill the form on "Basic Info Tab" in order to use Twitter API with following info:
		<ul>
			<li> On "Which best describes you?", choose "Academic", afterwards choose "Student", and "Get Started".
			<li> At the new page, confirm your username, email, and individual developer account.
			<li> On the last field, fill it with your name, country, and programming level (choose anyone, no matter which one you will choose), and "Next".
		</ul>
	<li> 3. Next pages are really import because they describe the usage purpose of your Twitter API. On "Intended Use" answer the following questions with which respectives sentences:
		<ul>
			<li> On "How will you use the Twitter API or Twiiter Data", describe "I am attending a course about introduction to data pipelines from a Brazilian training company called {Course Name}. I would like to have access to the Twitter API to learn about data pipelines and the process of extraction, load, and transformation of data as I will be using the Twitter data to build my first data pipeline. In this project, we are building an Apache Airflow job that daily will request tweets and users details related to conversations with the AluraOnline Twitter profile. This data will be processed using an Apache Spark job that will format it, allowing the extraction of information like the number of messages per day."
			<li> On "Are you planning to analyze Twitter Data?", describe "I will be extracting tweets and users data, analysing the number of messages and conversations exchanged with the AluraOnline profile and the number of unique users interacting per day."
			<li> Turn off the following Radio Buttons:
			<ul>
				<li> "Will your app use Tweet, Retweet, Like, Follow, or Direct Message functionality?"
				<li> "Do you plan to display Tweets or aggregate data about Twitter content outside Twitter?"
				<li> "Will your product, service, or analysis make Twitter content or derived information available to a government entity?"
			</ul>
		</ul>
	<li> 4. On "Review Tab", check your answers and click on "Next" button.
	<li> 5. On "Terms Tab", read the "Developer Agreement", and click on the "Submit Application" button.
	<li> 6. Wait for Twitter Approval, which can takes from some seconds to days.
	<li> 7. After Twitter Approval, go to Twitter API main menu and click on the "Create Project" button.
		<ul>
			<li> Name your project, and "Next".
			<li> On "Which best describes you?", choose "Student", and "Next".
			<li> On "Describe your new project", fill the field with "I will build my first data pipeline extracting data from Twitter to analyse the number of messages per day between the AluraOnline profile and other users.", and "Next".
			<li> On "Last Step, name your App", name your app (this name can be the same as that one on the first field), and "Complete".
		</ul>
	<li> 8. At the new page, click on "Add app" button.
	<li> 9. Name your app (suggestion: different name from previously), and "Next".
	<li> 10. At the new page, store API Key, API Secret Key, and Bearer Token in a safe place.
	</ul>
</details>

### 2.2. Setup the Project
<details><summary>Show me How To Setup the Project</summary>
	<ul>
		<li> Ensure you have docker installed on your computer, otherwise do it https://www.docker.com/products/docker-desktop. Note: WSL installation may be necessary.
		<li> On git bash, "git clone git@github.com:TheVini/TwitterDataIngestion.git"
		<li> On git bash, at the project root, run the following commands and go to drink a brazilian coffee:
		<ul>
			<blockquote> echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env </blockquote>
			<blockquote> docker-compose up airflow-init </blockquote>
			<blockquote> docker-compose up </blockquote>
		</ul>
		<li> Access the WebServer container by the CLI (there is a button on Docker Desktop for this purpose, on "Containers/App tab"), then run the following command:
		<ul>
			<blockquote> rm -rf datalake/* && tar -xzvf java/jre-8u301-linux-x64.tar.gz </blockquote>
		</ul>
		<li> Access the WebServer container by the browser (there is a button on Docker Desktop for this purpose, on "Containers/App tab"), then run the following command:
			<ul>
				<li> Username "airflow", password "airflow", then "Sign In".
				<li> On "Admin" button on the upper bar, access the "Connections" menu.
				<li> Click on the "+" blue button ("Add a new record").
					<ul>
						<li> conn_id: twitter_deafult
						<li> Conn Type: http
						<li> Host: https://api.twitter.com
						<li> Extra: {"Authorization": "Bearer [type here your bearer Token generated for your twitter API at the step <a href="https://github.com/TheVini/TwitterDataIngestion/blob/master/README.md#21-setup-your-twitter-api-and-account">2.1.10</a>]"}
						<li> Then, "Save".
					</ul>
				<li> Example:
					<p align="center">
					  <img src="https://github.com/TheVini/TwitterDataIngestion/blob/master/src_imgs/twitter_connection_example.png" height="400">
					</p>
				<li> Again, click on the "+" blue button ("Add a new record").
					<ul>
						<li> conn_id: spark_default
						<li> Conn Type: spark
						<li> Host: local
						<li> Extra: {"spark-home": "/home/airflow/.local/lib/python3.6/site-packages/pyspark"}
						<li> Then, "Save".
					</ul>
			</ul>
	</ul>
</details>

### 2.3. Run the Project
<details><summary>Show me How To Run the Project</summary>
	<ul>
		<li> On your browser, open the Airflow webserver DAGs Tab, and turn on the "twitter_dag".
			<p align="center">
			  <img src="https://github.com/TheVini/TwitterDataIngestion/blob/master/src_imgs/twitter_dag_example.PNG" height="400">
			</p>
		<li> Access the "twitter_dag".
		<li> It should looks similar to this image, but dates may vary.
			<p align="center">
			  <img src="https://github.com/TheVini/TwitterDataIngestion/blob/master/src_imgs/twitter_dag_success.PNG" height="300">
			</p>
		<li> Access your project directory from your computer and go to "datalake" folder, it should have two folders: "bronze", and "silver".
		<li> In order to create the "gold" folder, on airflow webserver CLI, run the command: /home/airflow/.local/lib/python3.6/site-packages/pyspark/bin/spark-submit /opt/airflow/spark/insight_tweet.py
		<li> In order to visualize the "gold" folder content, run the following commands:
			<ul>
				<blockquote> /home/airflow/.local/lib/python3.6/site-packages/pyspark/bin/spark-submit</blockquote>
				<blockquote> df = spark.read.json("/opt/airflow/datalake/gold/twitter_insight_tweet")</blockquote>
				<blockquote> df.show()</blockquote>
			</ul>
	</ul>
</details>

**Repository author's Linkedin profile**: https://bit.ly/3tsOnU3
