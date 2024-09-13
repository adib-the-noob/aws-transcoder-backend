import time
import boto3

from dotenv import load_dotenv
load_dotenv()

from db import db_dependency
from bson import ObjectId

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_task_public_ip(cluster_name, task_arn):
    # Initialize ECS and EC2 clients
    ecs_client = boto3.client('ecs', region_name='ap-south-1')
    ec2_client = boto3.client('ec2', region_name='ap-south-1')

    try:
        time.sleep(5)
        # Describe the task
        response = ecs_client.describe_tasks(
            cluster=cluster_name,
            tasks=[task_arn]
        )

        # Check if any task is returned
        if not response['tasks']:
            logger.error("No tasks found")
            return None

        # Extract the ENI (Elastic Network Interface) ID from the task details
        attachments = response['tasks'][0].get('attachments', [])
        if not attachments:
            logger.error("No ENI attachment found for the task")
            return None

        # Extract ENI ID from the attachments
        eni_id = None
        for detail in attachments[0].get('details', []):
            if detail.get('name') == 'networkInterfaceId':
                eni_id = detail.get('value')
                break

        if not eni_id:
            logger.error("ENI ID not found in task details")
            return None

        # Describe the network interface using EC2 client
        network_interface = ec2_client.describe_network_interfaces(
            NetworkInterfaceIds=[eni_id]
        )

        # Get the public IP from the network interface
        public_ip = network_interface['NetworkInterfaces'][0].get('Association', {}).get('PublicIp', 'No public IP assigned')

        return public_ip

    except Exception as e:
        logger.error(f"Error while fetching public IP: {str(e)}")
        return None
    
    
def update_task_public_ip(
    id: str,
    task_arn: str,
    cluster_name: str
):
    try:
        public_ip = get_task_public_ip(
            task_arn=task_arn,
            cluster_name=cluster_name
        )
        
        if public_ip:
            db_dependency.container_infos.update_one(
                {"_id": ObjectId(id)},
                {"$set": {"public_ip": public_ip}}
            )
    except Exception as e:
        logger.error(f"Error while updating task public IP: {str(e)}")
        raise e
