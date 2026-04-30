import subprocess

from prefect import flow, get_run_logger, task
from task.extract import fetch_dpwh_data
from task.load_to_s3 import upload_to_s3
from task.load_to_snowflake import load_to_snowflake


@task(name="extract-and-upload", retries=3, retry_delay_seconds=60)
def extract_task() -> None:
    records = fetch_dpwh_data()
    upload_to_s3(records)


@task(name="load-to-snowflake", retries=2, retry_delay_seconds=30)
def snowflake_task() -> None:
    load_to_snowflake()


@task(name="run-dbt-models", retries=1, retry_delay_seconds=30)
def dbt_task() -> None:
    logger = get_run_logger()
    cwd = "dpwh_projects_transform"

    for cmd in [["dbt", "deps"], ["dbt", "run"]]:
        result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
        logger.info(result.stdout)
        if result.returncode != 0:
            logger.error(result.stderr)
            raise Exception(f"{' '.join(cmd)} failed:\n{result.stderr}")


@flow(name="DPWH-Projects-Pipeline")
def dpwh_flow() -> None:
    extract_task()
    snowflake_task()
    dbt_task()


if __name__ == "__main__":
    dpwh_flow()
