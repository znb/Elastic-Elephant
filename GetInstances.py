#!/usr/bin/python
# Instance Information

from MaltegoTransform import *
import sys
import os
import boto.ec2
from init import load_credentials


creds = load_credentials()
REGION = sys.argv[1]

m = MaltegoTransform()

try:
    conn = boto.ec2.connect_to_region(REGION, aws_access_key_id=creds[0], aws_secret_access_key=creds[1])
    reservations = conn.get_all_reservations()

    for x in range(0, len(reservations)):
        instances = reservations[x].instances
        aid = instances[0].id
        ent = m.addEntity("matterasmus.AmazonEC2Instance", aid)
        ent.addAdditionalFields("Instance ID", "InstanceID", True, str(aid))
    else:
        m.addUIMessage("Completed")
except Exception as e:
    m.addUIMessage(str(e))

m.returnOutput()

