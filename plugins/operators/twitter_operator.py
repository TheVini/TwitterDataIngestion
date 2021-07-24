import json
import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from os.path import join

from airflow.models import DAG, BaseOperator, TaskInstance
from airflow.utils.decorators import apply_defaults
from hooks.twitter_hook import TwitterHook


class TwitterOperator(BaseOperator):

    template_fields = [
        "query",
        "file_path",
        "start_time",
        "end_time"
    ]

    @apply_defaults
    def __init__(
        self,
        query,
        file_path,
        conn_id = None,
        start_time = None,
        end_time = None,
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.query = query
        self.file_path = file_path
        self.conn_id = conn_id
        self.start_time = start_time
        self.end_time = end_time

    def create_parent_folder(self):
        print("***************[LOG VINI] Class TwitterOperator - Method create_parent_folder - 1")
        Path(Path(self.file_path).parent).mkdir(parents=True, exist_ok=True)
        print("***************[LOG VINI] Class TwitterOperator - Method create_parent_folder - 2")

    def execute(self, context):
        print("***************[LOG VINI] Class TwitterOperator - Method execute - 1")
        hook = TwitterHook(
            query=self.query,
            conn_id=self.conn_id,
            start_time=self.start_time,
            end_time=self.end_time
        )
        print("***************[LOG VINI] Class TwitterOperator - Method execute - 2")
        '''
        for pg in hook.run():
            print(json.dumps(pg, indent=4, sort_keys=True))
        '''
        print("***************[LOG VINI] Class TwitterOperator - Method execute - 3")
        self.create_parent_folder()
        print("***************[LOG VINI] Class TwitterOperator - Method execute - 4")
        with open(self.file_path, "w") as output_file:
            for pg in hook.run():
                json.dump(pg, output_file, ensure_ascii=False)
                output_file.write("\n")
        print("***************[LOG VINI] Class TwitterOperator - Method execute - 5")

if __name__ == "__main__":
    with DAG(dag_id="TwitterTest", start_date=datetime.now()) as dag:
        datalake_path = os.path.join("..","..", "datalake")
        to = TwitterOperator(
            query="AluraOnline",
            file_path=join(
                datalake_path,
                "bronze",
                "twitter_aluraonline",
                "extract_date={{ ds }}",
                "AluraOnline_{{ ds_nodash }}.json"
                ),
            task_id="test_run"
        )
        '''
        to = TwitterOperator(
            query="AluraOnline",
            file_path="AluraOnline_{{ ds_nodash }}",
            task_id="test_run"
        )
        '''
        ti = TaskInstance(task=to, execution_date=datetime.now() - timedelta(days=1))
        #to.execute(ti.get_template_context())
        try:
            ti.run()
        except:
            pass
