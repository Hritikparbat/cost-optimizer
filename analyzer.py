import boto3
from datetime import datetime, timedelta

cloudwatch = boto3.client('cloudwatch')
ec2 = boto3.client('ec2')

INSTANCE_ID = "i-0e0273043f6e02863"


def get_cpu_utilization(instance_id):
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=10)

    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
        Dimensions=[
            {'Name': 'InstanceId', 'Value': instance_id}
        ],
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=['Average']
    )

    datapoints = response['Datapoints']

    if not datapoints:
        print("No data found")
        return None

    datapoints.sort(key=lambda x: x['Timestamp'], reverse=True)
    return datapoints[0]['Average']


def stop_instance(instance_id):
    print(f"Stopping instance {instance_id}")
    ec2.stop_instances(InstanceIds=[instance_id])


def lambda_handler(event, context):
    cpu = get_cpu_utilization(INSTANCE_ID)

    if cpu is None:
        return

    print(f"CPU Utilization: {cpu}")

    if cpu < 10:
        print("Instance is idle → stopping")
        stop_instance(INSTANCE_ID)
    else:
        print("Instance is active")






"""

import boto3
from datetime import datetime, timedelta

# Create AWS clients
cloudwatch = boto3.client('cloudwatch')
ec2 = boto3.client('ec2')

# Replace with your instance ID
INSTANCE_ID = "i-0a7ef1d0a5d3a8823"

def get_cpu_utilization(instance_id):
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=10)

    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
        Dimensions=[
            {'Name': 'InstanceId', 'Value': instance_id}
        ],
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=['Average']
    )

    datapoints = response['Datapoints']

    if not datapoints:
        print("No data found")
        return None

    datapoints.sort(key=lambda x: x['Timestamp'], reverse=True)
    avg_cpu = datapoints[0]['Average']
    return avg_cpu


def analyze_instance():
    cpu = get_cpu_utilization(INSTANCE_ID)

    if cpu is None:
        return

    print(f"CPU Utilization: {cpu:.2f}%")

    if cpu < 10:
        confirm = input("Do you want to stop the instance? (yes/no): ")
        if confirm.lower() == "yes":
            stop_instance(INSTANCE_ID)
    else:
        print("✅ Instance is ACTIVE")

def stop_instance(instance_id):
    print(f"🛑 Stopping instance {instance_id}...")
    
    response = ec2.stop_instances(
        InstanceIds=[instance_id]
    )
    
    print("✅ Stop request sent successfully")  

if __name__ == "__main__":
    analyze_instance()

"""
