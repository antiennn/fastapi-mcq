import os
import subprocess

from prefect.client.schemas.schedules import CronSchedule
from dags.crawl_data import crawl_data
from prefect import flow

@flow
def crawl_data_dag():
    crawl_data()


if __name__ == "__main__":
    schedule = CronSchedule(
        cron="0 0 * * *",
        timezone="Asia/Ho_Chi_Minh"
    )

    # Serve flow với lịch trình
    crawl_data_dag.serve(
        name="flowing",
        schedule=schedule
    )
    crawl_data_dag.deploy(name="crawl_text")