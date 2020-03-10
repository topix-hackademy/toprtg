import json
from pysnmp.entity.rfc3413.oneliner import cmdgen

conf_paths = ['/etc/toprtg/', './']


def snmp_poll(ip, community, oid, method):

    """
    ip: ipv4 address of the device to poll
    community: snmp community string
    oid: tuple containing the oid to poll for
    method: 'get' or 'walk'
    returns: the object returned by the snmp get
    """

    generator = cmdgen.CommandGenerator()
    comm_data = cmdgen.CommunityData('server', community, 1)  # 1 means version SNMP v2c
    transport = cmdgen.UdpTransportTarget((ip, 161))

    if method == 'get':
        handler = getattr(generator, 'getCmd')
    else:
        handler = getattr(generator, 'nextCmd')

    res = (errorIndication, errorStatus, errorIndex, varBinds) = handler(comm_data, transport, oid)

    if not errorIndication is None or errorStatus is True:
        print("Error: %s %s %s %s" % res)
        exit(1)

    else:
        return varBinds


def obj_parse(obj):
    obj = str(obj)
    tokens = obj.split(' = ')
    temp_ifid = tokens[0].split('.')[-1]
    temp_name = tokens[1]
    return temp_ifid, temp_name


def get_name_ifid_dict(response):
    name_to_ifid = {}

    for item in response:
        for obj in item:
            ifid, name = obj_parse(obj)
            name_to_ifid[name] = int(ifid)

    return name_to_ifid


def find_conf_file():

    # Read config file
    for path in conf_paths:
        try:
            f = open(path + 'toprtg.conf', 'r')
            data = json.load(f)
            return data

        except FileNotFoundError:
            continue

    exit(1)

