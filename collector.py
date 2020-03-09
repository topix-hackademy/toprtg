import pysnmp
import json
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto.rfc1902 import Integer, IpAddress, OctetString

conf_paths = ['/etc/toprtg/', './']

ifTable =       (1,3,6,1,2,1,31,1,1,1,1)
ifXHCInOctets =  [1,3,6,1,2,1,31,1,1,1,6]


def poll_device():
    print('asd')


if __name__ == '__main__':

    found = False

    # Read config file
    for path in conf_paths:
        try:
            f = open(path + 'toprtg.conf', 'r')
            data = json.load(f)
            found = True
            break
        except FileNotFoundError:
            continue

    if not found:
        exit(1)

    for entry in data['entries']:

        generator = cmdgen.CommandGenerator()
        comm_data = cmdgen.CommunityData('server', entry['community'], 1) # 1 means version SNMP v2c
        transport = cmdgen.UdpTransportTarget((entry['ip'], 161))

        handler = getattr(generator, 'nextCmd')

        # get iflist
        name_to_ifid = {}
        res = (errorIndication, errorStatus, errorIndex, varBinds) = handler(comm_data, transport, ifTable)

        # todo: PARSE INTERFACE LIST
        for item in varBinds:
            for obj in item:
                obj = str(obj)
                tokens = obj.split(' = ')
                temp_ifid = tokens[0].split('.')[-1]
                temp_name = tokens[1]
                name_to_ifid[temp_name] = temp_ifid

        if not errorIndication is None or errorStatus is True:
            print("Error: %s %s %s %s" % res)
        else:
            for name in entry['interfaces']:
                ifid = int(name_to_ifid[name])
                ifHCInOctets = tuple(ifXHCInOctets + [ifid])
                print('OID: {}'.format(ifHCInOctets))
                handler = getattr(generator, 'getCmd')
                res = (errorIndication, errorStatus, errorIndex, varBinds) = handler(comm_data, transport, ifHCInOctets)
                if not errorIndication is None or errorStatus is True:
                    print("Error: %s %s %s %s" % res)
                else:
                    octects = int(str(varBinds[0]).split(' = ')[1])
                    print('ifid: {}\nname: {}\nin octects: {}\n'.format(ifid, name, octects))