from .models import Job, JobType, JobStatus, CustomerType, Site, Worker
import random
from .models import Site, JobType, UserRecords
from django.utils import timezone
from faker import Faker


def create_dummy_data():
    sites = []
    for i in range(10):
        site = Site.objects.create(
            name=f"Site {i+1}",
            record_capicity=random.randint(100,10000)*i,
            description=f"Description {i+1}",
            url=f"url {i+1}",
            domain=f"domain {i+1}",
        )
        sites.append(site)

    job_types = []
    execution_times = [0.001, 0.01, 0.1, 1, 10]
    for i in range(5):
        job_type = JobType.objects.create(
            name=f"JobType {i+1}",
            execution_time=random.choice(execution_times)
        )
        job_types.append(job_type)

    customer_types = []
    for i in range(3):
        customer_type = CustomerType.objects.create(
            name=f"CustomerType {i+1}",
            record_volume=random.choice([10000, 500, 50000])
        )
        customer_types.append(customer_type)

    workers = []
    for job_type in job_types:
        for customer_type in customer_types:
            worker = Worker.objects.create(
                name=f"Worker {job_type.name[:3]}-{customer_type.name[:3]}",  # Optional: a unique name based on job_type and customer_type
                job_type=job_type,
                customer_type=customer_type,
                is_busy=False
            )
            workers.append(worker)

    jobs = []
    for i in range(10):
        job = Job.objects.create(
            site=random.choice(sites),
            job_type=random.choice(job_types),
            customer_type=random.choice(customer_types),
            status=JobStatus.PENDING,
            created_at=timezone.now()
        )
        jobs.append(job)

    print("Dummy data created successfully.")

fake = Faker()

RECORD_CAPACITY_LOW = 1
RECORD_CAPACITY_MEDIUM = 2
RECORD_CAPACITY_HIGH = 3

def create_user_records():
    sites = Site.objects.all()

    # Record ranges for each capacity level
    record_ranges = {
        RECORD_CAPACITY_LOW: (500, 10000),
        RECORD_CAPACITY_MEDIUM: (10000, 50000),
        RECORD_CAPACITY_HIGH: (50000, 200000)
    }

    for site in sites:
        # Fetch the capacity level for the site
        num_records = site.record_capicity  # Should be one of the predefined constants
        

        
        for _ in range(num_records):
            # Generate random data for each user record

            phone_no = fake.phone_number()[:15]

            user_record = UserRecords.objects.create(
                site=site,
                name=fake.name(),
                email=fake.email(),
                phone=phone_no,
                address=fake.address(),
                country=fake.country(),
                state=fake.state(),
                city=fake.city(),
                pincode=fake.zipcode(),
                dob=fake.date_of_birth(),
                is_active=random.choice([True, False])  # Random active/inactive status
            )
            
            # Print confirmation for each user created
            print(f"Created user record for {user_record.name} at {site.name} with email {user_record.email}")

    print("User records creation completed.")