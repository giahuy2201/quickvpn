import linode_api4
import datetime
import threading

from app.core.config import config
import app.schemas.instance as schemas


def get_client():
    return linode_api4.LinodeClient(config.LINODE_TOKEN)


def generate_label(region: str):
    global wg_counter
    while "wg" + str(wg_counter) + "-" + region in instance_dict:
        wg_counter += 1
    return "wg" + str(wg_counter) + "-" + region


def parse_linodes(linodes: linode_api4.PaginatedList):
    instance_list: [schemas.Instance] = []
    for node in linodes:
        print(type(node.type))
        instance_list.append(
            schemas.Instance(
                label=node.label,
                region=str(node.region),
                status=str(node.status),
                image="image",
                type=str(node.type),
                expiration="expiration",
                ipv4=node.ipv4[0],
                ipv6=node.ipv6[0],
            )
        )
    return instance_list


def get_instance(instance_label: str):
    return instance_dict[instance_label]


def get_all_instances():
    # List all Linodes on the account
    linodes = client.linode.instances()
    return parse_linodes(linodes)


def create_instance(region: str, expiration: int):
    instance_label = generate_label(region)
    # Create a new Linode
    new_linode = client.linode.instance_create(
        ltype="g6-nanode-1",
        region=region,
        image="linode/debian12",
        label=instance_label,
        root_pass=config.SSH_PASSWD,
    )
    if new_linode:
        instance_dict[instance_label] = new_linode
        instance_ipv4 = new_linode.ipv4[0]
        print(f"{instance_label} ({instance_ipv4}) created")
        # Start timer
        if expiration != 0:
            expiration_dict[
                instance_label
            ] = datetime.datetime.now() + datetime.timedelta(hours=expiration)
            # Terminate instance 1 min less than set time to account for delay
            timer = threading.Timer(
                expiration * 3540, delete_instance, [instance_label]
            )
            timer.start()
            print(
                f"{instance_label} ({instance_ipv4}) timer set for {expiration} hours"
            )
        else:
            expiration_dict[instance_label] = 0
    return new_linode


def delete_instance(instance_label: str):
    instance = instance_dict[instance_label]
    instance_ipv4 = instance.ipv4[0]
    success = instance_dict.pop(instance_label).delete()
    if success:
        print(f"{instance_label} ({instance_ipv4}) deleted")
    return success


# references for created instances
instance_dict: {str: linode_api4.Instance} = {}
# store set duration for each instance
expiration_dict: {str: datetime} = {}

wg_counter = 0

client = get_client()
