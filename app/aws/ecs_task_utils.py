import boto3

from dotenv import load_dotenv
load_dotenv()


def get_public_ip_of_task(task_arn, cluster_name):
    ecs_client = boto3.client('ecs', region_name='ap-south-1')
    ec2_client = boto3.client('ec2', region_name='ap-south-1')

    try:
        task_and_cluster_arn = extract_task_and_cluster_arn(task_arn, cluster_name)
        # Step 1: Describe the ECS task to get network interface ID
        response = ecs_client.describe_tasks(
            cluster=task_and_cluster_arn['clusterArn'],
            tasks=[task_and_cluster_arn['taskArn']]
        )
        
        tasks = response.get('tasks', [])
        if not tasks:
            return {'error': 'Task not found'}
        
        # Step 2: Extract network interface ID from the task
        network_interfaces = tasks[0].get('containers', [])[0].get('networkInterfaces', [])
        if not network_interfaces:
            return {'error': 'No network interfaces found for the task'}
        
        network_interface_id = network_interfaces[0].get('networkInterfaceId')

        # Step 3: Describe the network interface using EC2 client
        network_interface_response = ec2_client.describe_network_interfaces(
            NetworkInterfaceIds=[network_interface_id]
        )

        # Step 4: Get the public IP address from the network interface details
        network_interface = network_interface_response.get('NetworkInterfaces', [])[0]
        public_ip = network_interface.get('Association', {}).get('PublicIp')

        if public_ip:
            return {'public_ip': public_ip}
        else:
            return {'error': 'No public IP found for the network interface'}

    except Exception as e:
        return {'error': str(e)}


def extract_task_and_cluster_arn(response):
    # Parse the response to get task details
    tasks = response.get('tasks', [])
    
    if not tasks:
        return {'error': 'No tasks found in the response'}
    
    task = tasks[0]  # Assuming you want to extract from the first task in the list
    task_arn = task.get('taskArn')
    cluster_arn = task.get('clusterArn')
    
    return {
        'taskArn': task_arn,
        'clusterArn': cluster_arn
    }