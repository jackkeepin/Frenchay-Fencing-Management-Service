from job.models import Job
from bson import ObjectId

def get_all_jobs():
    jobs = Job.objects.all().order_by('date_of_job')
    return jobs

def get_single_job(object_id):
    jobresp = Job.objects.get(_id=ObjectId(object_id))
    return jobresp