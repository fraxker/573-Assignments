from ns import ns
from cppyy import addressof, bind_object

def simulate(protocol, end_time, max_bytes):
    ns.core.Config.SetDefault("ns3::TcpL4Protocol::SocketType", protocol)
    # Sender Nodes
    sNodes = ns.network.NodeContainer()
    sNodes.Create(2)

    # Router Nodes
    rNodes = ns.network.NodeContainer()
    rNodes.Create(2)

    # Destination Nodes
    dNodes = ns.network.NodeContainer()
    dNodes.Create(2)

    # Create Architecture with rate of 1Gbps
    p2p = ns.point_to_point.PointToPointHelper()
    p2p.SetDeviceAttribute("DataRate", ns.core.StringValue("1Gbps"))
    r1r2 = p2p.Install(rNodes)
    s1r1 = p2p.Install(sNodes.Get(0), rNodes.Get(0))
    s2r1 = p2p.Install(sNodes.Get(1), rNodes.Get(0))
    r2d1 = p2p.Install(rNodes.Get(1), dNodes.Get(0))
    r2d2 = p2p.Install(rNodes.Get(1), dNodes.Get(1))
    
    # Install all nodes on to internet stack
    stack = ns.internet.InternetStackHelper()
    stack.InstallAll()

    # Assign each set of nodes onto its own subnet for proper architecture
    address = ns.internet.Ipv4AddressHelper()
    address.SetBase(ns.network.Ipv4Address("10.1.1.0"), ns.network.Ipv4Mask("255.255.255.0"))
    ipr1r2 = address.Assign(r1r2)
    address.SetBase(ns.network.Ipv4Address("10.1.2.0"), ns.network.Ipv4Mask("255.255.255.0"))
    ips1r1 = address.Assign(s1r1)
    ips2r1 = address.Assign(s2r1)
    address.SetBase(ns.network.Ipv4Address("10.1.3.0"), ns.network.Ipv4Mask("255.255.255.0"))
    ipr2d1 = address.Assign(r2d1)
    ipr2d2 = address.Assign(r2d2)

    # Create routing tables
    ns.network.Ipv4GlobalRoutingHelper.PopulateRoutingTables()
    
    # Set up flow monitor helper and install on all nodes
    fm = ns.network.FlowMonitorHelper()
    fm.InstallAll()
    monitor = fm.GetMonitor()
    monitor.Start(ns.core.Seconds(0.0))
    monitor.Stop(ns.core.Seconds(end_time))
    

    # Sender 1
    s1bsh = ns.network.BulkSendHelper("ns3::TcpSocketFactory", ns.network.InetSocketAddress(ips1r1.GetAddress(0), 5000).ConvertTo())
    s1bsh.SetAttribute("MaxBytes", ns.core.UintegerValue(max_bytes))
    s1sa = s1bsh.Install(sNodes.Get(0))
    s1sa.Start(ns.core.Seconds(5.0))
    s1sa.Stop(ns.core.Seconds(end_time))

    # # Sender 2
    # s2bsh = ns.network.BulkSendHelper("ns3::TcpSocketFactory", ns.network.InetSocketAddress(ips2r1.GetAddress(0), 5001).ConvertTo())
    # s2bsh.SetAttribute("MaxBytes", ns.core.UintegerValue(max_bytes))
    # s2sa = s2bsh.Install(sNodes.Get(1))
    # s2sa.Start(ns.core.Seconds(0.0))
    # s2sa.Stop(ns.core.Seconds(end_time))

    # Destination 1
    d1psh = ns.network.PacketSinkHelper("ns3::TcpSocketFactory", ns.network.InetSocketAddress(ns.network.Ipv4Address.GetAny(), 5000).ConvertTo())
    # d1psh.SetAttribute("Protocol", protocol)
    d1sa = d1psh.Install(dNodes.Get(0))
    d1sa.Start(ns.core.Seconds(5.0))
    d1sa.Stop(ns.core.Seconds(end_time))

    # # Destination 2
    # d2psh = ns.network.PacketSinkHelper("ns3::TcpSocketFactory", ns.network.InetSocketAddress(ns.network.Ipv4Address.GetAny(), 5001).ConvertTo())
    # d2sa = d2psh.Install(dNodes.Get(1))
    # d2sa.Start(ns.core.Seconds(0.0))
    # d2sa.Stop(ns.core.Seconds(end_time))

    print("Run Simulator")
    ns.core.Simulator.Stop(ns.core.Seconds(end_time))
    ns.core.Simulator.Run()
    ns.core.Simulator.Destroy()
    monitor.SerializeToXmlFile("xml_out.xml", False, False)
    print("Done")
    d1eps = bind_object(addressof(d1sa), ns.network.PacketSink)
    # d2eps = bind_object(addressof(d2sa), ns.network.PacketSink)
    print(d1eps.GetTotalRx(), d1eps.GetTotalRx())



####################################
####### ####### MAIN ####### #######
####################################

cubic = ns.core.TypeIdValue(ns.network.TcpCubic.GetTypeId())

# this line might not be right --Drew
dctcp = ns.core.TypeIdValue(ns.network.TcpDctcp.GetTypeId())

end_times = 100000.0

max_bytes = 100000

if __name__ == "__main__":
    simulate(dctcp, end_times, max_bytes)
    
