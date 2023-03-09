from ns import ns

if __name__ == "__main__":
    """
    Config::SetDefault("ns3::TcpL4Protocol::SocketType", StringValue("ns3::" + tcpTypeId));
    """

    s1 = ns.network.Node()
    s2 = ns.network.Node()
    d1 = ns.network.Node()
    d2 = ns.network.Node()
    r1 = ns.network.Node()
    r2 = ns.network.Node()

    p2p = ns.point_to_point.PointToPointHelper()
    p2p.SetDeviceAttribute("DataRate", ns.core.StringValue("1Gbps"))
    r1r2 = p2p.Install(r1, r2)
    s1r1 = p2p.Install(s1, r1)
    s2r1 = p2p.Install(s2, r1)
    r2d1 = p2p.Install(r2, d1)
    r2d2 = p2p.Install(r2, d2)

    address = ns.internet.Ipv4AddressHelper()
    address.SetBase("10.1.1.0", "255.255.255.0")
    address.Assign(r1r2)
    address.SetBase("10.1.2.0", "255.255.255.0")
    address.Assign(s1r1)
    address.Assign(s2r1)
    address.SetBase("10.1.3.0", "255.255.255.0")
    address.Assign(r2d1)
    address.Assign(r2d2)


    """
    Ipv4GlobalRoutingHelper::PopulateRoutingTables();
    Address sinkLocalAddress(InetSocketAddress(Ipv4Address::GetAny(), port));
    PacketSinkHelper sinkHelper("ns3::TcpSocketFactory", sinkLocalAddress);
    ApplicationContainer sinkApp = sinkHelper.Install(R2.Get(i));
    sinkApp.Start(startTime);
    sinkApp.Stop(stopTime);

    OnOffHelper clientHelper1("ns3::TcpSocketFactory", Address());
    clientHelper1.SetAttribute("OnTime",
                               StringValue("ns3::ConstantRandomVariable[Constant=1]"));
    clientHelper1.SetAttribute("OffTime",
                               StringValue("ns3::ConstantRandomVariable[Constant=0]"));
    clientHelper1.SetAttribute("DataRate", DataRateValue(DataRate("1Gbps")));
    clientHelper1.SetAttribute("PacketSize", UintegerValue(1000));

    ApplicationContainer clientApps1;
    AddressValue remoteAddress(InetSocketAddress(ipR2T2[i].GetAddress(0), port));
    clientHelper1.SetAttribute("Remote", remoteAddress);
    clientApps1.Add(clientHelper1.Install(S2.Get(i)));
    clientApps1.Start(i * flowStartupWindow / 20 + clientStartTime + MilliSeconds(i * 5));
    clientApps1.Stop(stopTime);

    Simulator::Run();
    Simulator::Destroy();
    """