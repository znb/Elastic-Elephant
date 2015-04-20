#!/usr/bin/python
# Instance Information

from MaltegoTransform import *
import sys
import boto.ec2
from init import load_credentials

creds = load_credentials()
REGION = creds[2]

amazon_id = sys.argv[1]
searchquery = "[Instance:" + amazon_id + "]"

m = MaltegoTransform()

# Get Instance Info
try:
    conn = boto.ec2.connect_to_region(REGION, aws_access_key_id=creds[0], aws_secret_access_key=creds[1])
    reservations = conn.get_all_instances()
    for x in range(0, len(reservations)):
        instance = reservations[x].instances
        if str(searchquery) in str(instance):
            ent = m.addEntity('matterasmus.AmazonEC2InstanceType', str(instance[0].instance_type))
            ent.addAdditionalFields("variable", "Instance Type", True, str(instance[0].instance_type))
            ent = m.addEntity('matterasmus.EC2InstanceName', str(instance[0].tags['Name']))
            ent.addAdditionalFields("variable", "Instance Name", True, str(instance[0].tags['Name']))
            ent = m.addEntity('matterasmus.AmazonEC2InstanceState', str(instance[0].state))
            ent.addAdditionalFields("variable", "State", True, str(instance[0].state))
            ent = m.addEntity('matterasmus.AmazonEC2Subnet', str(instance[0].subnet_id))
            ent.addAdditionalFields("variable", "Subnet ID", True, str(instance[0].subnet_id))
            ent = m.addEntity('matterasmus.AmazonEC2VPC', str(instance[0].vpc_id))
            ent.addAdditionalFields("variable", "VPC ID", True, str(instance[0].vpc_id))
            ent = m.addEntity('maltego.IPv4Address', str(instance[0].ip_address))
            ent.addAdditionalFields("variable", "IP Address", True, str(instance[0].ip_address))
            ent = m.addEntity('maltego.IPv4Address', str(instance[0].private_ip_address))
            ent.addAdditionalFields("variable", "Private IP Address", True, str(instance[0].private_ip_address))
            ent = m.addEntity('matterasmus.AmazonEC2Platform', str(instance[0].platform))
            ent.addAdditionalFields("variable", "Platform", True, str(instance[0].platform))
            ent = m.addEntity('matterasmus.AmazonEC2LaunchTime', str(instance[0].launch_time))
            ent.addAdditionalFields("variable", "Launch Time", True, str(instance[0].launch_time))
            ent = m.addEntity('matterasmus.AmazonEC2Key', str(instance[0].key_name))
            ent.addAdditionalFields("variable", "SSH Key", True, str(instance[0].key_name))
            # Get Security Group Information
            group_nums = len(instance[0].groups)
            group_id = instance[0].groups[0].id
            sg_name = conn.get_all_security_groups(group_ids=group_id)[0]
            sec_rules = conn.get_all_security_groups(group_ids=group_id)[0].rules
            ent = m.addEntity('matterasmus.AmazonEC2SecurityGroupName', str(sg_name).split(":")[1])
            ent.addAdditionalFields("GroupID", "Group ID", "strict", str(group_id))
            m.addUIMessage("Completed: Instance Info Fetch")
        else:
            pass
    else:
        m.addUIMessage("Completed")
except Exception as e:
    m.addUIMessage(str(e))

m.returnOutput()
