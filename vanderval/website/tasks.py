import logging
from time import sleep
from celery import shared_task
from .models import Job, JobStatus
import time

from .models import Site, UserRecords, Worker

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@shared_task
def task_01(site_id: int):
    TIME_MULTIPLIER = 0.001
    site = Site.objects.get(id=site_id)
    records = UserRecords.objects.filter(site=site)
    for record in records:
        sleep(TIME_MULTIPLIER)
        logger.info("Task 01: {} processed".format(record.name))
    return True

@shared_task
def task_02(site_id: int):
    TIME_MULTIPLIER = 0.01
    site = Site.objects.get(id=site_id)
    records = UserRecords.objects.filter(site=site)
    for record in records:
        sleep(TIME_MULTIPLIER)
        logger.info("Task 02: {} processed".format(record.name))
    return True

@shared_task
def task_03(site_id: int):
    TIME_MULTIPLIER = 0.1
    site = Site.objects.get(id=site_id)
    records = UserRecords.objects.filter(site=site)
    for record in records:
        sleep(TIME_MULTIPLIER)
        logger.info("Task 03: {} processed".format(record.name))
    return True

@shared_task
def task_04(site_id: int):
    TIME_MULTIPLIER = 1
    site = Site.objects.get(id=site_id)
    records = UserRecords.objects.filter(site=site)
    for record in records:
        sleep(TIME_MULTIPLIER)
        logger.info("Task 04: {} processed".format(record.name))
    return True

@shared_task
def task_05(site_id: int):
    TIME_MULTIPLIER = 10
    site = Site.objects.get(id=site_id)
    records = UserRecords.objects.filter(site=site)
    for record in records:
        sleep(TIME_MULTIPLIER)
        logger.info("Task 05: {} processed".format(record.name))
    return True

@shared_task
def process_job(worker_id, job_id):
    try:
        job = Job.objects.get(id=job_id)
        worker = Worker.objects.get(id=worker_id)

        if worker.is_busy:
            return f"Worker {worker.name} is busy. Job {job_id} cannot be processed."

        worker.is_busy = True
        worker.save()

        job.status = JobStatus.IN_PROGRESS
        job.save()

        execution_time = job.job_type.execution_time        
        if execution_time <= 0.001:
            task_01.delay(job.site.id)
        elif execution_time <= 0.01:
            task_02.delay(job.site.id)
        elif execution_time <= 0.1:
            task_03.delay(job.site.id)
        elif execution_time <= 1:
            task_04.delay(job.site.id)
        else:
            task_05.delay(job.site.id)


        job.status = JobStatus.COMPLETED
        job.save()

        worker.is_busy = False
        worker.save()

        logger.info(f"Job {job_id} processed by worker {worker.name} successfully.")
        return True
    except Job.DoesNotExist:
        logger.error(f"Job {job_id} not found.")
        return False
    except Worker.DoesNotExist:
        logger.error(f"Worker {worker_id} not found.")
        return False
