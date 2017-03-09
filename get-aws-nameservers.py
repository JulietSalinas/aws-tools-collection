#!/usr/bin/python

import boto3
import os

#f = open('zone_ids.txt')
#zones = f.read().split('\n')
client = boto3.client('route53')
hosted_zones = client.list_hosted_zones()
zones = []

for ZoneId in hosted_zones.get("HostedZones"):
    zones.extend([ZoneId.get("Id").translate(None, '/hostedzone/')])

def main():
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
