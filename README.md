Elastic Elephant
================


These are Maltego Transforms to talk to Amazon via [Boto](https://aws.amazon.com/sdk-for-python/)

You will also need the Maltego Python library from [here](http://www.paterva.com/web6/documentation/developer-local.php).

We want to find out what Instances are running with what Security Groups etc. 

The maltezon.mtz file contains the Entities needed for this to work. 


Script overview
---------------


Default/Init Scripts
--------------------

 * init.py.dist - Init stuff. Amazon credentials and default AWS region


Instance Scripts
----------------

 * GetInstances.py - Gets all the Instances running in a region
 * GetInstanceTag.py - Gets the Instance Tag/Name
 * GetInstanceInfo.py - Gets all the information for a specific Instance
 * GetInstancePublicIp.py - Gets the public IP address for a specific Instance
 * GetInstanceSecurityGroups.py - Gets all the Security Groups applied to an Instance
 * GetInstanceState.py - Get the running state of an Instance


Security Group Scripts
----------------------

 * GetGlobalSecurityGroups.py - Gets all the Security Groups in use in an AWS region
 * GetSecurityGroupRules.py - Gets the Security Group rules
 * GetIngressProtocolPort.py - THIS IS BROKEN
 * GetIngressSource.py - SOON
 * GetEgressProtocolPort.py - SOON
 * GetEgressDestination.py - SOON
