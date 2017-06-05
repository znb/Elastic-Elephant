#!/usr/bin/python
# Get Instance Information

from MaltegoTransform import *
import sys
import boto3

mt = MaltegoTransform()
mt.parseArguments(sys.argv)
REGION = mt.getVar('RegionName')
instance_id = mt.getVar('InstanceId')
mt.addUIMessage("Region: " + REGION)
mt.addUIMessage("Instance: " + instance_id)


# Get Instance Info
try:
    client = boto3.resource('ec2', region_name=REGION)
    instance_info = client.Instance(id=instance_id)
    ent = mt.addEntity('matterasmus.AmazonEC2InstanceType', str(instance_info.instance_type))
    ent.addAdditionalFields("InstanceType", "Instance Type", True, str(instance_info.instance_type))
    ent = mt.addEntity('matterasmus.AmazonEC2Key', str(instance_info.key_name))
    ent.addAdditionalFields("InstanceAccessKey", "Access Key", True, str(instance_info.key_name))
    ent = mt.addEntity('matterasmus.AmazonEC2Subnet', str(instance_info.subnet_id))
    ent.addAdditionalFields("variable", "Subnet ID", True, str(instance_info.subnet_id))
    # Get VPC Information
    vpc_info = client.Vpc(id=instance_info.vpc_id)
    ent = mt.addEntity('matterasmus.AmazonEC2VPC', str(vpc_info.cidr_block))
    ent.addAdditionalFields("VpcId", "VPC ID", True, str(instance_info.vpc_id))
    ent.addAdditionalFields("IPv4Address", "CIDR Block", True, str(vpc_info.cidr_block))
    ent = mt.addEntity('maltego.IPv4Address', str(instance_info.private_ip_address))
    ent.addAdditionalFields("variable", "IP Address", True, str(instance_info.private_ip_address))
    ent = mt.addEntity('maltego.IPv4Address', str(instance_info.public_ip_address))
    ent.addAdditionalFields("variable", "IP Address", True, str(instance_info.public_ip_address))


except Exception as e:
    mt.addUIMessage(str(e))

mt.returnOutput()
