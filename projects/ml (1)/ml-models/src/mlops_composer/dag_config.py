# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.
from datetime import timedelta
from airflow.utils.dates import days_ago

OWNER = 'airflow'
DEPENDS_ON_PAST= False
DAYS_AGO = 2
EMAIL = 'airflow@example.com'
EMAIL_ON_FAILURE = False
EMAIL_ON_RETRY = False
RETRIES = 0
RETRY_DELAY = 1

default_args = {
    'owner': OWNER,
    'depends_on_past': bool(DEPENDS_ON_PAST),
    'email': list(EMAIL),
    'email_on_failure': bool(EMAIL_ON_FAILURE),
    'email_on_retry': bool(EMAIL_ON_RETRY),
    'retries': RETRIES,
    'retry_delay': timedelta(minutes=RETRY_DELAY),
    'start_date': days_ago(DAYS_AGO)
}
