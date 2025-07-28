AWS

**Summary of the Flow**  
**Code**: Your Flask application code.  
**Dockerfile**: Defines how to build a container image of your app.  
**ECR**: You build the image and push it to this private registry.  
**RDS**: A managed database service for your PostgreSQL data.  
**S3**: A managed storage service for your files.  
**ECS**:
    Task Definition: A template specifying the container image, environment variables, and resources.
    Cluster: The logical grouping for your tasks.
    Service: Manages the desired number of tasks and integrates with the Application Load Balancer.  
**Application Load Balancer** (ALB): Publicly accessible endpoint that distributes traffic to your   
Fargate tasks. 

1. Push Docker container to ECR
2. Setup DB and IAM roles
DB - Amazon RDS Postgres
IAM - role with policy for access to s3 buckets
3. VPC and security groups

Configure AWS ECS
4. Task definition 
    - launch type Fargate
    - Role - IAM role
    - Define container
    - CPU and memory

5. Create Cluster - grouping of tasks
6. Create Service 
    - Choose Task
    - Load Balancer - this does health checks
    - Auto scaling 
7. Monitoring - Cloudwatch / Alarm
    
Auto scaling is handled by ECS

