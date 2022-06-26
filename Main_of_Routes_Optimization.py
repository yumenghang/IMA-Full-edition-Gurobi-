import numpy as np
import os
import Data_Loading_And_Processing_of_Routes_Optimization
import Configuration_of_Routes_Optimization

import Hyper_Parameters


class MAIN_OF_ROUTES_OPTIMIZATION():
    def __init__(self, topology_type, task, net_type):
        self.topology_type = topology_type
        self.task = task
        self.net_type = net_type
        self.SAVE_FILE = Hyper_Parameters.routes_file
        self.MIN_LATENCY = Hyper_Parameters.min_latency
        self.AVERAGE_NUMBER_OF_VL = Hyper_Parameters.average_number_of_vl
        self.GAP = Hyper_Parameters.gap_for_routes_optimization
        self.TIMELIMITED = Hyper_Parameters.time_limited_for_routes_optimization

    def main(self):
        DATA_LOADING_AND_PROCESSING_OF_ROUTES_OPTIMIZATION = Data_Loading_And_Processing_of_Routes_Optimization.DATA_LOADING_AND_PROCESSING_OF_ROUTES_OPTIMIZATION(self.topology_type)
        VL_DICT_OF_A_NET, \
        VL_DICT_OF_B_NET, \
        SOURCE_OF_A_NET, \
        ARINC664_DESTINATIONS_OF_A_NET, \
        DESTINATIONS_OF_A_NET, \
        LOGICAL_DESTINATIONS_OF_A_NET, \
        MTU_OF_A_NET, \
        BAG_OF_A_NET, \
        DELAY_BOUND_OF_A_NET, \
        DELAY_OCCURRED_OF_A_NET, \
        SOURCE_OF_B_NET, \
        ARINC664_DESTINATIONS_OF_B_NET, \
        DESTINATIONS_OF_B_NET, \
        LOGICAL_DESTINATIONS_OF_B_NET, \
        MTU_OF_B_NET, \
        BAG_OF_B_NET, \
        DELAY_BOUND_OF_B_NET, \
        DELAY_OCCURRED_OF_B_NET, \
        arinc664_physical_ports_connections_for_A_net, \
        arinc664_physical_ports_index_for_A_net, \
        arinc664_physical_ports_index_reversed_for_A_net, \
        arinc664_physical_ports_connections_for_B_net, \
        arinc664_physical_ports_index_for_B_net, \
        arinc664_physical_ports_index_reversed_for_B_net, \
        physical_ports_information, \
        messages_info, \
        physical_ports_adjacent_matrix, \
        physical_ports_index, \
        physical_ports_index_reversed = DATA_LOADING_AND_PROCESSING_OF_ROUTES_OPTIMIZATION.main()

        CONFIGURATION_OF_ROUTES_OPTIMIZATION = Configuration_of_Routes_Optimization.CONFIGURATION_OF_ROUTES_OPTIMIZATION(
                                                                                                                         self.MIN_LATENCY,
                                                                                                                         self.AVERAGE_NUMBER_OF_VL,
                                                                                                                         messages_info,
                                                                                                                         physical_ports_information,
                                                                                                                         physical_ports_adjacent_matrix,
                                                                                                                         physical_ports_index,
                                                                                                                         physical_ports_index_reversed
                                                                                                                         )
        if not os.path.exists(self.SAVE_FILE):
            print("%s does not exist!" % (self.SAVE_FILE))
            os.makedirs(self.SAVE_FILE)
            print("Successfully creat %s!" % (self.SAVE_FILE))

        if self.net_type == "A":
            if self.task == "usage":
                TOTAL_X_FOR_RETURN, \
                TOTAL_Y_FOR_RETURN, \
                SOURCE_OF_A_NET, \
                ARINC664_DESTINATIONS_OF_A_NET_NO_REPETITION, \
                DELAY_BOUND_LFET_OF_A_NET_NO_REPETITION, \
                BANDWIDTH_OF_NODES = CONFIGURATION_OF_ROUTES_OPTIMIZATION.minimum_bandwidth_usage_of_A_net(
                                                                                                           arinc664_physical_ports_connections_for_A_net,
                                                                                                           arinc664_physical_ports_index_reversed_for_A_net,
                                                                                                           SOURCE_OF_A_NET,
                                                                                                           MTU_OF_A_NET,
                                                                                                           BAG_OF_A_NET,
                                                                                                           ARINC664_DESTINATIONS_OF_A_NET,
                                                                                                           DELAY_BOUND_OF_A_NET,
                                                                                                           DELAY_OCCURRED_OF_A_NET,
                                                                                                           self.GAP,
                                                                                                           self.TIMELIMITED
                                                                                                           )
                if self.topology_type == "AFDX":
                    np.save(self.SAVE_FILE + "TOTAL_X_FOR_RETURN_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_OF_AFDX.npy", TOTAL_X_FOR_RETURN)
                    np.save(self.SAVE_FILE + "TOTAL_Y_FOR_RETURN_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_OF_AFDX.npy", TOTAL_Y_FOR_RETURN)
                    np.save(self.SAVE_FILE + "SOURCE_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_OF_AFDX.npy", SOURCE_OF_A_NET)
                    np.save(self.SAVE_FILE + "ARINC664_DESTINATIONS_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_NO_REPETITION_OF_AFDX.npy", ARINC664_DESTINATIONS_OF_A_NET_NO_REPETITION)
                    np.save(self.SAVE_FILE + "MTU_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_OF_AFDX.npy", MTU_OF_A_NET)
                    np.save(self.SAVE_FILE + "BAG_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_OF_AFDX.npy", BAG_OF_A_NET)
                    np.save(self.SAVE_FILE + "DELAY_BOUND_LFET_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_NO_REPETITION_OF_AFDX.npy", DELAY_BOUND_LFET_OF_A_NET_NO_REPETITION)
                    np.save(self.SAVE_FILE + "BANDWIDTH_OF_NODES_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_OF_AFDX.npy", BANDWIDTH_OF_NODES)
                else:
                    np.save(self.SAVE_FILE + "TOTAL_X_FOR_RETURN_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_OF_ARINC664.npy", TOTAL_X_FOR_RETURN)
                    np.save(self.SAVE_FILE + "TOTAL_Y_FOR_RETURN_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_OF_ARINC664.npy", TOTAL_Y_FOR_RETURN)
                    np.save(self.SAVE_FILE + "SOURCE_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_OF_ARINC664.npy", SOURCE_OF_A_NET)
                    np.save(self.SAVE_FILE + "ARINC664_DESTINATIONS_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_NO_REPETITION_OF_ARINC664.npy", ARINC664_DESTINATIONS_OF_A_NET_NO_REPETITION)
                    np.save(self.SAVE_FILE + "MTU_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_OF_ARINC664.npy", MTU_OF_A_NET)
                    np.save(self.SAVE_FILE + "BAG_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_OF_ARINC664.npy", BAG_OF_A_NET)
                    np.save(self.SAVE_FILE + "DELAY_BOUND_LFET_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_NO_REPETITION_OF_ARINC664.npy", DELAY_BOUND_LFET_OF_A_NET_NO_REPETITION)
                    np.save(self.SAVE_FILE + "BANDWIDTH_OF_NODES_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_OF_ARINC664.npy", BANDWIDTH_OF_NODES)
            if self.task == "usage_and_loading":
                TOTAL_X_FOR_RETURN, \
                TOTAL_Y_FOR_RETURN, \
                SOURCE_OF_A_NET, \
                ARINC664_DESTINATIONS_OF_A_NET_NO_REPETITION, \
                DELAY_BOUND_LFET_OF_A_NET_NO_REPETITION, \
                BANDWIDTH_OF_NODES = CONFIGURATION_OF_ROUTES_OPTIMIZATION.minimum_bandwidth_usage_and_load_balancing_of_A_net(
                                                                                                                              arinc664_physical_ports_connections_for_A_net,
                                                                                                                              arinc664_physical_ports_index_reversed_for_A_net,
                                                                                                                              SOURCE_OF_A_NET,
                                                                                                                              MTU_OF_A_NET,
                                                                                                                              BAG_OF_A_NET,
                                                                                                                              ARINC664_DESTINATIONS_OF_A_NET,
                                                                                                                              DELAY_BOUND_OF_A_NET,
                                                                                                                              DELAY_OCCURRED_OF_A_NET,
                                                                                                                              self.GAP,
                                                                                                                              self.TIMELIMITED
                                                                                                                              )
                if self.topology_type == "AFDX":
                    np.save(self.SAVE_FILE + "TOTAL_X_FOR_RETURN_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_OF_AFDX.npy", TOTAL_X_FOR_RETURN)
                    np.save(self.SAVE_FILE + "TOTAL_Y_FOR_RETURN_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_OF_AFDX.npy", TOTAL_Y_FOR_RETURN)
                    np.save(self.SAVE_FILE + "SOURCE_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_OF_AFDX.npy", SOURCE_OF_A_NET)
                    np.save(self.SAVE_FILE + "ARINC664_DESTINATIONS_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_NO_REPETITION_OF_AFDX.npy", ARINC664_DESTINATIONS_OF_A_NET_NO_REPETITION)
                    np.save(self.SAVE_FILE + "MTU_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_OF_AFDX.npy", MTU_OF_A_NET)
                    np.save(self.SAVE_FILE + "BAG_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_OF_AFDX.npy", BAG_OF_A_NET)
                    np.save(self.SAVE_FILE + "DELAY_BOUND_LFET_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_NO_REPETITION_OF_AFDX.npy", DELAY_BOUND_LFET_OF_A_NET_NO_REPETITION)
                    np.save(self.SAVE_FILE + "BANDWIDTH_OF_NODES_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_OF_AFDX.npy", BANDWIDTH_OF_NODES)
                else:
                    np.save(self.SAVE_FILE + "TOTAL_X_FOR_RETURN_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_OF_ARINC664.npy", TOTAL_X_FOR_RETURN)
                    np.save(self.SAVE_FILE + "TOTAL_Y_FOR_RETURN_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_OF_ARINC664.npy", TOTAL_Y_FOR_RETURN)
                    np.save(self.SAVE_FILE + "SOURCE_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_OF_ARINC664.npy", SOURCE_OF_A_NET)
                    np.save(self.SAVE_FILE + "ARINC664_DESTINATIONS_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_NO_REPETITION_OF_ARINC664.npy", ARINC664_DESTINATIONS_OF_A_NET_NO_REPETITION)
                    np.save(self.SAVE_FILE + "MTU_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_OF_ARINC664.npy", MTU_OF_A_NET)
                    np.save(self.SAVE_FILE + "BAG_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_OF_ARINC664.npy", BAG_OF_A_NET)
                    np.save(self.SAVE_FILE + "DELAY_BOUND_LFET_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_NO_REPETITION_OF_ARINC664.npy", DELAY_BOUND_LFET_OF_A_NET_NO_REPETITION)
                    np.save(self.SAVE_FILE + "BANDWIDTH_OF_NODES_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_OF_ARINC664.npy", BANDWIDTH_OF_NODES)
            #if self.task == "":
        else:
            if self.task == "usage":
                TOTAL_X_FOR_RETURN, \
                TOTAL_Y_FOR_RETURN, \
                SOURCE_OF_A_NET, \
                ARINC664_DESTINATIONS_OF_B_NET_NO_REPETITION, \
                DELAY_BOUND_LFET_OF_B_NET_NO_REPETITION, \
                BANDWIDTH_OF_NODES = CONFIGURATION_OF_ROUTES_OPTIMIZATION.minimum_bandwidth_usage_of_B_net(
                                                                                                           arinc664_physical_ports_connections_for_B_net,
                                                                                                           arinc664_physical_ports_index_reversed_for_B_net,
                                                                                                           SOURCE_OF_B_NET,
                                                                                                           MTU_OF_B_NET,
                                                                                                           BAG_OF_B_NET,
                                                                                                           ARINC664_DESTINATIONS_OF_B_NET,
                                                                                                           DELAY_BOUND_OF_B_NET,
                                                                                                           DELAY_OCCURRED_OF_B_NET,
                                                                                                           self.GAP,
                                                                                                           self.TIMELIMITED
                                                                                                           )
                if self.topology_type == "AFDX":
                    np.save(self.SAVE_FILE + "TOTAL_X_FOR_RETURN_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_OF_AFDX.npy", TOTAL_X_FOR_RETURN)
                    np.save(self.SAVE_FILE + "TOTAL_Y_FOR_RETURN_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_OF_AFDX.npy", TOTAL_Y_FOR_RETURN)
                    np.save(self.SAVE_FILE + "SOURCE_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_OF_AFDX.npy", SOURCE_OF_B_NET)
                    np.save(self.SAVE_FILE + "ARINC664_DESTINATIONS_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_NO_REPETITION_OF_AFDX.npy", ARINC664_DESTINATIONS_OF_B_NET_NO_REPETITION)
                    np.save(self.SAVE_FILE + "MTU_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_OF_AFDX.npy", MTU_OF_B_NET)
                    np.save(self.SAVE_FILE + "BAG_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_OF_AFDX.npy", BAG_OF_B_NET)
                    np.save(self.SAVE_FILE + "DELAY_BOUND_LFET_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_NO_REPETITION_OF_AFDX.npy", DELAY_BOUND_LFET_OF_B_NET_NO_REPETITION)
                    np.save(self.SAVE_FILE + "BANDWIDTH_OF_NODES_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_OF_AFDX.npy", BANDWIDTH_OF_NODES)
                else:
                    np.save(self.SAVE_FILE + "TOTAL_X_FOR_RETURN_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_OF_ARINC664.npy", TOTAL_X_FOR_RETURN)
                    np.save(self.SAVE_FILE + "TOTAL_Y_FOR_RETURN_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_OF_ARINC664.npy", TOTAL_Y_FOR_RETURN)
                    np.save(self.SAVE_FILE + "SOURCE_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_OF_ARINC664.npy", SOURCE_OF_B_NET)
                    np.save(self.SAVE_FILE + "ARINC664_DESTINATIONS_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_NO_REPETITION_OF_ARINC664.npy", ARINC664_DESTINATIONS_OF_B_NET_NO_REPETITION)
                    np.save(self.SAVE_FILE + "MTU_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_OF_ARINC664.npy", MTU_OF_B_NET)
                    np.save(self.SAVE_FILE + "BAG_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_OF_ARINC664.npy", BAG_OF_B_NET)
                    np.save(self.SAVE_FILE + "DELAY_BOUND_LFET_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_NO_REPETITION_OF_ARINC664.npy", DELAY_BOUND_LFET_OF_B_NET_NO_REPETITION)
                    np.save(self.SAVE_FILE + "BANDWIDTH_OF_NODES_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_OF_ARINC664.npy", BANDWIDTH_OF_NODES)
            if self.task == "usage_and_loading":
                TOTAL_X_FOR_RETURN, \
                TOTAL_Y_FOR_RETURN, \
                SOURCE_OF_B_NET, \
                ARINC664_DESTINATIONS_OF_B_NET_NO_REPETITION, \
                DELAY_BOUND_LFET_OF_B_NET_NO_REPETITION, \
                BANDWIDTH_OF_NODES = CONFIGURATION_OF_ROUTES_OPTIMIZATION.minimum_bandwidth_usage_and_load_balancing_of_B_net(
                                                                                                                              arinc664_physical_ports_connections_for_B_net,
                                                                                                                              arinc664_physical_ports_index_reversed_for_B_net,
                                                                                                                              SOURCE_OF_B_NET,
                                                                                                                              MTU_OF_B_NET,
                                                                                                                              BAG_OF_B_NET,
                                                                                                                              ARINC664_DESTINATIONS_OF_B_NET,
                                                                                                                              DELAY_BOUND_OF_B_NET,
                                                                                                                              DELAY_OCCURRED_OF_B_NET,
                                                                                                                              self.GAP,
                                                                                                                              self.TIMELIMITED
                                                                                                                              )
                if self.topology_type == "AFDX":
                    np.save(self.SAVE_FILE + "TOTAL_X_FOR_RETURN_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_OF_AFDX.npy", TOTAL_X_FOR_RETURN)
                    np.save(self.SAVE_FILE + "TOTAL_Y_FOR_RETURN_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_OF_AFDX.npy", TOTAL_Y_FOR_RETURN)
                    np.save(self.SAVE_FILE + "SOURCE_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_OF_AFDX.npy", SOURCE_OF_B_NET)
                    np.save(self.SAVE_FILE + "ARINC664_DESTINATIONS_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_NO_REPETITION_OF_AFDX.npy", ARINC664_DESTINATIONS_OF_B_NET_NO_REPETITION)
                    np.save(self.SAVE_FILE + "MTU_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_OF_AFDX.npy", MTU_OF_B_NET)
                    np.save(self.SAVE_FILE + "BAG_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_OF_AFDX.npy", BAG_OF_B_NET)
                    np.save(self.SAVE_FILE + "DELAY_BOUND_LFET_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_NO_REPETITION_OF_AFDX.npy", DELAY_BOUND_LFET_OF_B_NET_NO_REPETITION)
                    np.save(self.SAVE_FILE + "BANDWIDTH_OF_NODES_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_OF_AFDX.npy", BANDWIDTH_OF_NODES)
                else:
                    np.save(self.SAVE_FILE + "TOTAL_X_FOR_RETURN_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_OF_ARINC664.npy", TOTAL_X_FOR_RETURN)
                    np.save(self.SAVE_FILE + "TOTAL_Y_FOR_RETURN_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_OF_ARINC664.npy", TOTAL_Y_FOR_RETURN)
                    np.save(self.SAVE_FILE + "SOURCE_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_OF_ARINC664.npy", SOURCE_OF_B_NET)
                    np.save(self.SAVE_FILE + "ARINC664_DESTINATIONS_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_NO_REPETITION_OF_ARINC664.npy", ARINC664_DESTINATIONS_OF_B_NET_NO_REPETITION)
                    np.save(self.SAVE_FILE + "MTU_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_OF_ARINC664.npy", MTU_OF_B_NET)
                    np.save(self.SAVE_FILE + "BAG_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_OF_ARINC664.npy", BAG_OF_B_NET)
                    np.save(self.SAVE_FILE + "DELAY_BOUND_LFET_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_NO_REPETITION_OF_ARINC664.npy", DELAY_BOUND_LFET_OF_B_NET_NO_REPETITION)
                    np.save(self.SAVE_FILE + "BANDWIDTH_OF_NODES_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_OF_ARINC664.npy", BANDWIDTH_OF_NODES)
            #if self.task == "":