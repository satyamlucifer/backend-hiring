from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Job, JobType, JobStatus, CustomerType, Site, Worker
from .tasks import process_job
from .models import Site, JobType

class JobView(APIView):
    def post(self, request):
        try:
            data = request.data
            job_type = JobType.objects.get(id=data['job_type_id'])
            customer_type = CustomerType.objects.get(id=data['customer_type_id'])
            site = Site.objects.get(id=data['site_id'])

            worker = Worker.objects.filter(
                job_type=job_type,
                customer_type=customer_type,
                is_busy=False
            ).first()

            if worker is None:
                return Response({"status": "No available worker found."})

            job = Job.objects.create(
                site=site,
                job_type=job_type,
                customer_type=customer_type,
                status=JobStatus.PENDING
            )

            process_job.delay(worker.id, job.id)

            return Response({"status": "Job created and queued", "job_id": job.id})
        except Exception as e:
            return Response(
                {"error": "An error occurred while processing your request.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class SiteJobsView(APIView):
    def get(self, request, site_id):
        try:
            site = Site.objects.get(id=site_id)
            jobs = Job.objects.filter(site=site)
            job_list = [{"job_id": job.id, "status": JobStatus.get_status_name(job.status), "job_type": job.job_type.name} for job in jobs]
            return Response({"site_id": site.id, "jobs": job_list})
        except Site.DoesNotExist:
            return Response(
                {"error": "Site does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )

class WorkerStatusView(APIView):
    def get(self, request):
        workers = Worker.objects.all()
        worker_status = [{"worker_id": worker.id, "name": worker.name, "is_busy": worker.is_busy} for worker in workers]
        return Response({"workers": worker_status})

class CancelJobView(APIView):
    def post(self, request, job_id):
        try:
            job = Job.objects.get(id=job_id)
            job.status = JobStatus.CANCELLED
            job.save()
            return Response({"status": "Job cancelled successfully."})
        except Job.DoesNotExist:
            return Response(
                {"error": "Job does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )

class SitesView(APIView):
    def get(self, request):
        sites = Site.objects.all()
        site_data = [{"site_id": site.id, "name": site.name, "domain": site.domain} for site in sites]
        return Response({"sites": site_data})

class JobStatusFilterView(APIView):
    def get(self, request, status):
        try:
            status_value = JobStatus.PENDING if status == 'pending' else JobStatus.COMPLETED if status == 'completed' else JobStatus.CANCELLED
            jobs = Job.objects.filter(status=status_value)
            job_list = [{"job_id": job.id, "site": job.site.name, "job_type": job.job_type.name} for job in jobs]
            return Response({"jobs": job_list})
        except Exception as e:
            return Response(
                {"error": "An error occurred while processing your request.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class JobStatisticsView(APIView):
    def get(self, request):
        try:
            total_jobs = Job.objects.count()
            completed_jobs = Job.objects.filter(status=JobStatus.COMPLETED).count()
            pending_jobs = Job.objects.filter(status=JobStatus.PENDING).count()

            # Add additional statistics as needed
            return Response({
                "total_jobs": total_jobs,
                "completed_jobs": completed_jobs,
                "pending_jobs": pending_jobs
            })
        except Exception as e:
            return Response(
                {"error": "An error occurred while processing your request.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class AssignWorkerView(APIView):
    def post(self, request, job_id, worker_id):
        try:
            job = Job.objects.get(id=job_id)
            worker = Worker.objects.get(id=worker_id)

            if worker.is_busy:
                return Response({"status": "Worker is currently busy."}, status=status.HTTP_400_BAD_REQUEST)

            job.status = JobStatus.PENDING
            job.save()

            # Manually assign the worker to the job
            process_job.delay(worker.id, job.id)

            return Response({"status": "Job assigned to worker and queued for processing."})
        except (Job.DoesNotExist, Worker.DoesNotExist) as e:
            return Response(
                {"error": f"Error occurred: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

class UpdateWorkerAvailabilityView(APIView):
    def post(self, request, worker_id):
        try:
            worker = Worker.objects.get(id=worker_id)
            worker.is_busy = False
            worker.save()
            return Response({"status": f"Worker {worker.name} marked as available."})
        except Worker.DoesNotExist:
            return Response(
                {"error": "Worker does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )

class JobExecutionTimeView(APIView):
    def get(self, request, job_id):
        try:
            job = Job.objects.get(id=job_id)
            execution_time = job.job_type.execution_time  # or you could store the start/end time to calculate
            return Response({"job_id": job.id, "execution_time": execution_time})
        except Job.DoesNotExist:
            return Response(
                {"error": "Job does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )

class JobStatusView(APIView):
    def get(self, request, job_id):
        try:
            job = Job.objects.get(id=job_id)
            return Response({"job_id": job.id, "job_type_name": job.job_type.name, "status": JobStatus.get_status_name(job.status)})
        except Job.DoesNotExist:
            return Response(
                {"error": "Job does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )