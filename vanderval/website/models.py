from django.db import models
from datetime import datetime
from django_unixdatetimefield import UnixDateTimeField


# Create your models here.
class Site(models.Model):
    RECORD_CAPACITY_LOW = 1  # user records between 500-10000
    RECORD_CAPACITY_MEDIUM = 2  # user records between 10000-50000
    RECORD_CAPACITY_HIGH = 3  # user records between 50000-200000

    RECORD_CAPACITY_CHOICES = (
        (RECORD_CAPACITY_LOW, "Low"),
        (RECORD_CAPACITY_MEDIUM, "Medium"),
        (RECORD_CAPACITY_HIGH, "High"),
    )

    name = models.CharField(max_length=100)
    domain = models.URLField()
    url = models.URLField()
    description = models.TextField()
    record_capicity = models.IntegerField(choices=RECORD_CAPACITY_CHOICES)


# you can choose to reuse the User model from django.contrib.auth.models
class UserRecords(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    dob = models.DateField()
    is_active = models.BooleanField(default=True)  # do not count for active records if false


class JobType(models.Model):
    name = models.CharField(max_length=50)
    execution_time = models.DecimalField(max_digits=10, decimal_places=3)

    def __str__(self):
        return self.name

class CustomerType(models.Model):
    name = models.CharField(max_length=50)
    record_volume = models.IntegerField()

    def __str__(self):
        return self.name
    
class JobStatus:
    PENDING = 1
    IN_PROGRESS=2
    COMPLETED = 3
    CANCELLED = 4
    choices = (
        (PENDING, 'Pending'),
        (IN_PROGRESS, 'IN_PROGRESS'),
        (COMPLETED, 'Completed'),
        (CANCELLED, 'Cancelled'),
    )
    @classmethod
    def get_status_name(cls, status_value):
        """Return the display name for a given status value."""
        status_dict = dict(cls.choices)
        return status_dict.get(status_value, 'Unknown')
    
class Job(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    job_type = models.ForeignKey(JobType, on_delete=models.CASCADE)
    customer_type = models.ForeignKey(CustomerType, on_delete=models.CASCADE)
    status = models.IntegerField(choices=JobStatus.choices, blank=False, default=JobStatus.PENDING)
    created_at = UnixDateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Job for {self.site.name} ({self.job_type.name})"
    

class Worker(models.Model):
    name = models.CharField(max_length=100)
    job_type = models.ForeignKey(JobType, on_delete=models.CASCADE)
    customer_type = models.ForeignKey(CustomerType, on_delete=models.CASCADE)
    is_busy = models.BooleanField(default=False)  # To check if the worker is busy

    def __str__(self):
        return self.name