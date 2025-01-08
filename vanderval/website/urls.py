from django.urls import path
from .views import  *


urlpatterns = [
# Job-related APIs
    path('job/', JobView.as_view(), name='create-job'),  # Create a new job
    path('job/status/<int:job_id>/', JobStatusView.as_view(), name='job-status'),  # Get status of a specific job
    path('site/<int:site_id>/jobs/', SiteJobsView.as_view(), name='site-jobs'),  # Get all jobs for a site
    path('job/cancel/<int:job_id>/', CancelJobView.as_view(), name='cancel-job'),  # Cancel a job
    
    # Worker-related APIs
    path('workers/status/', WorkerStatusView.as_view(), name='worker-status'),  # Get all workers' status
    path('worker/assign/<int:job_id>/<int:worker_id>/', AssignWorkerView.as_view(), name='assign-worker'),  # Assign worker to a job
    path('worker/availability/<int:worker_id>/', UpdateWorkerAvailabilityView.as_view(), name='update-worker-availability'),  # Update worker's availability

    # Site-related APIs
    path('sites/', SitesView.as_view(), name='sites-list'),  # Get all sites
    
    # Job Filtering and Statistics
    path('jobs/status/<str:status>/', JobStatusFilterView.as_view(), name='filter-jobs-by-status'),  # Get jobs by status (pending/completed/cancelled)
    path('jobs/statistics/', JobStatisticsView.as_view(), name='job-statistics'),  # Get job statistics
    path('job/execution-time/<int:job_id>/', JobExecutionTimeView.as_view(), name='job-execution-time'),  # Get the execution time for a job    
]
