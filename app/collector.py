from exceptions import SNMPException
from util.util import snmp_poll, get_name_ifid_dict, find_conf_file
from util.db import write_interfaces
import traceback

ifTable =       (1,3,6,1,2,1,31,1,1,1,1)
ifXHCInOctets =  [1,3,6,1,2,1,31,1,1,1,6]


def poll_device():
    data = find_conf_file()

    interfaces = []

    for entry in data['entries']:
        try:
            response = snmp_poll(entry['ip'], entry['community'], ifTable, 'walk')
            name_to_ifid = get_name_ifid_dict(response)

            for name in entry['interfaces']:
                ifid = name_to_ifid.get(name, None)
                if ifid is not None:
                    ifHCInOctets = tuple(ifXHCInOctets + [ifid])

                    response = snmp_poll(entry['ip'], entry['community'], ifHCInOctets, 'get')
                    octets = int(str(response[0]).split(' = ')[1])

                    interfaces.append({
                        'ifid': ifid,
                        'name': name,
                        'in_octects': name
                    })
                else:
                    print(f'Warning: {name} not found on device {entry["ip"]}')
        except SNMPException as e:
            print(f'[SNMP Timeout] for {entry["ip"]}')
        except Exception as e:
            traceback.print_exc()

    write_interfaces(interfaces)


if __name__ == '__main__':
    poll_device()
