# import urllib2


def map_3(hosts, mapping):
    groups = mapping['host_groups']
    for i in range(len(groups)):
        groups[i]['hosts'][0]['fqdn'] = hosts["masters"].pop()
    return mapping


def map_7(hosts, mapping):
    groups = mapping['host_groups']
    for i in range(len(groups)):
        host_role = (groups[i]['name']).split('_')
        if host_role[0] == 'master':
            groups[i]['hosts'][0]['fqdn'] = hosts["masters"].pop()
        elif (len(host_role) > 1 and host_role[0] == 'slave' and host_role[1] == 'zk'):
            groups[i]['hosts'][0]['fqdn'] = hosts["slaves"].pop()
        elif (len(host_role) == 1 and host_role[0] == 'slave'):
            slave_hosts = groups[i]['hosts']
            for ii in range(len(hosts["slaves"])):
                slave_hosts.append({'fqdn': hosts["slaves"].pop()})
    return mapping


def map_8(hosts, mapping):
    groups = mapping['host_groups']
    for i in range(len(groups)):
        host_role = (groups[i]['name']).split('_')
        if host_role[0] == 'master':
            groups[i]['hosts'][0]['fqdn'] = hosts["masters"].pop()
        elif (len(host_role) > 1 and host_role[0] == 'slave' and host_role[1] == 'zk'):
            groups[i]['hosts'][0]['fqdn'] = hosts["slaves"].pop()
        elif (len(host_role) == 1 and host_role[0] == 'slave'):
            slave_hosts = groups[i]['hosts']
            for ii in range(len(hosts["slaves"])):
                slave_hosts.append({'fqdn': hosts["slaves"].pop()})
    config = mapping['configurations']
    config[0]['yarn-site']['yarn.resourcemanager.zk-address'] = groups[4]['hosts'][0]['fqdn'] + ":2181," + groups[5]['hosts'][0]['fqdn'] + ":2181," + groups[6]['hosts'][0]['fqdn'] + ":2181"
    config[0]['yarn-site']['yarn.resourcemanager.hostname.rm1'] = groups[2]['hosts'][0]['fqdn']
    config[0]['yarn-site']['yarn.resourcemanager.hostname.rm2'] = groups[3]['hosts'][0]['fqdn']
    return mapping


# test ...
# if __name__ == "__main__":
# url = 'http://localhost:5000/plan -d "master=3" -d "slave=0" -d "components={mini}" -X PUT'
# req = urllib2.Request(url)
# reponse = urllib2.urlopen(req)
# print len(reponse.read())
