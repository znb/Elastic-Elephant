#!/usr/bin/python
# Get all the instances in our Region

from MaltegoTransform import *
import sys
import boto3

# Get our region name from Maltego
REGION = sys.argv[1]

m = MaltegoTransform()

try:
    client = boto3.resource('ec2', region_name=REGION)
    instances = client.instances.all()

    for instance in instances:
        ent = m.addEntity('matterasmus.AmazonEC2Instance', instance.tags[0].get("Value"))
        ent.addAdditionalFields("Instance Id", "InstanceId", "strict", str(instance.id))
    else:
        m.addUIMessage("Completed.")
except Exception as e:
    m.addUIMessage(str(e))

m.returnOutput()
