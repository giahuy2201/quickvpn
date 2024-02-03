import CloudFlare

from app.core.config import config
from app.core.linode import get_instance


def update_dns(instance_label: str):
    # retrieve instance
    instance = get_instance(instance_label)
    instance_ipv4 = instance.ipv4[0]
    cf = CloudFlare.CloudFlare(token=config.CF_TOKEN)
    try:
        params = {"name": config.CF_DOMAIN, "match": "all", "type": "A"}
        dns_records = cf.zones.dns_records.get(config.CF_ZONEID, params=params)
        new_record = {
            "name": config.CF_DOMAIN,
            "type": "A",
            "content": instance_ipv4,
            "proxied": False,
        }
        if len(dns_records) == 0:
            dns_record = cf.zones.dns_records.post(config.CF_ZONEID, data=new_record)
            print(f"{instance_label} ({instance_ipv4}) {config.CF_DOMAIN} created")
        else:
            record = dns_records[0]
            dns_record = cf.zones.dns_records.put(
                config.CF_ZONEID, record["id"], data=new_record
            )
            print(f"{instance_label} ({instance_ipv4}) {config.CF_DOMAIN} updated")
        return True
    except CloudFlare.exceptions.CloudFlareAPIError as e:
        print("%s - %d %s - api call failed" % (config.CF_DOMAIN, e, e))
    return False
