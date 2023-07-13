from google.cloud import pubsub_v1
import json

# TODO(developer)
project_id = "gmail-test-363715"
topic_id = "PythonTestCreationTopic"


# with open('token.json', 'r') as token:
#     tv = json.load(token)
#     project_id = tv[]
            
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

topic = publisher.create_topic(request={"name": topic_path})

print(f"Created topic: {topic.name}")