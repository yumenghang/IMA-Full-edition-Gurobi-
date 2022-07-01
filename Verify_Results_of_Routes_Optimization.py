import Hyper_Parameters

class VERIFY_RESULTS_OF_ROUTES_OPTIMIZATION():
    def __init__(self,
                 ADJACENT_MATRIX,
                 ADJACENT_MATRIX_INDEX_REVERSED,
                 PHYSICAL_PORTS_INFORMATION,
                 SOURCE,
                 DESTINATION,
                 MTU,
                 BAG,
                 DELAY_BOUND_LEFT,
                 X_FOR_RETURN,
                 Y_FOR_RETURN,
                 TOTAL_BANDWIDTH_COST_FOR_RETURN,
                 DELAY_OF_NODES_FOR_RETURN,
                 BANDWIDTH_OF_NODES):
        self.ADJACENT_MATRIX = ADJACENT_MATRIX
        self.ADJACENT_MATRIX_INDEX_REVERSED = ADJACENT_MATRIX_INDEX_REVERSED
        self.PHYSICAL_PORTS_INFORMATION = PHYSICAL_PORTS_INFORMATION
        self.SOURCE = SOURCE
        self.DESTINATION = DESTINATION
        self.MTU = MTU
        self.BAG = BAG
        self.DELAY_BOUND_LEFT = DELAY_BOUND_LEFT
        self.X_FOR_RETURN = X_FOR_RETURN
        self.Y_FOR_RETURN = Y_FOR_RETURN
        self.TOTAL_BANDWIDTH_COST_FOR_RETURN = TOTAL_BANDWIDTH_COST_FOR_RETURN
        self.NUMBER_OF_VL = len( SOURCE )
        self.NUMBER_OF_NODES = len( self.ADJACENT_MATRIX )
        self.DELAY_OF_NODES_FOR_RETURN = DELAY_OF_NODES_FOR_RETURN
        self.DELTA = Hyper_Parameters.delta
        self.BANDWIDTH_OF_NODES = BANDWIDTH_OF_NODES

    def verify_routing_connections(self):
        # 验证路由优化结果的连通性是否正确
        for VL_index in range(self.NUMBER_OF_VL):
            source = self.SOURCE[VL_index]
            for destionation in self.DESTINATION[VL_index]:
                following_node = destionation
                OUTER_INDICATOR = 0
                path_reversed = [following_node]
                while not OUTER_INDICATOR:
                    INNER_INDICATOR = 0
                    for previous_node in range(self.NUMBER_OF_NODES):
                        if self.Y_FOR_RETURN[VL_index][previous_node][following_node] == 1:
                            INNER_INDICATOR = 1
                            if previous_node == source:
                                OUTER_INDICATOR = 1
                            else:
                                following_node = previous_node
                            path_reversed.append(previous_node)
                    if not INNER_INDICATOR:
                        break
                path = list(reversed(path_reversed))
                if OUTER_INDICATOR == 1:
                    continue
                else:
                    print("Routing for destionation %d is wrong! VL_index: %d, source:%d, destinations:" % (destionation, VL_index, source), self.DESTINATION[VL_index])
                    return False
        return True

    def verify_routing_capacity(self):
        # 验证物理端口在一个BAG时间间隔内能否将所有经此物理端口转发的虚链路的一个MTU转发出去
        for previous_node in range(self.NUMBER_OF_NODES):
            previous_physical_port_name = self.ADJACENT_MATRIX_INDEX_REVERSED[previous_node]
            for following_node in range(self.NUMBER_OF_NODES):
                following_physical_port_name = self.ADJACENT_MATRIX_INDEX_REVERSED[ following_node]
                min_bag, total_MTU = 1024, 0
                for VL_index in range(self.NUMBER_OF_VL):
                    if self.Y_FOR_RETURN[VL_index][previous_node][following_node] == 1:
                        min_bag = min(min_bag, self.BAG[VL_index])
                        total_MTU += self.MTU[VL_index]
                previous_capacity = min_bag * self.BANDWIDTH_OF_NODES[previous_node]
                following_capacity = min_bag * self.BANDWIDTH_OF_NODES[previous_node]
                if total_MTU >= previous_capacity or total_MTU >= following_capacity:
                    print("There is an error in capacity of previous-physical-port: %s and following-physical-port %s:" % (previous_physical_port_name, following_physical_port_name), total_MTU, previous_capacity, following_capacity)
        return True

    def verify_routing_bandwidth(self):
        # 验证物理端口传输虚拟链路的带宽是否超出物理端口的传输速率
        for previous_node in range(self.NUMBER_OF_NODES):
            bandwidth_cost = 0
            for VL_index in range(self.NUMBER_OF_VL):
                for following_node in range(self.NUMBER_OF_NODES):
                    if self.Y_FOR_RETURN[VL_index][previous_node][following_node] == 1:
                        bandwidth_cost += (self.MTU[VL_index] + self.DELTA) / self.BAG[VL_index]
            previous_physical_port_name = self.ADJACENT_MATRIX_INDEX_REVERSED[previous_node]
            if bandwidth_cost >= self.PHYSICAL_PORTS_INFORMATION[previous_physical_port_name][7] * 1000:
                print("There is an error in bandwidth of previous-physical-port: %s. The rate of physical port is: %f and the bandwidth cost is: %f!" % (previous_physical_port_name, self.BANDWIDTH_OF_NODES[previous_node], bandwidth_cost))
        return True

    def verify_routing_delay(self):
        # 验证路由优化结果的延迟是否正确
        DELAY = []
        for VL_index in range(self.NUMBER_OF_VL):
            source = self.SOURCE[VL_index]
            delay_for_destinations = []
            for destionation_index in range(len(self.DESTINATION[VL_index])):
                destionation = self.DESTINATION[VL_index][ destionation_index ]
                delay_introduced = 0
                following_node, indicator = destionation, 1  # 从destination出发寻找source
                while following_node != source and indicator:
                    indicator = 0
                    for node_index in range(self.NUMBER_OF_NODES):
                        if self.Y_FOR_RETURN[VL_index][node_index][following_node] == 1:
                            delay_introduced += 2 * self.MTU[VL_index] / self.BANDWIDTH_OF_NODES[node_index]
                            following_node = node_index
                            indicator = 1  # 找到前一个结点
                            break

                if following_node == source:
                    delay_for_destinations.append(delay_introduced)
                    continue
                if delay_introduced >= self.DELAY_BOUND_LEFT[VL_index][destionation_index]:
                    print("Routing for destionation %d is wrong!" % (destionation))
                    return False
            DELAY.append(delay_for_destinations)
        print("DELAY:", DELAY)
        print("DELAY OF NODES:", self.DELAY_OF_NODES_FOR_RETURN)
        return True

    def verify_results_of_routes_optimization(self):
        if self.verify_routing_connections():
            print("Connections qualified!" )
            if self.verify_routing_capacity():
                print("Capacity qualified!")
                if self.verify_routing_bandwidth():
                    print("Bandwidth qualified!")
                    if self.verify_routing_delay():
                        print("Delay qualified!" )
                    else:
                        print("Delay unqualified!")
                else:
                    print("Bandwidth unqualified!")
            else:
                print("Capacity unqualified!")
        else:
            print("Connections unqualified!")