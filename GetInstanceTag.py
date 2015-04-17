#!/usr/bin/python
# Get the Instance tag/name

from MaltegoTransform import *
import sys
import boto.ec2
from init import load_credentials

creds = load_credentials()
REGION = creds[2]

amazon_id = sys.argv[1]
searchquery = "[Instance:" + amazon_id + "]"

m = MaltegoTransform()

try:
    conn = boto.ec2.connect_to_region(REGION, aws_access_key_id=creds[0], aws_secret_access_key=creds[1])
    reservations = conn.get_all_reservations()
    instance_list = []
    for x in range(0, len(reservations)):
        instances = reservations[x].instances
        if str(searchquery) in str(instances):
            instances = reservations[x].instances
            ent = m.addEntity("matterasmus.EC2InstanceName", str(instances[0].tags['Name']))
            ent.addAdditionalFields("Instance Name", "InstanceName", "strict", str(instances[0].tags['Name']))
            m.addUIMessage("Completed")
        else:
            pass
    else:
        m.addUIMessage("Completed")
except Exception as e:
    m.addUIMessage(str(e))

m.returnOutput()
