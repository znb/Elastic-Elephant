#!/usr/bin/python
# Pull all Security Group rule information for a Security Group

from MaltegoTransform import *
import boto.ec2
from init import load_credentials

creds = load_credentials()
REGION = creds[2]

sec_group = sys.argv[1]

m = MaltegoTransform()

try:
    conn = boto.ec2.connect_to_region(REGION, aws_access_key_id=creds[0], aws_secret_access_key=creds[1])

    reservations = conn.get_all_instances()

    for i in reservations:
        group_nums = len(i.instances[0].groups)
        for z in range(group_nums):
            group_id = i.instances[0].groups[z].id
            sg_name = conn.get_all_security_groups(group_ids=group_id)[0]
            # Match on our search string
            if str(sg_name).split(":")[1] == str(sec_group):
                # Security Group Ingress Rules
                ingress= m.addEntity("matterasmus.AmazonEC2IngressRules", "Ingress Rules")
                ingress.addAdditionalFields("IngressRules", "Ingress Rules", "strict", "Ingress Rules")

                # Security Group Egress Rules
                egress = m.addEntity("matterasmus.AmazonEC2EgressRules", "Egress Rules")
                egress.addAdditionalFields("EgressRules", "Egress Rules", "strict", "Egress rules")


    m.addUIMessage("Completed.")

except Exception as e:
    m.addUIMessage(str(e))


m.returnOutput()
