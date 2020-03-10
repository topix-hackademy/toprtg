from util.util import snmp_poll, get_name_ifid_dict, find_conf_file

ifTable =       (1,3,6,1,2,1,31,1,1,1,1)
ifXHCInOctets =  [1,3,6,1,2,1,31,1,1,1,6]


def poll_device():
    data = find_conf_file()

    for entry in data['entries']:
        response = snmp_poll(entry['ip'], entry['community'], ifTable, 'walk')
        name_to_ifid = get_name_ifid_dict(response)

        for name in entry['interfaces']:
            ifid = name_to_ifid[name]
            ifHCInOctets = tuple(ifXHCInOctets + [ifid])

            response = snmp_poll(entry['ip'], entry['community'], ifHCInOctets, 'get')
            octets = int(str(response[0]).split(' = ')[1])

            print('ifid: {}\nname: {}\nin octects: {}\n'.format(ifid, name, octets))


if __name__ == '__main__':
    poll_device()