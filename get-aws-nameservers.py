#!/usr/bin/python

import boto3
import os

#
# Just a simple tool for pulling in the nameservers for all hosted zones on your AWS account
# Usage: set your IAM access keys in your environment variables and run:
# python get-aws-nameservers.py
#

def main():

    client = boto3.client('route53')
    hosted_zones = client.list_hosted_zones()
    zones = []

    for ZoneId in hosted_zones.get("HostedZones"):
        zones.extend([ZoneId.get("Id").translate(None, '/hostedzone/')])

        for zone in zones:
            response = client.get_hosted_zone(Id=zone)
            HostedZone = response.get("HostedZone")
            DelegationSet = response.get("DelegationSet")
            if "HostedZone" in response:
                name = HostedZone.get("Name")
                zoneid = HostedZone.get("Id").translate(None, '/hostedzone/')
            if "DelegationSet" in response:
                nameservers = DelegationSet.get("NameServers", "none")
            else:
                nameservers = "None"
            print(name.replace("'", "") + " " + str(nameservers).strip('[]')).replace("'", "")

if __name__ == "__main__":
    main()
