import Optimization_Model_of_Routes_Optimization
import Verify_Results_of_Routes_Optimization
import math

class CONFIGURATION_OF_ROUTES_OPTIMIZATION():
    def __init__(
                 self,
                 MIN_LATENCY,
                 AVERAGE_NUMBER_OF_VL,
                 messages_info,
                 physical_ports_information,
                 physical_ports_adjacent_matrix,
                 physical_ports_index,
                 physical_ports_index_reversed
                ):
        self.MIN_LATENCY = MIN_LATENCY
        self.AVERAGE_NUMBER_OF_VL = AVERAGE_NUMBER_OF_VL # 平均每次求解数目为AVERAGE_NUMBER_OF_VL的虚链路的路径
        self.messages_info = messages_info
        self.physical_ports_information = physical_ports_information
        self.physical_ports_adjacent_matrix = physical_ports_adjacent_matrix
        self.physical_ports_index = physical_ports_index
        self.physical_ports_index_reversed = physical_ports_index_reversed

    def minimum_bandwidth_usage_of_A_net(
                                         self,
                                         arinc664_physical_ports_connections_for_A_net,
                                         arinc664_physical_ports_index_reversed_for_A_net,
                                         SOURCE_OF_A_NET,
                                         MTU_OF_A_NET,
                                         BAG_OF_A_NET,
                                         ARINC664_DESTINATIONS_OF_A_NET,
                                         DELAY_BOUND_OF_A_NET,
                                         DELAY_OCCURRED_OF_A_NET,
                                         GAP,
                                         TIMELIMITED
                                        ):
        """
        数据中存在以下情况，会对路由的优化产生影响，因此，需要先做一些处理：
        1, 在一条虚拟链路中，存在着：一条消息的源节点和目的节点属于同一个物理设备，因此需要将源节点从目的节点列表中去除；
        2, 一条虚拟链路中，存在着多条消息被传输至相同的目的节点，也就是说：一条虚拟链路的目的节点中有重复，所以在优化路由前，先做去重处理
        相应地，一条虚拟链路中，被传输至相同目的节点的消息的延迟也不尽相同，因此，我们只需要考虑同一条虚拟链路中，被传输至相同目的节点的消息中，剩余时间最小的即可
        """
        ARINC664_DESTINATIONS_OF_A_NET_NO_REPETITION = []
        for source_index in range(len(SOURCE_OF_A_NET)):
            ARINC664_DESTINATIONS_OF_A_NET_NO_REPETITION.append(list(set(ARINC664_DESTINATIONS_OF_A_NET[source_index]) - {SOURCE_OF_A_NET[source_index]}))
        DELAY_BOUND_LFET_OF_A_NET_NO_REPETITION = []
        for source_index in range(len(SOURCE_OF_A_NET)):
            delay_bound_left_of_a_net_no_repetition = []
            for destination_index in range(len(ARINC664_DESTINATIONS_OF_A_NET_NO_REPETITION[source_index])):
                min_latency = self.MIN_LATENCY
                for index in range(len(ARINC664_DESTINATIONS_OF_A_NET[source_index])):
                    if ARINC664_DESTINATIONS_OF_A_NET[source_index][index] == ARINC664_DESTINATIONS_OF_A_NET_NO_REPETITION[source_index][destination_index]:
                        min_latency = min(min_latency, DELAY_BOUND_OF_A_NET[source_index][index] - DELAY_OCCURRED_OF_A_NET[source_index][index])
                delay_bound_left_of_a_net_no_repetition.append(min_latency)
            DELAY_BOUND_LFET_OF_A_NET_NO_REPETITION.append(delay_bound_left_of_a_net_no_repetition)

        # 首先处理A网数据
        NUMBER_OF_VL = len(SOURCE_OF_A_NET)
        NUMBER_OF_SUBSETS = math.ceil(NUMBER_OF_VL / self.AVERAGE_NUMBER_OF_VL)
        NUMBER_OF_VL_PER_SUBSET = math.ceil(NUMBER_OF_VL / NUMBER_OF_SUBSETS)
        NUMBER_OF_NODES = len(arinc664_physical_ports_connections_for_A_net)
        BANDWIDTH_OF_NODES = []
        for index in range(NUMBER_OF_NODES):
            BANDWIDTH_OF_NODES.append(1000 * self.physical_ports_information[arinc664_physical_ports_index_reversed_for_A_net[index]][7] )
        print("NUMBER OF VL: %d, NUMBER OF SUBSETS: %d, NUMBER OF VL PER SUBSET: %d!" % (NUMBER_OF_VL, NUMBER_OF_SUBSETS, NUMBER_OF_VL_PER_SUBSET))
        TOTAL_X_FOR_RETURN, TOTAL_Y_FOR_RETURN = [], []
        for subset_index in range(NUMBER_OF_SUBSETS):
            if subset_index + 1 == NUMBER_OF_VL_PER_SUBSET:
                START_INDEX, END_INDEX = NUMBER_OF_VL_PER_SUBSET * subset_index, NUMBER_OF_VL
            else:
                START_INDEX, END_INDEX = NUMBER_OF_VL_PER_SUBSET * subset_index, NUMBER_OF_VL_PER_SUBSET * (subset_index + 1)
            print("VL %d to %d!" % (START_INDEX, END_INDEX))
            print("SOURCE:", SOURCE_OF_A_NET[ START_INDEX: END_INDEX])
            print("DESTINATION:", ARINC664_DESTINATIONS_OF_A_NET_NO_REPETITION[START_INDEX: END_INDEX])
            print("MTU:", MTU_OF_A_NET[ START_INDEX: END_INDEX])
            print("DELAY_BOUND_LFET_OF_A_NET_NO_REPETITION:", DELAY_BOUND_LFET_OF_A_NET_NO_REPETITION[START_INDEX: END_INDEX])
            OPTIMIZATION_MODEL_OF_ROUTES_OPTIMIZATION = Optimization_Model_of_Routes_Optimization.OPTIMIZATION_MODEL_OF_ROUTES_OPTIMIZATION(self.physical_ports_information, BANDWIDTH_OF_NODES)

            X_FOR_RETURN, \
            Y_FOR_RETURN, \
            TOTAL_BANDWIDTH_COST_FOR_RETURN, \
            DELAY_OF_NODES_FOR_RETURN, \
            BANDWIDTH_OF_NODES = OPTIMIZATION_MODEL_OF_ROUTES_OPTIMIZATION.arinc664_routing_optimize_for_minimum_bandwidth_usage(
                                                                                                                                 arinc664_physical_ports_connections_for_A_net,
                                                                                                                                 SOURCE_OF_A_NET[START_INDEX: END_INDEX],
                                                                                                                                 ARINC664_DESTINATIONS_OF_A_NET_NO_REPETITION[START_INDEX: END_INDEX],
                                                                                                                                 MTU_OF_A_NET[START_INDEX: END_INDEX], BAG_OF_A_NET[START_INDEX: END_INDEX],
                                                                                                                                 DELAY_BOUND_LFET_OF_A_NET_NO_REPETITION[START_INDEX: END_INDEX],
                                                                                                                                 GAP,
                                                                                                                                 TIMELIMITED
                                                                                                                                 )
            VERIFY_RESULTS_OF_ROUTES_OPTIMIZATION = Verify_Results_of_Routes_Optimization.VERIFY_RESULTS_OF_ROUTES_OPTIMIZATION(
                                                                                                                                arinc664_physical_ports_connections_for_A_net,
                                                                                                                                arinc664_physical_ports_index_reversed_for_A_net,
                                                                                                                                self.physical_ports_information,
                                                                                                                                SOURCE_OF_A_NET[START_INDEX: END_INDEX],
                                                                                                                                ARINC664_DESTINATIONS_OF_A_NET_NO_REPETITION[START_INDEX: END_INDEX],
                                                                                                                                MTU_OF_A_NET[START_INDEX: END_INDEX],
                                                                                                                                BAG_OF_A_NET[START_INDEX: END_INDEX],
                                                                                                                                DELAY_BOUND_LFET_OF_A_NET_NO_REPETITION[START_INDEX: END_INDEX],
                                                                                                                                X_FOR_RETURN,
                                                                                                                                Y_FOR_RETURN,
                                                                                                                                TOTAL_BANDWIDTH_COST_FOR_RETURN,
                                                                                                                                DELAY_OF_NODES_FOR_RETURN,
                                                                                                                                BANDWIDTH_OF_NODES
                                                                                                                                )
            VERIFY_RESULTS_OF_ROUTES_OPTIMIZATION.verify_results_of_routes_optimization()
            TOTAL_X_FOR_RETURN += X_FOR_RETURN
            TOTAL_Y_FOR_RETURN += Y_FOR_RETURN
        return TOTAL_X_FOR_RETURN, TOTAL_Y_FOR_RETURN, SOURCE_OF_A_NET, ARINC664_DESTINATIONS_OF_A_NET_NO_REPETITION, DELAY_BOUND_LFET_OF_A_NET_NO_REPETITION, BANDWIDTH_OF_NODES

    def minimum_bandwidth_usage_of_B_net(
                                         self,
                                         arinc664_physical_ports_connections_for_B_net,
                                         arinc664_physical_ports_index_reversed_for_B_net,
                                         SOURCE_OF_B_NET,
                                         MTU_OF_B_NET,
                                         BAG_OF_B_NET,
                                         ARINC664_DESTINATIONS_OF_B_NET,
                                         DELAY_BOUND_OF_B_NET,
                                         DELAY_OCCURRED_OF_B_NET,
                                         GAP,
                                         TIMELIMITED
                                         ):
        """
        数据中存在以下情况，会对路由的优化产生影响，因此，需要先做一些处理：
        1, 在一条虚拟链路中，存在着：一条消息的源节点和目的节点属于同一个物理设备，因此需要将源节点从目的节点列表中去除；
        2, 一条虚拟链路中，存在着多条消息被传输至相同的目的节点，也就是说：一条虚拟链路的目的节点中有重复，所以在优化路由前，先做去重处理
        相应地，一条虚拟链路中，被传输至相同目的节点的消息的延迟也不尽相同，因此，我们只需要考虑同一条虚拟链路中，被传输至相同目的节点的消息中，剩余时间最小的即可
        """
        ARINC664_DESTINATIONS_OF_B_NET_NO_REPETITION = []
        for source_index in range(len(SOURCE_OF_B_NET) ):
            ARINC664_DESTINATIONS_OF_B_NET_NO_REPETITION.append(list(set(ARINC664_DESTINATIONS_OF_B_NET[source_index]) - {SOURCE_OF_B_NET[source_index]}))
        DELAY_BOUND_LFET_OF_B_NET_NO_REPETITION = []
        for source_index in range(len(SOURCE_OF_B_NET)):
            delay_bound_left_of_b_net_no_repetition = []
            for destination_index in range(len(ARINC664_DESTINATIONS_OF_B_NET_NO_REPETITION[source_index])):
                min_latency = self.MIN_LATENCY
                for index in range(len(ARINC664_DESTINATIONS_OF_B_NET[source_index])):
                    if ARINC664_DESTINATIONS_OF_B_NET[source_index][index] == ARINC664_DESTINATIONS_OF_B_NET_NO_REPETITION[source_index][destination_index]:
                        min_latency = min(min_latency, DELAY_BOUND_OF_B_NET[source_index][index] - DELAY_OCCURRED_OF_B_NET[source_index][index])
                delay_bound_left_of_b_net_no_repetition.append(min_latency)
            DELAY_BOUND_LFET_OF_B_NET_NO_REPETITION.append(delay_bound_left_of_b_net_no_repetition)

        # 首先处理A网数据
        NUMBER_OF_VL = len(SOURCE_OF_B_NET)
        NUMBER_OF_SUBSETS = math.ceil(NUMBER_OF_VL / self.AVERAGE_NUMBER_OF_VL)
        NUMBER_OF_VL_PER_SUBSET = math.ceil(NUMBER_OF_VL / NUMBER_OF_SUBSETS)
        NUMBER_OF_NODES = len(arinc664_physical_ports_connections_for_B_net)
        BANDWIDTH_OF_NODES = []
        for index in range(NUMBER_OF_NODES):
            BANDWIDTH_OF_NODES.append(1000 * self.physical_ports_information[arinc664_physical_ports_index_reversed_for_B_net[index]][7])
        print("NUMBER OF VL: %d, NUMBER OF SUBSETS: %d, NUMBER OF VL PER SUBSET: %d!" % (NUMBER_OF_VL, NUMBER_OF_SUBSETS, NUMBER_OF_VL_PER_SUBSET))
        TOTAL_X_FOR_RETURN, TOTAL_Y_FOR_RETURN = [], []
        for subset_index in range(NUMBER_OF_SUBSETS):
            if subset_index + 1 == NUMBER_OF_VL_PER_SUBSET:
                START_INDEX, END_INDEX = NUMBER_OF_VL_PER_SUBSET * subset_index, NUMBER_OF_VL
            else:
                START_INDEX, END_INDEX = NUMBER_OF_VL_PER_SUBSET * subset_index, NUMBER_OF_VL_PER_SUBSET * (subset_index + 1)
            print("VL %d to %d!" % (START_INDEX, END_INDEX))
            print("SOURCE:", SOURCE_OF_B_NET[START_INDEX: END_INDEX])
            print("DESTINATION:", ARINC664_DESTINATIONS_OF_B_NET_NO_REPETITION[START_INDEX: END_INDEX])
            print("MTU:", MTU_OF_B_NET[START_INDEX: END_INDEX])
            print("DELAY_BOUND_LFET_OF_A_NET_NO_REPETITION:", DELAY_BOUND_LFET_OF_B_NET_NO_REPETITION[START_INDEX: END_INDEX])
            OPTIMIZATION_MODEL_OF_ROUTES_OPTIMIZATION = Optimization_Model_of_Routes_Optimization.OPTIMIZATION_MODEL_OF_ROUTES_OPTIMIZATION(self.physical_ports_information, BANDWIDTH_OF_NODES)

            X_FOR_RETURN, \
            Y_FOR_RETURN, \
            TOTAL_BANDWIDTH_COST_FOR_RETURN, \
            DELAY_OF_NODES_FOR_RETURN, \
            BANDWIDTH_OF_NODES = OPTIMIZATION_MODEL_OF_ROUTES_OPTIMIZATION.arinc664_routing_optimize_for_minimum_bandwidth_usage(
                                                                                                                                 arinc664_physical_ports_connections_for_B_net,
                                                                                                                                 SOURCE_OF_B_NET[START_INDEX: END_INDEX],
                                                                                                                                 ARINC664_DESTINATIONS_OF_B_NET_NO_REPETITION[START_INDEX: END_INDEX],
                                                                                                                                 MTU_OF_B_NET[START_INDEX: END_INDEX],
                                                                                                                                 BAG_OF_B_NET[START_INDEX: END_INDEX],
                                                                                                                                 DELAY_BOUND_LFET_OF_B_NET_NO_REPETITION[START_INDEX: END_INDEX],
                                                                                                                                 GAP,
                                                                                                                                 TIMELIMITED
                                                                                                                                 )
            VERIFY_RESULTS_OF_ROUTES_OPTIMIZATION = Verify_Results_of_Routes_Optimization.VERIFY_RESULTS_OF_ROUTES_OPTIMIZATION(
                                                                                                                                arinc664_physical_ports_connections_for_B_net,
                                                                                                                                arinc664_physical_ports_index_reversed_for_B_net,
                                                                                                                                self.physical_ports_information,
                                                                                                                                SOURCE_OF_B_NET[START_INDEX: END_INDEX],
                                                                                                                                ARINC664_DESTINATIONS_OF_B_NET_NO_REPETITION[START_INDEX: END_INDEX],
                                                                                                                                MTU_OF_B_NET[START_INDEX: END_INDEX],
                                                                                                                                BAG_OF_B_NET[START_INDEX: END_INDEX],
                                                                                                                                DELAY_BOUND_LFET_OF_B_NET_NO_REPETITION[START_INDEX: END_INDEX],
                                                                                                                                X_FOR_RETURN,
                                                                                                                                Y_FOR_RETURN,
                                                                                                                                TOTAL_BANDWIDTH_COST_FOR_RETURN,
                                                                                                                                DELAY_OF_NODES_FOR_RETURN,
                                                                                                                                BANDWIDTH_OF_NODES
                                                                                                                                )
            VERIFY_RESULTS_OF_ROUTES_OPTIMIZATION.verify_results_of_routes_optimization()
            TOTAL_X_FOR_RETURN += X_FOR_RETURN
            TOTAL_Y_FOR_RETURN += Y_FOR_RETURN
        return TOTAL_X_FOR_RETURN, TOTAL_Y_FOR_RETURN, SOURCE_OF_B_NET, ARINC664_DESTINATIONS_OF_B_NET_NO_REPETITION, DELAY_BOUND_LFET_OF_B_NET_NO_REPETITION, BANDWIDTH_OF_NODES

    def minimum_bandwidth_usage_and_load_balancing_of_A_net(
                                                            self,
                                                            arinc664_physical_ports_connections_for_A_net,
                                                            arinc664_physical_ports_index_reversed_for_A_net,
                                                            SOURCE_OF_A_NET,
                                                            MTU_OF_A_NET,
                                                            BAG_OF_A_NET,
                                                            ARINC664_DESTINATIONS_OF_A_NET,
                                                            DELAY_BOUND_OF_A_NET,
                                                            DELAY_OCCURRED_OF_A_NET,
                                                            GAP,
                                                            TIMELIMITED
                                                            ):
        """
        数据中存在以下情况，会对路由的优化产生影响，因此，需要先做一些处理：
        1, 在一条虚拟链路中，存在着：一条消息的源节点和目的节点属于同一个物理设备，因此需要将源节点从目的节点列表中去除；
        2, 一条虚拟链路中，存在着多条消息被传输至相同的目的节点，也就是说：一条虚拟链路的目的节点中有重复，所以在优化路由前，先做去重处理
        相应地，一条虚拟链路中，被传输至相同目的节点的消息的延迟也不尽相同，因此，我们只需要考虑同一条虚拟链路中，被传输至相同目的节点的消息中，剩余时间最小的即可
        """
        ARINC664_DESTINATIONS_OF_A_NET_NO_REPETITION = []
        for source_index in range(len(SOURCE_OF_A_NET)):
            ARINC664_DESTINATIONS_OF_A_NET_NO_REPETITION.append(list(set(ARINC664_DESTINATIONS_OF_A_NET[source_index]) - {SOURCE_OF_A_NET[source_index]}))
        DELAY_BOUND_LFET_OF_A_NET_NO_REPETITION = []
        for source_index in range(len(SOURCE_OF_A_NET)):
            delay_bound_left_of_a_net_no_repetition = []
            for destination_index in range(len(ARINC664_DESTINATIONS_OF_A_NET_NO_REPETITION[source_index])):
                min_latency = self.MIN_LATENCY
                for index in range(len(ARINC664_DESTINATIONS_OF_A_NET[source_index])):
                    if ARINC664_DESTINATIONS_OF_A_NET[source_index][index] == ARINC664_DESTINATIONS_OF_A_NET_NO_REPETITION[source_index][destination_index]:
                        min_latency = min(min_latency, DELAY_BOUND_OF_A_NET[source_index][index] - DELAY_OCCURRED_OF_A_NET[source_index][index])
                delay_bound_left_of_a_net_no_repetition.append(min_latency)
            DELAY_BOUND_LFET_OF_A_NET_NO_REPETITION.append(delay_bound_left_of_a_net_no_repetition)

        # 首先处理A网数据
        NUMBER_OF_VL = len(SOURCE_OF_A_NET)
        NUMBER_OF_SUBSETS = math.ceil(NUMBER_OF_VL / self.AVERAGE_NUMBER_OF_VL)
        NUMBER_OF_VL_PER_SUBSET = math.ceil(NUMBER_OF_VL / NUMBER_OF_SUBSETS)
        NUMBER_OF_NODES = len(arinc664_physical_ports_connections_for_A_net)
        BANDWIDTH_OF_NODES = []
        for index in range(NUMBER_OF_NODES):
            BANDWIDTH_OF_NODES.append(1000 * self.physical_ports_information[arinc664_physical_ports_index_reversed_for_A_net[index]][7])
        print("NUMBER OF VL: %d, NUMBER OF SUBSETS: %d, NUMBER OF VL PER SUBSET: %d!" % (NUMBER_OF_VL, NUMBER_OF_SUBSETS, NUMBER_OF_VL_PER_SUBSET))
        TOTAL_X_FOR_RETURN, TOTAL_Y_FOR_RETURN = [], []
        for subset_index in range(NUMBER_OF_SUBSETS):
            if subset_index + 1 == NUMBER_OF_VL_PER_SUBSET:
                START_INDEX, END_INDEX = NUMBER_OF_VL_PER_SUBSET * subset_index, NUMBER_OF_VL
            else:
                START_INDEX, END_INDEX = NUMBER_OF_VL_PER_SUBSET * subset_index, NUMBER_OF_VL_PER_SUBSET * (subset_index + 1)
            print("VL %d to %d!" % (START_INDEX, END_INDEX))
            print("SOURCE:", SOURCE_OF_A_NET[START_INDEX: END_INDEX])
            print("DESTINATION:", ARINC664_DESTINATIONS_OF_A_NET_NO_REPETITION[START_INDEX: END_INDEX])
            print("MTU:", MTU_OF_A_NET[START_INDEX: END_INDEX])
            print("DELAY_BOUND_LFET_OF_A_NET_NO_REPETITION:", DELAY_BOUND_LFET_OF_A_NET_NO_REPETITION[START_INDEX: END_INDEX])
            OPTIMIZATION_MODEL_OF_ROUTES_OPTIMIZATION = Optimization_Model_of_Routes_Optimization.OPTIMIZATION_MODEL_OF_ROUTES_OPTIMIZATION(self.physical_ports_information, BANDWIDTH_OF_NODES)

            X_FOR_RETURN, \
            Y_FOR_RETURN, \
            TOTAL_BANDWIDTH_COST_FOR_RETURN, \
            DELAY_OF_NODES_FOR_RETURN, \
            BANDWIDTH_OF_NODES = OPTIMIZATION_MODEL_OF_ROUTES_OPTIMIZATION.arinc664_routing_optimize_for_minimum_bandwidth_usage_and_load_balancing(
                                                                                                                                                    arinc664_physical_ports_connections_for_A_net,
                                                                                                                                                    SOURCE_OF_A_NET[START_INDEX: END_INDEX],
                                                                                                                                                    ARINC664_DESTINATIONS_OF_A_NET_NO_REPETITION[START_INDEX: END_INDEX],
                                                                                                                                                    MTU_OF_A_NET[START_INDEX: END_INDEX],
                                                                                                                                                    BAG_OF_A_NET[START_INDEX: END_INDEX],
                                                                                                                                                    DELAY_BOUND_LFET_OF_A_NET_NO_REPETITION[START_INDEX: END_INDEX],
                                                                                                                                                    GAP,
                                                                                                                                                    TIMELIMITED
                                                                                                                                                    )
            VERIFY_RESULTS_OF_ROUTES_OPTIMIZATION = Verify_Results_of_Routes_Optimization.VERIFY_RESULTS_OF_ROUTES_OPTIMIZATION(
                                                                                                                                arinc664_physical_ports_connections_for_A_net,
                                                                                                                                arinc664_physical_ports_index_reversed_for_A_net,
                                                                                                                                self.physical_ports_information,
                                                                                                                                SOURCE_OF_A_NET[START_INDEX: END_INDEX],
                                                                                                                                ARINC664_DESTINATIONS_OF_A_NET_NO_REPETITION[START_INDEX: END_INDEX],
                                                                                                                                MTU_OF_A_NET[START_INDEX: END_INDEX],
                                                                                                                                BAG_OF_A_NET[START_INDEX: END_INDEX],
                                                                                                                                DELAY_BOUND_LFET_OF_A_NET_NO_REPETITION[START_INDEX: END_INDEX],
                                                                                                                                X_FOR_RETURN,
                                                                                                                                Y_FOR_RETURN,
                                                                                                                                TOTAL_BANDWIDTH_COST_FOR_RETURN,
                                                                                                                                DELAY_OF_NODES_FOR_RETURN,
                                                                                                                                BANDWIDTH_OF_NODES
                                                                                                                                )
            VERIFY_RESULTS_OF_ROUTES_OPTIMIZATION.verify_results_of_routes_optimization()
            TOTAL_X_FOR_RETURN += X_FOR_RETURN
            TOTAL_Y_FOR_RETURN += Y_FOR_RETURN
        return TOTAL_X_FOR_RETURN, TOTAL_Y_FOR_RETURN, SOURCE_OF_A_NET, ARINC664_DESTINATIONS_OF_A_NET_NO_REPETITION, DELAY_BOUND_LFET_OF_A_NET_NO_REPETITION, BANDWIDTH_OF_NODES


    def minimum_bandwidth_usage_and_load_balancing_of_B_net(
                                                            self,
                                                            arinc664_physical_ports_connections_for_B_net,
                                                            arinc664_physical_ports_index_reversed_for_B_net,
                                                            SOURCE_OF_B_NET,
                                                            MTU_OF_B_NET,
                                                            BAG_OF_B_NET,
                                                            ARINC664_DESTINATIONS_OF_B_NET,
                                                            DELAY_BOUND_OF_B_NET,
                                                            DELAY_OCCURRED_OF_B_NET,
                                                            GAP,
                                                            TIMELIMITED
                                                            ):
        """
        数据中存在以下情况，会对路由的优化产生影响，因此，需要先做一些处理：
        1, 在一条虚拟链路中，存在着：一条消息的源节点和目的节点属于同一个物理设备，因此需要将源节点从目的节点列表中去除；
        2, 一条虚拟链路中，存在着多条消息被传输至相同的目的节点，也就是说：一条虚拟链路的目的节点中有重复，所以在优化路由前，先做去重处理
        相应地，一条虚拟链路中，被传输至相同目的节点的消息的延迟也不尽相同，因此，我们只需要考虑同一条虚拟链路中，被传输至相同目的节点的消息中，剩余时间最小的即可
        """
        ARINC664_DESTINATIONS_OF_B_NET_NO_REPETITION = []
        for source_index in range(len(SOURCE_OF_B_NET)):
            ARINC664_DESTINATIONS_OF_B_NET_NO_REPETITION.append(list(set(ARINC664_DESTINATIONS_OF_B_NET[source_index]) - {SOURCE_OF_B_NET[source_index]}))
        DELAY_BOUND_LFET_OF_B_NET_NO_REPETITION = []
        for source_index in range(len(SOURCE_OF_B_NET)):
            delay_bound_left_of_b_net_no_repetition = []
            for destination_index in range(len(ARINC664_DESTINATIONS_OF_B_NET_NO_REPETITION[source_index])):
                min_latency = self.MIN_LATENCY
                for index in range(len(ARINC664_DESTINATIONS_OF_B_NET[source_index])):
                    if ARINC664_DESTINATIONS_OF_B_NET[source_index][index] == ARINC664_DESTINATIONS_OF_B_NET_NO_REPETITION[source_index][destination_index]:
                        min_latency = min(min_latency, DELAY_BOUND_OF_B_NET[source_index][index] - DELAY_OCCURRED_OF_B_NET[source_index][index])
                delay_bound_left_of_b_net_no_repetition.append(min_latency)
            DELAY_BOUND_LFET_OF_B_NET_NO_REPETITION.append(delay_bound_left_of_b_net_no_repetition)

        # 首先处理A网数据
        NUMBER_OF_VL = len(SOURCE_OF_B_NET)
        NUMBER_OF_SUBSETS = math.ceil(NUMBER_OF_VL / self.AVERAGE_NUMBER_OF_VL)
        NUMBER_OF_VL_PER_SUBSET = math.ceil(NUMBER_OF_VL / NUMBER_OF_SUBSETS)
        NUMBER_OF_NODES = len(arinc664_physical_ports_connections_for_B_net)
        BANDWIDTH_OF_NODES = []
        for index in range(NUMBER_OF_NODES):
            BANDWIDTH_OF_NODES.append(1000 * self.physical_ports_information[arinc664_physical_ports_index_reversed_for_B_net[index]][7])
        print("NUMBER OF VL: %d, NUMBER OF SUBSETS: %d, NUMBER OF VL PER SUBSET: %d!" % (NUMBER_OF_VL, NUMBER_OF_SUBSETS, NUMBER_OF_VL_PER_SUBSET))
        TOTAL_X_FOR_RETURN, TOTAL_Y_FOR_RETURN = [], []
        for subset_index in range(NUMBER_OF_SUBSETS):
            if subset_index + 1 == NUMBER_OF_VL_PER_SUBSET:
                START_INDEX, END_INDEX = NUMBER_OF_VL_PER_SUBSET * subset_index, NUMBER_OF_VL
            else:
                START_INDEX, END_INDEX = NUMBER_OF_VL_PER_SUBSET * subset_index, NUMBER_OF_VL_PER_SUBSET * (subset_index + 1)
            print("VL %d to %d!" % (START_INDEX, END_INDEX))
            print("SOURCE:", SOURCE_OF_B_NET[START_INDEX: END_INDEX])
            print("DESTINATION:", ARINC664_DESTINATIONS_OF_B_NET_NO_REPETITION[START_INDEX: END_INDEX])
            print("MTU:", MTU_OF_B_NET[START_INDEX: END_INDEX])
            print("DELAY_BOUND_LFET_OF_B_NET_NO_REPETITION:", DELAY_BOUND_LFET_OF_B_NET_NO_REPETITION[START_INDEX: END_INDEX])
            OPTIMIZATION_MODEL_OF_ROUTES_OPTIMIZATION = Optimization_Model_of_Routes_Optimization.OPTIMIZATION_MODEL_OF_ROUTES_OPTIMIZATION(self.physical_ports_information, BANDWIDTH_OF_NODES)

            X_FOR_RETURN, \
            Y_FOR_RETURN, \
            TOTAL_BANDWIDTH_COST_FOR_RETURN, \
            DELAY_OF_NODES_FOR_RETURN, \
            BANDWIDTH_OF_NODES = OPTIMIZATION_MODEL_OF_ROUTES_OPTIMIZATION.arinc664_routing_optimize_for_minimum_bandwidth_usage_and_load_balancing(
                                                                                                                                                    arinc664_physical_ports_connections_for_B_net,
                                                                                                                                                    SOURCE_OF_B_NET[START_INDEX: END_INDEX],
                                                                                                                                                    ARINC664_DESTINATIONS_OF_B_NET_NO_REPETITION[START_INDEX: END_INDEX],
                                                                                                                                                    MTU_OF_B_NET[START_INDEX: END_INDEX],
                                                                                                                                                    BAG_OF_B_NET[START_INDEX: END_INDEX],
                                                                                                                                                    DELAY_BOUND_LFET_OF_B_NET_NO_REPETITION[START_INDEX: END_INDEX],
                                                                                                                                                    GAP,
                                                                                                                                                    TIMELIMITED
                                                                                                                                                    )
            VERIFY_RESULTS_OF_ROUTES_OPTIMIZATION = Verify_Results_of_Routes_Optimization.VERIFY_RESULTS_OF_ROUTES_OPTIMIZATION(
                                                                                                                                arinc664_physical_ports_connections_for_B_net,
                                                                                                                                arinc664_physical_ports_index_reversed_for_B_net,
                                                                                                                                self.physical_ports_information,
                                                                                                                                SOURCE_OF_B_NET[START_INDEX: END_INDEX],
                                                                                                                                ARINC664_DESTINATIONS_OF_B_NET_NO_REPETITION[START_INDEX: END_INDEX],
                                                                                                                                MTU_OF_B_NET[START_INDEX: END_INDEX],
                                                                                                                                BAG_OF_B_NET[START_INDEX: END_INDEX],
                                                                                                                                DELAY_BOUND_LFET_OF_B_NET_NO_REPETITION[START_INDEX: END_INDEX],
                                                                                                                                X_FOR_RETURN,
                                                                                                                                Y_FOR_RETURN,
                                                                                                                                TOTAL_BANDWIDTH_COST_FOR_RETURN,
                                                                                                                                DELAY_OF_NODES_FOR_RETURN,
                                                                                                                                BANDWIDTH_OF_NODES
                                                                                                                                )
            VERIFY_RESULTS_OF_ROUTES_OPTIMIZATION.verify_results_of_routes_optimization()
            TOTAL_X_FOR_RETURN += X_FOR_RETURN
            TOTAL_Y_FOR_RETURN += Y_FOR_RETURN
        return TOTAL_X_FOR_RETURN, TOTAL_Y_FOR_RETURN, SOURCE_OF_B_NET, ARINC664_DESTINATIONS_OF_B_NET_NO_REPETITION, DELAY_BOUND_LFET_OF_B_NET_NO_REPETITION, BANDWIDTH_OF_NODES