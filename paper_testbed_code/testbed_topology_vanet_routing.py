        #!/bin/python3

# Copyright (c) 2018 SONATA-NFV, 5GTANGO and Paderborn University
# ALL RIGHTS RESERVED.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Neither the name of the SONATA-NFV, 5GTANGO, Paderborn University
# nor the names of its contributors may be used to endorse or promote
# products derived from this software without specific prior written
# permission.
#
# This work has also been performed in the framework of the 5GTANGO project,
# funded by the European Commission under Grant number 761493 through
# the Horizon 2020 and 5G-PPP programmes. The authors would like to
# acknowledge the contributions of their colleagues of the 5GTANGO
# partner consortium (www.5gtango.eu).
import re
import logging
from sys import exit
from mininet.log import setLogLevel, info, error
import testbed_utils as tu
import time

from mininet.node import Controller, Node
from mininet.term import makeTerm
from mn_wifi.node import OVSKernelAP
from mn_wifi.link import wmediumd
from mn_wifi.cli import CLI
from mn_wifi.wmediumdConnector import interference
from mn_wifi.sumo.runner import sumo
from mn_wifi.net import Mininet_wifi
from mininet.link import Intf
from mininet.util import quietRun


logging.basicConfig(level=logging.DEBUG)
setLogLevel('info')  # set Mininet loglevel

class LinuxRouter(Node):
    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        # Enable forwarding on the router
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()

def checkIntf( intf ):
    "Make sure intf exists and is not configured."
    config = quietRun( 'ifconfig %s 2>/dev/null' % intf, shell=True )
    if not config:
        error( 'Error:', intf, 'does not exist!\n' )
        exit( 1 )
    ips = re.findall( r'\d+\.\d+\.\d+\.\d+', config )
    if ips:
        error( 'Error:', intf, 'has an IP address,'
               'and is probably in use!\n' )
        exit( 1 )

def create_topology():

    trains_file = "good_map/osm.rail.trips.xml"
#    access_points_file = "ap_names_positions.csv"
    cars_file = "good_map/osm.passenger.trips.xml"

    net = Mininet_wifi(controller=Controller, link=wmediumd, wmediumd_mode=interference)

    kwargs = {'ssid':'wifi', 'mode':'n','txpower':'10dBm','range': 300, 'failMode': 'standalone', 'datapath': 'user'}

    info("Loading trains and cars informations")
    trains_ids = tu.getIdFromXml(trains_file,"trip")
#    cars_ids = tu.getIdFromXml(cars_file, "trip")

    info("*** Creating nodes : Train and vehicles\n")

    # info("Trains list :")
    # print(trains_ids)
    # info("Cars list")
    # print(cars_ids)
    kwargs2 = {'bgscan_threshold':-70,'s_inverval':2, 'l_interval':5, 'bgscan_module':'simple'}
    defaultIP = '11.0.0.1/8'
    defaultExtIp = '15.0.0.2'

    router = net.addHost("r0", cls=LinuxRouter, ip=defaultIP, defaultRoute='via %s' %defaultExtIp)
    h2 = net.addHost("h2", ip="11.0.0.2/8")
    h3 = net.addHost("h3", ip="11.0.0.3/8")
    h4 = net.addHost("h4", ip="11.0.0.10/8")
    # # for id in range(len(trains_ids)):

    for id in range(1,20):
        train_id = 't%s'%trains_ids[id]
        ip_address = '11.0.0²8'.format(id+20+1)
        net.addCar(train_id, ip=ip_address, defaultRoute='via 11.0.0.1', **kwargs2)

    # for id in range(1,10):
    #     car_id = 'c%s'%cars_ids[id]
    #     net.addCar(car_id, wlans=1, encrypt=['wpa2', '123456789a'],**kwargs2)

    # create access points
    info("Access points creation")
    #access_points = tu.get_access_point_names(access_points_file)
    ap_1 = net.addAccessPoint('ap_1', channel=6, position='484,1909,0',
                              mac="00:00:00:11:00:01",**kwargs)
    ap_2 = net.addAccessPoint('ap_2', channel=11, position='595,1929,0',
                              mac="00:00:00:11:00:02", **kwargs)
    ap_3 = net.addAccessPoint('ap_3', channel=1, position='751,1964,0',
                              mac="00:00:00:11:00:03", **kwargs)
    ap_4 = net.addAccessPoint('ap_4', channel=13, position='901,1993,0',
                              mac="00:00:00:11:00:04", **kwargs)
    ap_5 = net.addAccessPoint('ap_5', channel=6, position='1063,2027,0',
                              mac="00:00:00:11:00:05", **kwargs)
    ap_6 = net.addAccessPoint('ap_6', channel=11, position='1231,2061,0',
                              mac="00:00:00:11:00:06", **kwargs)
    ap_7 = net.addAccessPoint('ap_7', channel=13, position='1459,2098,0',
                              mac="00:00:00:11:00:07", **kwargs)
    ap_8 = net.addAccessPoint('ap_8', channel=1, position='1662,2143,0',
                              mac="00:00:00:11:00:08", **kwargs)
    ap_9 = net.addAccessPoint('ap_9', channel=6, position='1876,2184,0',
                              mac="00:00:00:11:00:09", **kwargs)
    ap_10 = net.addAccessPoint('ap_10', channel=11, position='2100,2229,0',
                              mac="00:00:00:11:00:10", **kwargs)
    ap_11 = net.addAccessPoint('ap_11', channel=1, position='2273,2260,0',
                              mac="00:00:00:11:00:11", **kwargs)
    ap_12 = net.addAccessPoint('ap_12', channel=13, position='2459,2289,0',
                              mac="00:00:00:11:00:12", **kwargs)
    ap_13 = net.addAccessPoint('ap_13', channel=6, position='2606,2309,0',
                              mac="00:00:00:11:00:13", **kwargs)
    ap_14 = net.addAccessPoint('ap_14', channel=11, position='2746,2316,0',
                              mac="00:00:00:11:00:14", **kwargs)
    ap_15 = net.addAccessPoint('ap_15', channel=1, position='2931,2347,0',
                              mac="00:00:00:11:00:15", **kwargs)
    ap_16 = net.addAccessPoint('ap_16', channel=13, position='2974,2485,0',
                              mac="00:00:00:11:00:16", **kwargs)
    ap_17 = net.addAccessPoint('ap_17', channel=6, position='3244,2538,0',
                              mac="00:00:00:11:00:17", **kwargs)

    print("Access points loading complete \n.")

    #Adding internal network switch s1 and external switch s2
    info("*** Adding switches for routing")
    s1 = net.addSwitch('s1')

    s2 = net.addSwitch('s2')

    intfName = "p1net"
    # info("*** Checking intf name")
    # checkIntf(intfName)

    # info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=2.8)

    c0 = net.addController('c0')
    info("Adding controller ....")

    info("Controller info : \n")
    info(c0)

    net.configureWifiNodes()

    info("**** Adding link between access points, swith and router")

    net.addLink(s1, router, intfName = 'r0-eth1',
            params2={ 'ip' : defaultIP })
    net.addLink(s2, router, intfName = 'r0-eth2', params2={ 'ip' : '15.0.0.4/8'})

    net.addLink(h2, ap_2)
    net.addLink(h3, ap_5)
    net.addLink(h4, ap_17)

    net.addLink(s1, ap_1)
    net.addLink(ap_1, ap_2)

    net.addLink(ap_2, ap_3)
    net.addLink(ap_3, ap_4)
    net.addLink(ap_4, ap_5)
    net.addLink(ap_5, ap_6)
    net.addLink(ap_6, ap_7)
    net.addLink(ap_7, ap_8)

    net.addLink(ap_8, ap_9)
    net.addLink(ap_9, ap_10)

    net.addLink(ap_10, ap_11)
    net.addLink(ap_11, ap_12)
    net.addLink(ap_12, ap_13)

    net.addLink(ap_13, ap_14)

    net.addLink(ap_14, ap_15)
    net.addLink(ap_15, ap_16)
    net.addLink(ap_16, ap_17)

    info("**** Starting network and connecting to traci")
    info('Connecting to traci - sumo')
    # exec_order: Tells TraCI to give the current
    # client the given position in the execution order.
    # We may have to change it from 0 to 1 if we want to
    # load/reload the current simulation from a 2nd client

    net.useExternalProgram(program=sumo, port=8813,
                           config_file='good_map/osm.sumocfg',
                           extra_params=["--start --delay 1000"],
                            clients=1, exec_order=0)

    net.build()

    info("*** Connecting to intf %s"%intfName)
    Intf( intfName, node=s2)

    c0.start()
    for ap in net.aps:
        ap.start([c0])

    # # Track the position of the nodes
    nodes = net.cars + net.aps

    net.telemetry(nodes=nodes, data_type='position',
                  min_x=200, min_y=200,
                  max_x=3500, max_y=3500)

    info("**** Launching vnfs")
    #timer_debut = time.perf_counter()
    iperf_server = "11.0.0.10"
    makeTerm(h4, cmd="bash -c 'iperf -s ")
    for c in net.cars:
        # default_route_cmd = 'ip route add default via 11.0.0.1'
        # makeTerm(c, cmd=f"bash -c '{default_route_cmd}'")
        start_cmd = f"bash -c "+ "'python3 host_edge_service_start_edit.py " + c.name + " " + iperf_server +"'"
        makeTerm(c, cmd=start_cmd)


    # route add -net 10.0.0.0/8 gw 12.0.0.1
    router.cmd("route add -net 10.0.0.0/8 gw 15.0.0.2")
    net.start()

    info("*** Configuring %s interface"%intfName)
    #quietRun( f'ovs-vsctl del-port {s2.name} {intfName}', shell=True )
    #res = quietRun( f' ovs-vsctl add-port {s2.name} {intfName}', shell=True )
    #print(res)
    config = quietRun( 'ifconfig %s up' %s2.name, shell=True)
    print(config)

    # quietRun( f'ip addr add {defaultExtIp}/8 dev {s2.name}', shell=True)
    # config = quietRun('ifconfig %s' %s2.name, shell=True)

    info("*** Running CLI\n")
    CLI(net)
    # when the user types exit in the CLI, we stop the emulator
    net.stop()


if __name__ == '__main__':
    create_topology()
