from linode_api4 import LinodeClient, Instance
import datetime
import threading

from app.core.config import config


def get_client():
    return LinodeClient(config.LINODE_TOKEN)


def generate_label(region: str):
    global wg_counter
    while "wg" + str(wg_counter) + "-" + region in instance_dict:
        wg_counter += 1
    return "wg" + str(wg_counter) + "-" + region


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
    instance_dict[instance_label] = new_linode
    # Start timer
    if expiration != 0:
        expiration_dict[instance_label] = datetime.datetime.now() + datetime.timedelta(
            hours=expiration
        )
        # Terminate instance 1 min less than set time to account for delay
        timer = threading.Timer(expiration * 3540, delete_instance, [instance_label])
        timer.start()
        print(
            "{instance_label} ({instance_ipv4}) timer set for {expiration} hours".format(
                instance_label=new_linode.label,
                instance_ipv4=new_linode.ipv4[0],
                expiration=expiration,
            )
        )
    else:
        expiration_dict[instance_label] = 0
    if new_linode:
        print(
            "{instance_label} ({instance_ipv4}) created".format(
                instance_label=new_linode.label, instance_ipv4=new_linode.ipv4[0]
            )
        )
    return new_linode


def delete_instance(instance_label: str):
    instance = instance_dict[instance_label]
    print(
        "{instance_label} ({instance_ipv4}) deleted".format(
            instance_label=instance_label, instance_ipv4=instance.ipv4[0]
        )
    )
    return instance_dict.pop(instance_label).delete()


# references for created instances
instance_dict: {str: Instance} = {}
# store set duration for each instance
expiration_dict: {str: datetime} = {}

wg_counter = 0

client = get_client()
