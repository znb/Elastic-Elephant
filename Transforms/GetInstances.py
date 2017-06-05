#!/usr/bin/python
# Get all the instances in our Region

from MaltegoTransform import *
import sys
import boto3

mt = MaltegoTransform()
mt.parseArguments(sys.argv)
REGION = mt.getVar('RegionName')

try:
    client = boto3.resource('ec2', region_name=REGION)
    instances = client.instances.all()

    mt.addUIMessage("Getting instances in " + REGION)
    for instance in instances:
        ent = mt.addEntity('matterasmus.AmazonEC2Instance', instance.tags[0].get("Value"))
        ent.addAdditionalFields("InstanceId", "Instance ID", "strict", str(instance.id))
        ent.addAdditionalFields("InstanceType", "Instance Type", "strict", instance.instance_type)
        ent.addAdditionalFields("KeyName", "Key Name", "strict", instance.key_name)
        ent.addAdditionalFields("PrivateIp", "Private Ip", "strict", instance.private_ip_address)
        ent.addAdditionalFields("RegionName", "Region Name", "strict", REGION)
    else:
        mt.addUIMessage("Completed.")
except Exception as e:
    mt.addUIMessage(str(e))

mt.returnOutput()
