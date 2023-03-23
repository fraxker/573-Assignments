from ns import ns
import csv
from statistics import mean, stdev

# Returns (s1 throughput, s1 fct, s2 throughput, s2 fct) last 2 can be none
def simulate(protocol1, protocol2):
    
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
    address.SetBase(ns.network.Ipv4Address("10.1.3.0"), ns.network.Ipv4Mask("255.255.255.0"))
    ips2r1 = address.Assign(s2r1)
    address.SetBase(ns.network.Ipv4Address("10.1.4.0"), ns.network.Ipv4Mask("255.255.255.0"))
    ipr2d1 = address.Assign(r2d1)
    address.SetBase(ns.network.Ipv4Address("10.1.5.0"), ns.network.Ipv4Mask("255.255.255.0"))
    ipr2d2 = address.Assign(r2d2)

    # Create routing tables
    ns.network.Ipv4GlobalRoutingHelper.PopulateRoutingTables()
    
    # Set up flow monitor helper and install on all nodes
    fm = ns.network.FlowMonitorHelper()
    fm.InstallAll()

    ns.core.Config.SetDefault("ns3::TcpL4Protocol::SocketType", protocol1)
    # Sender 1
    s1bsh = ns.network.BulkSendHelper("ns3::TcpSocketFactory", ns.network.InetSocketAddress(ipr2d1.GetAddress(1), 50000).ConvertTo())
    s1bsh.SetAttribute("MaxBytes", ns.core.UintegerValue(max_bytes))
    s1sa = s1bsh.Install(sNodes.Get(0))
    s1sa.Start(ns.core.Seconds(0.0))
    s1sa.Stop(ns.core.Seconds(end_time))

    # Destination 1
    d1psh = ns.network.PacketSinkHelper("ns3::TcpSocketFactory", ns.network.InetSocketAddress(ns.network.Ipv4Address.GetAny(), 50000).ConvertTo())
    d1sa = d1psh.Install(dNodes.Get(0))
    d1sa.Start(ns.core.Seconds(0.0))
    d1sa.Stop(ns.core.Seconds(end_time))

    if protocol2 is not None:
        ns.core.Config.SetDefault("ns3::TcpL4Protocol::SocketType", protocol2)
        # # Sender 2
        s2bsh = ns.network.BulkSendHelper("ns3::TcpSocketFactory", ns.network.InetSocketAddress(ipr2d2.GetAddress(1), 5001).ConvertTo())
        s2bsh.SetAttribute("MaxBytes", ns.core.UintegerValue(max_bytes))
        s2sa = s2bsh.Install(sNodes.Get(1))
        s2sa.Start(ns.core.Seconds(0.0))
        s2sa.Stop(ns.core.Seconds(end_time))

        # # Destination 2
        d2psh = ns.network.PacketSinkHelper("ns3::TcpSocketFactory", ns.network.InetSocketAddress(ns.network.Ipv4Address.GetAny(), 5001).ConvertTo())
        d2sa = d2psh.Install(dNodes.Get(1))
        d2sa.Start(ns.core.Seconds(0.0))
        d2sa.Stop(ns.core.Seconds(end_time))

    print("Run Simulator")
    ns.core.Simulator.Stop(ns.core.Seconds(end_time))
    ns.core.Simulator.Run()
    ns.core.Simulator.Destroy()
    print("Done")
    #Calculate stats
    m = fm.GetMonitor()
    stats = m.GetFlowStats()
    # Sender 1
    s1_stats = stats[1]
    s1_fct = (s1_stats.timeLastTxPacket - s1_stats.timeFirstTxPacket).GetSeconds()
    s1_throughput = s1_stats.txBytes * 8 / s1_fct
    # Sender 2
    s2_fct = None
    s2_throughput = None
    if protocol2 is not None:
        s2_stats = stats[2]
        s2_fct = (s2_stats.timeLastTxPacket - s2_stats.timeFirstTxPacket).GetSeconds()
        s2_throughput = s2_stats.txBytes * 8 / s2_fct
    print(s1_fct, s1_throughput, s2_fct, s2_throughput)
    return (s1_fct, s1_throughput, s2_fct, s2_throughput)

####################################
####### ####### MAIN ####### #######
####################################

cubic = ns.core.TypeIdValue(ns.network.TcpCubic.GetTypeId())

dctcp = ns.core.TypeIdValue(ns.network.TcpDctcp.GetTypeId())

end_time = 5.0

max_bytes = 50000000

if __name__ == "__main__":
    with open("pa2.csv", "w", newline='') as c:
        csvwriter = csv.writer(c, delimiter=',')
        csvwriter.writerow(['exp','r1_s1','r2_s1','r3_s1','avg_s1','std_s1','unit_s1','r1_s2','r2_s2','r3_s2','avg_s2','std_s2','unit_s2', ""])
        #Experiment 1
        afct_1_r1_s1, th_1_r1_s1, afct_1_r1_s2, th_1_r1_s2 = simulate(cubic, None)
        afct_1_r2_s1, th_1_r2_s1, afct_1_r2_s2, th_1_r2_s2 = simulate(cubic, None)
        afct_1_r3_s1, th_1_r3_s1, afct_1_r3_s2, th_1_r3_s2 = simulate(cubic, None)
        #Experiment 2
        afct_2_r1_s1, th_2_r1_s1, afct_2_r1_s2, th_2_r1_s2 = simulate(cubic, cubic)
        afct_2_r2_s1, th_2_r2_s1, afct_2_r2_s2, th_2_r2_s2 = simulate(cubic, cubic)
        afct_2_r3_s1, th_2_r3_s1, afct_2_r3_s2, th_2_r3_s2 = simulate(cubic, cubic)
        #Experiment 3
        afct_3_r1_s1, th_3_r1_s1, afct_3_r1_s2, th_3_r1_s2 = simulate(dctcp, None)
        afct_3_r2_s1, th_3_r2_s1, afct_3_r2_s2, th_3_r2_s2 = simulate(dctcp, None)
        afct_3_r3_s1, th_3_r3_s1, afct_3_r3_s2, th_3_r3_s2 = simulate(dctcp, None)
        #Experiment 4
        afct_4_r1_s1, th_4_r1_s1, afct_4_r1_s2, th_4_r1_s2 = simulate(dctcp, dctcp)
        afct_4_r2_s1, th_4_r2_s1, afct_4_r2_s2, th_4_r2_s2 = simulate(dctcp, dctcp)
        afct_4_r3_s1, th_4_r3_s1, afct_4_r3_s2, th_4_r3_s2 = simulate(dctcp, dctcp)    
        #Experiment 5
        afct_5_r1_s1, th_5_r1_s1, afct_5_r1_s2, th_5_r1_s2 = simulate(dctcp, cubic)
        afct_5_r2_s1, th_5_r2_s1, afct_5_r2_s2, th_5_r2_s2 = simulate(dctcp, cubic)
        afct_5_r3_s1, th_5_r3_s1, afct_5_r3_s2, th_5_r3_s2 = simulate(dctcp, cubic)

        csvwriter.writerow(["th_1", th_1_r1_s1, th_1_r2_s1, th_1_r3_s1, mean([th_1_r1_s1, th_1_r2_s1, th_1_r3_s1]), stdev([th_1_r1_s1, th_1_r2_s1, th_1_r3_s1]), "bps", "", "", "", "", "", ""])
        csvwriter.writerow(["th_2", th_2_r1_s1, th_2_r2_s1, th_2_r3_s1, mean([th_2_r1_s1, th_2_r2_s1, th_2_r3_s1]), stdev([th_2_r1_s1, th_2_r2_s1, th_2_r3_s1]), "bps", th_2_r1_s2, th_2_r2_s2, th_2_r3_s2, mean([th_2_r1_s2, th_2_r2_s2, th_2_r3_s2]), stdev([th_2_r1_s2, th_2_r2_s2, th_2_r3_s2]), "bps"])
        csvwriter.writerow(["th_3", th_3_r1_s1, th_3_r2_s1, th_3_r3_s1, mean([th_3_r1_s1, th_3_r2_s1, th_3_r3_s1]), stdev([th_3_r1_s1, th_3_r2_s1, th_3_r3_s1]), "bps", "", "", "", "", "", ""])
        csvwriter.writerow(["th_4", th_4_r1_s1, th_4_r2_s1, th_4_r3_s1, mean([th_4_r1_s1, th_4_r2_s1, th_4_r3_s1]), stdev([th_4_r1_s1, th_4_r2_s1, th_4_r3_s1]), "bps", th_4_r1_s2, th_4_r2_s2, th_4_r3_s2, mean([th_4_r1_s2, th_4_r2_s2, th_4_r3_s2]), stdev([th_4_r1_s2, th_4_r2_s2, th_4_r3_s2]), "bps"])
        csvwriter.writerow(["th_5", th_5_r1_s1, th_5_r2_s1, th_5_r3_s1, mean([th_5_r1_s1, th_5_r2_s1, th_5_r3_s1]), stdev([th_5_r1_s1, th_5_r2_s1, th_5_r3_s1]), "bps", th_5_r1_s2, th_5_r2_s2, th_5_r3_s2, mean([th_5_r1_s2, th_5_r2_s2, th_5_r3_s2]), stdev([th_5_r1_s2, th_5_r2_s2, th_5_r3_s2]), "bps"])
        csvwriter.writerow(["afct_1", afct_1_r1_s1, afct_1_r2_s1, afct_1_r3_s1, mean([afct_1_r1_s1, afct_1_r2_s1, afct_1_r3_s1]), stdev([afct_1_r1_s1, afct_1_r2_s1, afct_1_r3_s1]), "sec", "", "", "", "", "", ""])
        csvwriter.writerow(["afct_2", afct_2_r1_s1, afct_2_r2_s1, afct_2_r3_s1, mean([afct_2_r1_s1, afct_2_r2_s1, afct_2_r3_s1]), stdev([afct_2_r1_s1, afct_2_r2_s1, afct_2_r3_s1]), "sec", afct_2_r1_s2, afct_2_r2_s2, afct_2_r3_s2, mean([afct_2_r1_s2, afct_2_r2_s2, afct_2_r3_s2]), stdev([afct_2_r1_s2, afct_2_r2_s2, afct_2_r3_s2]), "sec"])
        csvwriter.writerow(["afct_3", afct_3_r1_s1, afct_3_r2_s1, afct_3_r3_s1, mean([afct_3_r1_s1, afct_3_r2_s1, afct_3_r3_s1]), stdev([afct_3_r1_s1, afct_3_r2_s1, afct_3_r3_s1]), "sec", "", "", "", "", "", ""])
        csvwriter.writerow(["afct_4", afct_4_r1_s1, afct_4_r2_s1, afct_4_r3_s1, mean([afct_4_r1_s1, afct_4_r2_s1, afct_4_r3_s1]), stdev([afct_4_r1_s1, afct_4_r2_s1, afct_4_r3_s1]), "sec", afct_4_r1_s2, afct_4_r2_s2, afct_4_r3_s2, mean([afct_4_r1_s2, afct_4_r2_s2, afct_4_r3_s2]), stdev([afct_4_r1_s2, afct_4_r2_s2, afct_4_r3_s2]), "sec"])
        csvwriter.writerow(["afct_5", afct_5_r1_s1, afct_5_r2_s1, afct_5_r3_s1, mean([afct_5_r1_s1, afct_5_r2_s1, afct_5_r3_s1]), stdev([afct_5_r1_s1, afct_5_r2_s1, afct_5_r3_s1]), "sec", afct_5_r1_s2, afct_5_r2_s2, afct_5_r3_s2, mean([afct_5_r1_s2, afct_5_r2_s2, afct_5_r3_s2]), stdev([afct_5_r1_s2, afct_5_r2_s2, afct_5_r3_s2]), "sec"])