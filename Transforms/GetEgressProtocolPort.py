#!/usr/bin/python
# Pull all the egress rules for a Security Group

from MaltegoTransform import *
import boto.ec2
import sys
from init import load_credentials

creds = load_credentials()
REGION = creds[2]

m = MaltegoTransform()
m.parseArguments(sys.argv)
sec_group = m.getVar("GroupID")

try:
    conn = boto.ec2.connect_to_region(REGION, aws_access_key_id=creds[0], aws_secret_access_key=creds[1])

    reservations = conn.get_all_instances()

    for i in reservations:
        group_nums = len(i.instances[0].groups)
        for z in range(group_nums):
            group_id = i.instances[0].groups[z].id
            sg_name = conn.get_all_security_groups(group_ids=group_id)[0]
            if str(group_id) == str(sec_group):
                egress_rules = conn.get_all_security_groups(group_ids=group_id)[0].rules_egress
                number_of_egress = len(egress_rules)
                for k in range(number_of_egress):
                    ent = m.addEntity('matterasmus.AmazonEC2SecurityGroupPP', str(conn.get_all_security_groups(group_ids=group_id)[0].rules_egress[k]))
                    ent.addAdditionalFields("GroupID", "Group ID", "strict", str(group_id))

    m.addUIMessage("Completed.")

except Exception as e:
    m.addUIMessage(str(e))


m.returnOutput()
