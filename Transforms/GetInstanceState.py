#!/usr/bin/python
# Instance Information

from MaltegoTransform import *
import sys
import boto.ec2
from init import load_credentials

creds = load_credentials()
REGION = creds[2]

instance_check = sys.argv[1]

m = MaltegoTransform()

try:
    conn = boto.ec2.connect_to_region(REGION, aws_access_key_id=creds[0], aws_secret_access_key=creds[1])
    instances = conn.get_all_instances()

    for x in range(0, len(instances)):
        instance = instances[x].instances
        if str(instance_check) in str(instance):
            ent = m.addEntity('matterasmus.AmazonEC2InstanceState', str(instance[0].state))
            ent.addAdditionalFields("variable", "State", True, str(instance[0].state))
        else:
            pass
    else:
        m.addUIMessage("Completed")
except Exception as e:
    m.addUIMessage(str(e))

m.returnOutput()
