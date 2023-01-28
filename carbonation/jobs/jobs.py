from huey import crontab

from carbonation.app import huey


@huey.periodic_task(crontab(minute=0, hour="*/4"))
def cron_gen_bert():
    import subprocess

    subprocess.run(["python", "-m" "carbonation.jobs.bert_job"], stdout=subprocess.PIPE)
