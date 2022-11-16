import os
from datetime import datetime
from pprint import pprint

import bitdotio
from dotenv import load_dotenv
from flask_apscheduler import APScheduler

load_dotenv()
scheduler = APScheduler()

# b = bitdotio.bitdotio(os.environ.get("BITIO"))

# create_table_sql = """
#     CREATE TABLE IF NOT EXISTS test (
#       time varchar
#     )
#     """


# @scheduler.task("interval", id="do_job_1", seconds=3, misfire_grace_time=900)
# def job1():
#     now = str(datetime.now())
#     print(f"Job executing at {now}")

#     # Connect to a database by name
#     with b.get_connection("jayloofah/carbonation") as conn:
#         cursor = conn.cursor()
#         cursor.execute(create_table_sql)

#         insert_table_sql = f"""
#             INSERT INTO test (time)
#             VALUES ('{now}')
#         """
#         cursor.execute(insert_table_sql)


# @scheduler.task("interval", id="do_job_2", seconds=20, misfire_grace_time=900)
# def job2():
#     with b.get_connection("jayloofah/carbonation") as conn:
#         cur = conn.cursor()
#         cur.execute("SELECT * from test")
#         pprint(cur.fetchone())


# cron examples
# @scheduler.task('cron', id='do_job_2', minute='*')
# def job2():
#     print('Job 2 executed')


# @scheduler.task('cron', id='do_job_3', week='*', day_of_week='sun')
# def job3():
#     print('Job 3 executed')

# scheduler.start()
