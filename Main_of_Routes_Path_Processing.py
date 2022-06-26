import numpy as np
import os
import Get_The_Transmitting_Path_of_Messages_of_Routes_Path_Processing
import Data_Loading_of_Routes_Path_Processing
import Hyper_Parameters

class MAIN_OF_ROUTES_PATH_PROCESSING():
    def __init__(self, topology_type, task, net_type):
        self.SAVE_FILE = Hyper_Parameters.messages_routes_file
        self.topology_type = topology_type
        self.task = task
        self.net_type = net_type
        self.GAP = Hyper_Parameters.gap_for_routes_path_processing
        self.TIMELIMITED = Hyper_Parameters.time_limited_for_routes_path_processing

    def main(self):
        if not os.path.exists(self.SAVE_FILE):
            print("%s does not exist!" % (self.SAVE_FILE))
            os.makedirs(self.SAVE_FILE)
            print("Successfully creat %s!" % (self.SAVE_FILE))
        DATA_LOADING_OF_ROUTES_PATH_PROCESSING = Data_Loading_of_Routes_Path_Processing.DATA_LOADING_OF_ROUTES_PATH_PROCESSING(self.topology_type, self.task, self.net_type)

        physical_ports_information, \
        messages_info, \
        physical_ports_adjacent_matrix, \
        physical_ports_index, \
        physical_ports_index_reversed, \
        arinc664_physical_ports_connections, \
        arinc664_physical_ports_index, \
        arinc664_physical_ports_index_reversed, \
        SOURCE, \
        ARINC664_DESTINATIONS, \
        MTU, \
        BAG, \
        DELAY_BOUND_LFET, \
        TOTAL_Y_FOR_RETURN, \
        VL_DICT, \
        BANDWIDTH_OF_NODES = DATA_LOADING_OF_ROUTES_PATH_PROCESSING.data_loading_of_routes_path_processing()

        if self.topology_type == "AFDX":
            GET_THE_TRANSMITTING_PATH_OF_MESSAGES_OF_ROUTES_PATH_PROCESSING = \
                Get_The_Transmitting_Path_of_Messages_of_Routes_Path_Processing.GET_THE_TRANSMITTING_PATH_OF_MESSAGES_OF_ROUTES_PATH_PROCESSING(
                                                                                                                                                physical_ports_information,
                                                                                                                                                messages_info,
                                                                                                                                                physical_ports_adjacent_matrix,
                                                                                                                                                physical_ports_index,
                                                                                                                                                physical_ports_index_reversed,
                                                                                                                                                BANDWIDTH_OF_NODES,
                                                                                                                                                self.GAP,
                                                                                                                                                self.TIMELIMITED
                                                                                                                                                )
            MESSAGES_DICT = GET_THE_TRANSMITTING_PATH_OF_MESSAGES_OF_ROUTES_PATH_PROCESSING.get_the_transmitting_path_of_messages_in_AFDX(
                                                                                                                                          self.net_type,
                                                                                                                                          arinc664_physical_ports_connections,
                                                                                                                                          arinc664_physical_ports_index,
                                                                                                                                          arinc664_physical_ports_index_reversed,
                                                                                                                                          SOURCE,
                                                                                                                                          ARINC664_DESTINATIONS,
                                                                                                                                          MTU,
                                                                                                                                          BAG,
                                                                                                                                          DELAY_BOUND_LFET,
                                                                                                                                          TOTAL_Y_FOR_RETURN,
                                                                                                                                          VL_DICT
                                                                                                                                          )
            if self.net_type == "A":
                if self.task == "usage":
                    np.save(self.SAVE_FILE + "MESSAGES_DICT_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_OF_AFDX.npy", MESSAGES_DICT)
                if self.task == "usage_and_loading":
                    np.save(self.SAVE_FILE + "MESSAGES_DICT_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_OF_AFDX.npy", MESSAGES_DICT)
            else:
                if self.task == "usage":
                    np.save(self.SAVE_FILE + "MESSAGES_DICT_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_OF_AFDX.npy", MESSAGES_DICT)
                if self.task == "usage_and_loading":
                    np.save(self.SAVE_FILE + "MESSAGES_DICT_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_OF_AFDX.npy", MESSAGES_DICT)
        else:
            GET_THE_TRANSMITTING_PATH_OF_MESSAGES_OF_ROUTES_PATH_PROCESSING = \
                Get_The_Transmitting_Path_of_Messages_of_Routes_Path_Processing.GET_THE_TRANSMITTING_PATH_OF_MESSAGES_OF_ROUTES_PATH_PROCESSING(
                                                                                                                                                physical_ports_information,
                                                                                                                                                messages_info,
                                                                                                                                                physical_ports_adjacent_matrix,
                                                                                                                                                physical_ports_index,
                                                                                                                                                physical_ports_index_reversed,
                                                                                                                                                BANDWIDTH_OF_NODES,
                                                                                                                                                self.GAP,
                                                                                                                                                self.TIMELIMITED
                                                                                                                                                )
            MESSAGES_DICT = GET_THE_TRANSMITTING_PATH_OF_MESSAGES_OF_ROUTES_PATH_PROCESSING.get_the_transmitting_path_of_messages_in_AFDX(
                                                                                                                                          self.net_type,
                                                                                                                                          arinc664_physical_ports_connections,
                                                                                                                                          arinc664_physical_ports_index,
                                                                                                                                          arinc664_physical_ports_index_reversed,
                                                                                                                                          SOURCE,
                                                                                                                                          ARINC664_DESTINATIONS,
                                                                                                                                          MTU,
                                                                                                                                          BAG,
                                                                                                                                          DELAY_BOUND_LFET,
                                                                                                                                          TOTAL_Y_FOR_RETURN,
                                                                                                                                          VL_DICT
                                                                                                                                          )
            if self.net_type == "A":
                if self.task == "usage":
                    np.save(self.SAVE_FILE + "MESSAGES_DICT_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_OF_ARINC664.npy", MESSAGES_DICT)
                if self.task == "usage_and_loading":
                    np.save(self.SAVE_FILE + "MESSAGES_DICT_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_OF_ARINC664.npy", MESSAGES_DICT)
            else:
                if self.task == "usage":
                    np.save(self.SAVE_FILE + "MESSAGES_DICT_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_OF_ARINC664.npy", MESSAGES_DICT)
                if self.task == "usage_and_loading":
                    np.save(self.SAVE_FILE + "MESSAGES_DICT_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_OF_ARINC664.npy", MESSAGES_DICT)