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
                group_nums = len(i.instances[0].groups)
                sg_name = conn.get_all_security_groups(group_ids=group_id)[0]
                # Security Group Ingress Rules
                sec_rules = conn.get_all_security_groups(group_ids=group_id)[0].rules
                rule_nums = len(sec_rules)
                ent = m.addEntity("matterasmus.AmazonEC2SecurityGroupRule", "Ingress Rules")
                ent.addAdditionalFields("IngressRules", "Ingress Rules", "strict", "Ingress Rules")
                for g in range(rule_nums):
                    ent = m.getVar("IngressRules")
                    ent = m.addEntity("matterasmus.AmazonEC2SecurityGroup", str(conn.get_all_security_groups(group_ids=group_id)[0].rules[g]))
                    ent.addAdditionalFields("ProtocolPort", "Protocol Port", "strict", str(conn.get_all_security_groups(group_ids=group_id)[0].rules[g]))
                    ent = m.getVar("ProtocolPort")
                    ent = m.addEntity("maltego.IPv4Address", str(conn.get_all_security_groups(group_ids=group_id)[0].rules[g].grants))
                    ent.addAdditionalFields("Source", "Source", "strict", str(conn.get_all_security_groups(group_ids=group_id)[0].rules[g].grants))

                # Security Group Egress Rules
                egress_rules = conn.get_all_security_groups(group_ids=group_id)[0].rules_egress
                number_of_egress = len(egress_rules)
                ent = m.addEntity("matterasmus.AmazonEC2SecurityGroupRule", "Egress Rules")
                ent.addAdditionalFields("EgressRules", "Egress Rules", "strict", "Egress rules")
                for k in range(number_of_egress):
                    ent = m.getVar("EgressRules")
                    ent = m.addEntity("matterasmus.AmazonEC2SecurityGroup", str(conn.get_all_security_groups(group_ids=group_id)[0].rules_egress[k]))
                    ent.addAdditionalFields("ProtocolPort", "Protocol Port", "strict", str(conn.get_all_security_groups(group_ids=group_id)[0].rules_egress[k]))
                    ent = m.getVar("ProtocolPort")
                    ent = m.addEntity("maltego.IPv4Address", str(conn.get_all_security_groups(group_ids=group_id)[0].rules_egress[k].grants))
                    ent.addAdditionalFields("Destination", "Destination", "strict", str(conn.get_all_security_groups(group_ids=group_id)[0].rules_egress[k].grants))

    m.addUIMessage("Completed.")

except Exception as e:
    m.addUIMessage(str(e))


m.returnOutput()
