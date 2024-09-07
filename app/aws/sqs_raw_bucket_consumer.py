# make a consumer for listening the queue and lauch a ECS container based on this

def listen_queue():
    """
    1. When an event will hit backend app, consumer it will check:
        - s3 object info and save it to DB.
        - after that it will launch docker container on aws ecs using lauch_container() function.
    """
    
    pass