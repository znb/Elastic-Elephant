#!/usr/bin/python
# Instance Information

from MaltegoTransform import *
import sys
import boto.ec2
from init import load_credentials


creds = load_credentials()

REGION = sys.argv[1]

m = MaltegoTransform()

try:
    conn = boto.ec2.connect_to_region(REGION, aws_access_key_id=creds[0], aws_secret_access_key=creds[1])
    instances = conn.get_all_instances()

    for x in range(0, len(instances)):
        instance = instances[x].instances
        ent = m.addEntity('matterasmus.AmazonEC2Instance', instance[0].id)
        ent.addAdditionalFields("InstanceID", "Instance ID", "strict", str(instance[0].id))
    else:
        m.addUIMessage("Completed.")
except Exception as e:
    m.addUIMessage(str(e))

m.returnOutput()

