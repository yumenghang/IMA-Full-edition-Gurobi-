import numpy as np
import Hyper_Parameters

class DATA_LOADING_OF_ROUTES_PATH_PROCESSING():
    def __init__(self, topology_type, task, net_type):
        self.topology_type = topology_type
        self.task = task
        self.net_type = net_type
        self.LOAD_FILE_1 = Hyper_Parameters.intermediate_data_file # 加载消息预处理过程中的中间文件
        self.LOAD_FILE_2 = Hyper_Parameters.vl_dict_file # 加载建立虚链路过程中的中间文件
        self.LOAD_FILE_3 = Hyper_Parameters.routes_file # 加载寻找虚链路路由过程中的中间文件

        self.PHYSICAL_PORTS_INFORMATION_PATH = self.LOAD_FILE_1 + "physical_ports_information.npy"
        self.MESSAGES_INFO_PATH = self.LOAD_FILE_1 + "messages_info.npy"
        self.PHYSICAL_PORTS_ADJACENT_MATRIX_PATH = self.LOAD_FILE_1 + "physical_ports_adjacent_matrix.txt"
        self.PHYSICAL_PORTS_INDEX_PATH = self.LOAD_FILE_1 + "physical_ports_index.npy"
        self.PHYSICAL_PORTS_INDEX_REVERSED_PATH = self.LOAD_FILE_1 + "physical_ports_index_reversed.npy"

    def data_loading_of_routes_path_processing(self):
        physical_ports_information = np.load(self.PHYSICAL_PORTS_INFORMATION_PATH, allow_pickle="TRUE").item()
        messages_info = np.load(self.MESSAGES_INFO_PATH, allow_pickle="TRUE").item()
        physical_ports_index = np.load(self.PHYSICAL_PORTS_INDEX_PATH, allow_pickle="TRUE").item()
        physical_ports_index_reversed = np.load(self.PHYSICAL_PORTS_INDEX_REVERSED_PATH, allow_pickle="TRUE").item()
        physical_ports_adjacent_matrix = []
        f_read = open(self.PHYSICAL_PORTS_ADJACENT_MATRIX_PATH, "r")
        for line in f_read:
            intermediate = []
            records = line
            records = records.split()
            for record in records:
                intermediate.append(int(record))
            physical_ports_adjacent_matrix.append(intermediate)

        if self.topology_type == "AFDX":
            if self.net_type == "A":
                if self.task == "usage":
                    arinc664_physical_ports_index_for_A_net = np.load(self.LOAD_FILE_1 + "ARINC664_PHYSICAL_PORTS_INDEX_FOR_A_NET.npy", allow_pickle="TRUE").item()
                    arinc664_physical_ports_index_reversed_for_A_net = np.load(self.LOAD_FILE_1 + "ARINC664_PHYSICAL_PORTS_INDEX_REVERSED_FOR_A_NET.npy", allow_pickle="TRUE").item()
                    arinc664_physical_ports_connections_for_A_net = []
                    f_read = open(self.LOAD_FILE_1 + "ARINC664_PHYSICAL_PORTS_CONNECTIONS_OF_NET_A.txt", "r")
                    for line in f_read:
                        intermediate = []
                        records = line
                        records = records.split()
                        for record in records:
                            intermediate.append(int(record))
                        arinc664_physical_ports_connections_for_A_net.append(intermediate)

                    SOURCE_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_OF_AFDX = np.load(self.LOAD_FILE_3 + "SOURCE_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_OF_AFDX.npy", allow_pickle="TRUE")
                    ARINC664_DESTINATIONS_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_NO_REPETITION_OF_AFDX = np.load(self.LOAD_FILE_3 + "ARINC664_DESTINATIONS_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_NO_REPETITION_OF_AFDX.npy", allow_pickle="TRUE")
                    MTU_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_OF_AFDX = np.load(self.LOAD_FILE_3 + "MTU_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_OF_AFDX.npy", allow_pickle="TRUE")
                    BAG_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_OF_AFDX = np.load(self.LOAD_FILE_3 + "BAG_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_OF_AFDX.npy", allow_pickle="TRUE")
                    DELAY_BOUND_LFET_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_NO_REPETITION_OF_AFDX = np.load(self.LOAD_FILE_3 + "DELAY_BOUND_LFET_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_NO_REPETITION_OF_AFDX.npy", allow_pickle="TRUE")
                    TOTAL_Y_FOR_RETURN_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_OF_AFDX = np.load(self.LOAD_FILE_3 + "TOTAL_Y_FOR_RETURN_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_OF_AFDX.npy", allow_pickle="TRUE")
                    VL_DICT_OF_A_NET_OF_AFDX = np.load(self.LOAD_FILE_2 + "VL_DICT_OF_A_NET_OF_AFDX.npy", allow_pickle="TRUE").item()
                    BANDWIDTH_OF_NODES_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_OF_AFDX = np.load(self.LOAD_FILE_3 + "BANDWIDTH_OF_NODES_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_OF_AFDX.npy", allow_pickle="TRUE")
                    return physical_ports_information, \
                           messages_info, \
                           physical_ports_adjacent_matrix, \
                           physical_ports_index, \
                           physical_ports_index_reversed, \
                           arinc664_physical_ports_connections_for_A_net, \
                           arinc664_physical_ports_index_for_A_net, \
                           arinc664_physical_ports_index_reversed_for_A_net, \
                           SOURCE_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_OF_AFDX, \
                           ARINC664_DESTINATIONS_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_NO_REPETITION_OF_AFDX, \
                           MTU_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_OF_AFDX, \
                           BAG_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_OF_AFDX, \
                           DELAY_BOUND_LFET_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_NO_REPETITION_OF_AFDX, \
                           TOTAL_Y_FOR_RETURN_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_OF_AFDX, \
                           VL_DICT_OF_A_NET_OF_AFDX, \
                           BANDWIDTH_OF_NODES_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_OF_AFDX
                if self.task == "usage_and_loading":
                    arinc664_physical_ports_index_for_A_net = np.load(self.LOAD_FILE_1 + "ARINC664_PHYSICAL_PORTS_INDEX_FOR_A_NET.npy", allow_pickle="TRUE").item()
                    arinc664_physical_ports_index_reversed_for_A_net = np.load(self.LOAD_FILE_1 + "ARINC664_PHYSICAL_PORTS_INDEX_REVERSED_FOR_A_NET.npy", allow_pickle="TRUE").item()
                    arinc664_physical_ports_connections_for_A_net = []
                    f_read = open(self.LOAD_FILE_1 + "ARINC664_PHYSICAL_PORTS_CONNECTIONS_OF_NET_A.txt", "r")
                    for line in f_read:
                        intermediate = []
                        records = line
                        records = records.split()
                        for record in records:
                            intermediate.append(int(record))
                        arinc664_physical_ports_connections_for_A_net.append(intermediate)

                    SOURCE_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_OF_AFDX = np.load(self.LOAD_FILE_3 + "SOURCE_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_OF_AFDX.npy", allow_pickle="TRUE")
                    ARINC664_DESTINATIONS_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_NO_REPETITION_OF_AFDX = np.load(self.LOAD_FILE_3 + "ARINC664_DESTINATIONS_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_NO_REPETITION_OF_AFDX.npy", allow_pickle="TRUE")
                    MTU_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_OF_AFDX = np.load(self.LOAD_FILE_3 + "MTU_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_OF_AFDX.npy", allow_pickle="TRUE")
                    BAG_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_OF_AFDX = np.load(self.LOAD_FILE_3 + "BAG_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_OF_AFDX.npy", allow_pickle="TRUE")
                    DELAY_BOUND_LFET_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_NO_REPETITION_OF_AFDX = np.load(self.LOAD_FILE_3 + "DELAY_BOUND_LFET_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_NO_REPETITION_OF_AFDX.npy", allow_pickle="TRUE")
                    TOTAL_Y_FOR_RETURN_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_OF_AFDX = np.load(self.LOAD_FILE_3 + "TOTAL_Y_FOR_RETURN_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_OF_AFDX.npy", allow_pickle="TRUE")
                    VL_DICT_OF_A_NET_OF_AFDX = np.load(self.LOAD_FILE_2 + "VL_DICT_OF_A_NET_OF_AFDX.npy", allow_pickle="TRUE").item()
                    BANDWIDTH_OF_NODES_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_OF_AFDX = np.load(self.LOAD_FILE_3 + "BANDWIDTH_OF_NODES_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_OF_AFDX.npy", allow_pickle="TRUE")
                    return physical_ports_information, \
                           messages_info, \
                           physical_ports_adjacent_matrix, \
                           physical_ports_index, \
                           physical_ports_index_reversed, \
                           arinc664_physical_ports_connections_for_A_net, \
                           arinc664_physical_ports_index_for_A_net, \
                           arinc664_physical_ports_index_reversed_for_A_net, \
                           SOURCE_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_OF_AFDX, \
                           ARINC664_DESTINATIONS_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_NO_REPETITION_OF_AFDX, \
                           MTU_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_OF_AFDX, \
                           BAG_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_OF_AFDX, \
                           DELAY_BOUND_LFET_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_NO_REPETITION_OF_AFDX, \
                           TOTAL_Y_FOR_RETURN_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_OF_AFDX, \
                           VL_DICT_OF_A_NET_OF_AFDX, \
                           BANDWIDTH_OF_NODES_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_OF_AFDX
                #if self.task == ""
            else:
                if self.task == "usage":
                    arinc664_physical_ports_index_for_B_net = np.load(self.LOAD_FILE_1 + "ARINC664_PHYSICAL_PORTS_INDEX_FOR_B_NET.npy", allow_pickle="TRUE").item()
                    arinc664_physical_ports_index_reversed_for_B_net = np.load(self.LOAD_FILE_1 + "ARINC664_PHYSICAL_PORTS_INDEX_REVERSED_FOR_B_NET.npy", allow_pickle="TRUE").item()
                    arinc664_physical_ports_connections_for_B_net = []
                    f_read = open(self.LOAD_FILE_1 + "ARINC664_PHYSICAL_PORTS_CONNECTIONS_OF_NET_B.txt", "r")
                    for line in f_read:
                        intermediate = []
                        records = line
                        records = records.split()
                        for record in records:
                            intermediate.append(int(record))
                        arinc664_physical_ports_connections_for_B_net.append(intermediate)

                    SOURCE_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_OF_AFDX = np.load(self.LOAD_FILE_3 + "SOURCE_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_OF_AFDX.npy", allow_pickle="TRUE")
                    ARINC664_DESTINATIONS_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_NO_REPETITION_OF_AFDX = np.load(self.LOAD_FILE_3 + "ARINC664_DESTINATIONS_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_NO_REPETITION_OF_AFDX.npy", allow_pickle="TRUE")
                    MTU_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_OF_AFDX = np.load(self.LOAD_FILE_3 + "MTU_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_OF_AFDX.npy", allow_pickle="TRUE")
                    BAG_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_OF_AFDX = np.load(self.LOAD_FILE_3 + "BAG_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_OF_AFDX.npy", allow_pickle="TRUE")
                    DELAY_BOUND_LFET_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_NO_REPETITION_OF_AFDX = np.load(self.LOAD_FILE_3 + "DELAY_BOUND_LFET_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_NO_REPETITION_OF_AFDX.npy", allow_pickle="TRUE")
                    TOTAL_Y_FOR_RETURN_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_OF_AFDX = np.load(self.LOAD_FILE_3 + "TOTAL_Y_FOR_RETURN_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_OF_AFDX.npy", allow_pickle="TRUE")
                    VL_DICT_OF_B_NET_OF_AFDX = np.load(self.LOAD_FILE_2 + "VL_DICT_OF_B_NET_OF_AFDX.npy", allow_pickle="TRUE").item()
                    BANDWIDTH_OF_NODES_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_OF_AFDX = np.load(self.LOAD_FILE_3 + "BANDWIDTH_OF_NODES_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_OF_AFDX.npy", allow_pickle="TRUE")
                    return physical_ports_information, \
                           messages_info, \
                           physical_ports_adjacent_matrix, \
                           physical_ports_index, \
                           physical_ports_index_reversed, \
                           arinc664_physical_ports_connections_for_B_net, \
                           arinc664_physical_ports_index_for_B_net, \
                           arinc664_physical_ports_index_reversed_for_B_net, \
                           SOURCE_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_OF_AFDX, \
                           ARINC664_DESTINATIONS_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_NO_REPETITION_OF_AFDX, \
                           MTU_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_OF_AFDX, \
                           BAG_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_OF_AFDX, \
                           DELAY_BOUND_LFET_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_NO_REPETITION_OF_AFDX, \
                           TOTAL_Y_FOR_RETURN_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_OF_AFDX, \
                           VL_DICT_OF_B_NET_OF_AFDX, \
                           BANDWIDTH_OF_NODES_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_OF_AFDX
                if self.task == "usage_and_loading":
                    arinc664_physical_ports_index_for_B_net = np.load(self.LOAD_FILE_1 + "ARINC664_PHYSICAL_PORTS_INDEX_FOR_B_NET.npy", allow_pickle="TRUE").item()
                    arinc664_physical_ports_index_reversed_for_B_net = np.load(self.LOAD_FILE_1 + "ARINC664_PHYSICAL_PORTS_INDEX_REVERSED_FOR_B_NET.npy", allow_pickle="TRUE").item()
                    arinc664_physical_ports_connections_for_B_net = []
                    f_read = open(self.LOAD_FILE_1 + "ARINC664_PHYSICAL_PORTS_CONNECTIONS_OF_NET_B.txt", "r")
                    for line in f_read:
                        intermediate = []
                        records = line
                        records = records.split()
                        for record in records:
                            intermediate.append(int(record))
                        arinc664_physical_ports_connections_for_B_net.append(intermediate)

                    SOURCE_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_OF_AFDX = np.load(self.LOAD_FILE_3 + "SOURCE_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_OF_AFDX.npy", allow_pickle="TRUE")
                    ARINC664_DESTINATIONS_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_NO_REPETITION_OF_AFDX = np.load(self.LOAD_FILE_3 + "ARINC664_DESTINATIONS_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_NO_REPETITION_OF_AFDX.npy", allow_pickle="TRUE")
                    MTU_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_OF_AFDX = np.load(self.LOAD_FILE_3 + "MTU_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_OF_AFDX.npy", allow_pickle="TRUE")
                    BAG_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_OF_AFDX = np.load(self.LOAD_FILE_3 + "BAG_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_OF_AFDX.npy", allow_pickle="TRUE")
                    DELAY_BOUND_LFET_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_NO_REPETITION_OF_AFDX = np.load(self.LOAD_FILE_3 + "DELAY_BOUND_LFET_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_NO_REPETITION_OF_AFDX.npy", allow_pickle="TRUE")
                    TOTAL_Y_FOR_RETURN_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_OF_AFDX = np.load(self.LOAD_FILE_3 + "TOTAL_Y_FOR_RETURN_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_OF_AFDX.npy", allow_pickle="TRUE")
                    VL_DICT_OF_B_NET_OF_AFDX = np.load(self.LOAD_FILE_2 + "VL_DICT_OF_B_NET_OF_AFDX.npy", allow_pickle="TRUE").item()
                    BANDWIDTH_OF_NODES_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_OF_AFDX = np.load(self.LOAD_FILE_3 + "BANDWIDTH_OF_NODES_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_OF_AFDX.npy", allow_pickle="TRUE")
                    return physical_ports_information, \
                           messages_info, \
                           physical_ports_adjacent_matrix, \
                           physical_ports_index, \
                           physical_ports_index_reversed, \
                           arinc664_physical_ports_connections_for_B_net, \
                           arinc664_physical_ports_index_for_B_net, \
                           arinc664_physical_ports_index_reversed_for_B_net, \
                           SOURCE_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_OF_AFDX, \
                           ARINC664_DESTINATIONS_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_NO_REPETITION_OF_AFDX, \
                           MTU_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_OF_AFDX, \
                           BAG_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_OF_AFDX, \
                           DELAY_BOUND_LFET_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_NO_REPETITION_OF_AFDX, \
                           TOTAL_Y_FOR_RETURN_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_OF_AFDX, \
                           VL_DICT_OF_B_NET_OF_AFDX, \
                           BANDWIDTH_OF_NODES_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_OF_AFDX
                #if self.task == ""
        else:
            if self.net_type == "A":
                if self.task == "usage":
                    arinc664_physical_ports_index_for_A_net = np.load(self.LOAD_FILE_1 + "ARINC664_PHYSICAL_PORTS_INDEX_FOR_A_NET.npy", allow_pickle="TRUE").item()
                    arinc664_physical_ports_index_reversed_for_A_net = np.load(self.LOAD_FILE_1 + "ARINC664_PHYSICAL_PORTS_INDEX_REVERSED_FOR_A_NET.npy", allow_pickle="TRUE").item()
                    arinc664_physical_ports_connections_for_A_net = []
                    f_read = open(self.LOAD_FILE_1 + "ARINC664_PHYSICAL_PORTS_CONNECTIONS_OF_NET_A.txt", "r")
                    for line in f_read:
                        intermediate = []
                        records = line
                        records = records.split()
                        for record in records:
                            intermediate.append(int(record))
                        arinc664_physical_ports_connections_for_A_net.append(intermediate)

                    SOURCE_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_OF_ARINC664 = np.load(self.LOAD_FILE_3 + "SOURCE_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_OF_ARINC664.npy", allow_pickle="TRUE")
                    ARINC664_DESTINATIONS_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_NO_REPETITION_OF_ARINC664 = np.load(self.LOAD_FILE_3 + "ARINC664_DESTINATIONS_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_NO_REPETITION_OF_ARINC664.npy", allow_pickle="TRUE")
                    MTU_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_OF_ARINC664 = np.load(self.LOAD_FILE_3 + "MTU_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_OF_ARINC664.npy", allow_pickle="TRUE")
                    BAG_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_OF_ARINC664 = np.load(self.LOAD_FILE_3 + "BAG_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_OF_ARINC664.npy", allow_pickle="TRUE")
                    DELAY_BOUND_LFET_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_NO_REPETITION_OF_ARINC664 = np.load(self.LOAD_FILE_3 + "DELAY_BOUND_LFET_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_NO_REPETITION_OF_ARINC664.npy", allow_pickle="TRUE")
                    TOTAL_Y_FOR_RETURN_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_OF_ARINC664 = np.load(self.LOAD_FILE_3 + "TOTAL_Y_FOR_RETURN_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_OF_ARINC664.npy", allow_pickle="TRUE")
                    VL_DICT_OF_A_NET_OF_ARINC664 = np.load(self.LOAD_FILE_2 + "VL_DICT_OF_A_NET_OF_ARINC664.npy", allow_pickle="TRUE").item()
                    BANDWIDTH_OF_NODES_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_OF_ARINC664 = np.load(self.LOAD_FILE_3 + "BANDWIDTH_OF_NODES_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_OF_ARINC664.npy", allow_pickle="TRUE")
                    return physical_ports_information, \
                           messages_info, \
                           physical_ports_adjacent_matrix, \
                           physical_ports_index, \
                           physical_ports_index_reversed, \
                           arinc664_physical_ports_connections_for_A_net, \
                           arinc664_physical_ports_index_for_A_net, \
                           arinc664_physical_ports_index_reversed_for_A_net, \
                           SOURCE_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_OF_ARINC664, \
                           ARINC664_DESTINATIONS_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_NO_REPETITION_OF_ARINC664, \
                           MTU_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_OF_ARINC664, \
                           BAG_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_OF_ARINC664, \
                           DELAY_BOUND_LFET_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_NO_REPETITION_OF_ARINC664, \
                           TOTAL_Y_FOR_RETURN_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_OF_ARINC664, \
                           VL_DICT_OF_A_NET_OF_ARINC664, \
                           BANDWIDTH_OF_NODES_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_OF_ARINC664
                if self.task == "usage_and_loading":
                    arinc664_physical_ports_index_for_A_net = np.load(self.LOAD_FILE_1 + "ARINC664_PHYSICAL_PORTS_INDEX_FOR_A_NET.npy", allow_pickle="TRUE").item()
                    arinc664_physical_ports_index_reversed_for_A_net = np.load(self.LOAD_FILE_1 + "ARINC664_PHYSICAL_PORTS_INDEX_REVERSED_FOR_A_NET.npy", allow_pickle="TRUE").item()
                    arinc664_physical_ports_connections_for_A_net = []
                    f_read = open(self.LOAD_FILE_1 + "ARINC664_PHYSICAL_PORTS_CONNECTIONS_OF_NET_A.txt", "r")
                    for line in f_read:
                        intermediate = []
                        records = line
                        records = records.split()
                        for record in records:
                            intermediate.append(int(record))
                        arinc664_physical_ports_connections_for_A_net.append(intermediate)

                    SOURCE_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_OF_ARINC664 = np.load(self.LOAD_FILE_3 + "SOURCE_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_OF_ARINC664.npy", allow_pickle="TRUE")
                    ARINC664_DESTINATIONS_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_NO_REPETITION_OF_ARINC664 = np.load(self.LOAD_FILE_3 + "ARINC664_DESTINATIONS_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_NO_REPETITION_OF_ARINC664.npy", allow_pickle="TRUE")
                    MTU_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_OF_ARINC664 = np.load(self.LOAD_FILE_3 + "MTU_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_OF_ARINC664.npy", allow_pickle="TRUE")
                    BAG_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_OF_ARINC664 = np.load(self.LOAD_FILE_3 + "BAG_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_OF_ARINC664.npy", allow_pickle="TRUE")
                    DELAY_BOUND_LFET_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_NO_REPETITION_OF_ARINC664 = np.load(self.LOAD_FILE_3 + "DELAY_BOUND_LFET_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_NO_REPETITION_OF_ARINC664.npy", allow_pickle="TRUE")
                    TOTAL_Y_FOR_RETURN_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_OF_ARINC664 = np.load(self.LOAD_FILE_3 + "TOTAL_Y_FOR_RETURN_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_OF_ARINC664.npy", allow_pickle="TRUE")
                    VL_DICT_OF_A_NET_OF_ARINC664 = np.load(self.LOAD_FILE_2 + "VL_DICT_OF_A_NET_OF_ARINC664.npy", allow_pickle="TRUE").item()
                    BANDWIDTH_OF_NODES_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_OF_ARINC664 = np.load(self.LOAD_FILE_3 + "BANDWIDTH_OF_NODES_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_OF_ARINC664.npy", allow_pickle="TRUE")
                    return physical_ports_information, \
                           messages_info, \
                           physical_ports_adjacent_matrix, \
                           physical_ports_index, \
                           physical_ports_index_reversed, \
                           arinc664_physical_ports_connections_for_A_net, \
                           arinc664_physical_ports_index_for_A_net, \
                           arinc664_physical_ports_index_reversed_for_A_net, \
                           SOURCE_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_OF_ARINC664, \
                           ARINC664_DESTINATIONS_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_NO_REPETITION_OF_ARINC664, \
                           MTU_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_OF_ARINC664, \
                           BAG_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_OF_ARINC664, \
                           DELAY_BOUND_LFET_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_NO_REPETITION_OF_ARINC664, \
                           TOTAL_Y_FOR_RETURN_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_OF_ARINC664, \
                           VL_DICT_OF_A_NET_OF_ARINC664, \
                           BANDWIDTH_OF_NODES_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_OF_ARINC664
                #if self.task == ""
            else:
                if self.task == "usage":
                    arinc664_physical_ports_index_for_B_net = np.load(self.LOAD_FILE_1 + "ARINC664_PHYSICAL_PORTS_INDEX_FOR_B_NET.npy", allow_pickle="TRUE").item()
                    arinc664_physical_ports_index_reversed_for_B_net = np.load(self.LOAD_FILE_1 + "ARINC664_PHYSICAL_PORTS_INDEX_REVERSED_FOR_B_NET.npy", allow_pickle="TRUE").item()
                    arinc664_physical_ports_connections_for_B_net = []
                    f_read = open(self.LOAD_FILE_1 + "ARINC664_PHYSICAL_PORTS_CONNECTIONS_OF_NET_B.txt", "r")
                    for line in f_read:
                        intermediate = []
                        records = line
                        records = records.split()
                        for record in records:
                            intermediate.append(int(record))
                        arinc664_physical_ports_connections_for_B_net.append(intermediate)

                    SOURCE_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_OF_ARINC664 = np.load(self.LOAD_FILE_3 + "SOURCE_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_OF_ARINC664.npy", allow_pickle="TRUE")
                    ARINC664_DESTINATIONS_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_NO_REPETITION_OF_ARINC664 = np.load(self.LOAD_FILE_3 + "ARINC664_DESTINATIONS_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_NO_REPETITION_OF_ARINC664.npy", allow_pickle="TRUE")
                    MTU_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_OF_ARINC664 = np.load(self.LOAD_FILE_3 + "MTU_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_OF_ARINC664.npy", allow_pickle="TRUE")
                    BAG_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_OF_ARINC664 = np.load(self.LOAD_FILE_3 + "BAG_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_OF_ARINC664.npy", allow_pickle="TRUE")
                    DELAY_BOUND_LFET_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_NO_REPETITION_OF_ARINC664 = np.load(self.LOAD_FILE_3 + "DELAY_BOUND_LFET_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_NO_REPETITION_OF_ARINC664.npy", allow_pickle="TRUE")
                    TOTAL_Y_FOR_RETURN_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_OF_ARINC664 = np.load(self.LOAD_FILE_3 + "TOTAL_Y_FOR_RETURN_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_OF_ARINC664.npy", allow_pickle="TRUE")
                    VL_DICT_OF_B_NET_OF_ARINC664 = np.load(self.LOAD_FILE_2 + "VL_DICT_OF_B_NET_OF_ARINC664.npy", allow_pickle="TRUE").item()
                    BANDWIDTH_OF_NODES_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_OF_ARINC664 = np.load(self.LOAD_FILE_3 + "BANDWIDTH_OF_NODES_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_OF_ARINC664.npy", allow_pickle="TRUE")
                    return physical_ports_information, \
                           messages_info, \
                           physical_ports_adjacent_matrix, \
                           physical_ports_index, \
                           physical_ports_index_reversed, \
                           arinc664_physical_ports_connections_for_B_net, \
                           arinc664_physical_ports_index_for_B_net, \
                           arinc664_physical_ports_index_reversed_for_B_net, \
                           SOURCE_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_OF_ARINC664, \
                           ARINC664_DESTINATIONS_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_NO_REPETITION_OF_ARINC664, \
                           MTU_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_OF_ARINC664, \
                           BAG_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_OF_ARINC664, \
                           DELAY_BOUND_LFET_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_NO_REPETITION_OF_ARINC664, \
                           TOTAL_Y_FOR_RETURN_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_OF_ARINC664, \
                           VL_DICT_OF_B_NET_OF_ARINC664, \
                           BANDWIDTH_OF_NODES_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_OF_ARINC664
                if self.task == "usage_and_loading":
                    arinc664_physical_ports_index_for_B_net = np.load(self.LOAD_FILE_1 + "ARINC664_PHYSICAL_PORTS_INDEX_FOR_B_NET.npy", allow_pickle="TRUE").item()
                    arinc664_physical_ports_index_reversed_for_B_net = np.load(self.LOAD_FILE_1 + "ARINC664_PHYSICAL_PORTS_INDEX_REVERSED_FOR_B_NET.npy", allow_pickle="TRUE").item()
                    arinc664_physical_ports_connections_for_B_net = []
                    f_read = open(self.LOAD_FILE_1 + "ARINC664_PHYSICAL_PORTS_CONNECTIONS_OF_NET_B.txt", "r")
                    for line in f_read:
                        intermediate = []
                        records = line
                        records = records.split()
                        for record in records:
                            intermediate.append(int(record))
                        arinc664_physical_ports_connections_for_B_net.append(intermediate)

                    SOURCE_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_OF_ARINC664 = np.load(self.LOAD_FILE_3 + "SOURCE_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_OF_ARINC664.npy", allow_pickle="TRUE")
                    ARINC664_DESTINATIONS_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_NO_REPETITION_OF_ARINC664 = np.load(self.LOAD_FILE_3 + "ARINC664_DESTINATIONS_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_NO_REPETITION_OF_ARINC664.npy", allow_pickle="TRUE")
                    MTU_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_OF_ARINC664 = np.load(self.LOAD_FILE_3 + "MTU_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_OF_ARINC664.npy", allow_pickle="TRUE")
                    BAG_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_OF_ARINC664 = np.load(self.LOAD_FILE_3 + "BAG_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_OF_ARINC664.npy", allow_pickle="TRUE")
                    DELAY_BOUND_LFET_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_NO_REPETITION_OF_ARINC664 = np.load(self.LOAD_FILE_3 + "DELAY_BOUND_LFET_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_NO_REPETITION_OF_ARINC664.npy", allow_pickle="TRUE")
                    TOTAL_Y_FOR_RETURN_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_OF_ARINC664 = np.load(self.LOAD_FILE_3 + "TOTAL_Y_FOR_RETURN_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_OF_ARINC664.npy", allow_pickle="TRUE")
                    VL_DICT_OF_B_NET_OF_ARINC664 = np.load(self.LOAD_FILE_2 + "VL_DICT_OF_B_NET_OF_ARINC664.npy", allow_pickle="TRUE").item()
                    BANDWIDTH_OF_NODES_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_OF_ARINC664 = np.load(self.LOAD_FILE_3 + "BANDWIDTH_OF_NODES_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_OF_ARINC664.npy", allow_pickle="TRUE")
                    return physical_ports_information, \
                           messages_info, \
                           physical_ports_adjacent_matrix, \
                           physical_ports_index, \
                           physical_ports_index_reversed, \
                           arinc664_physical_ports_connections_for_B_net, \
                           arinc664_physical_ports_index_for_B_net, \
                           arinc664_physical_ports_index_reversed_for_B_net, \
                           SOURCE_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_OF_ARINC664, \
                           ARINC664_DESTINATIONS_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_NO_REPETITION_OF_ARINC664, \
                           MTU_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_OF_ARINC664, \
                           BAG_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_OF_ARINC664, \
                           DELAY_BOUND_LFET_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_NO_REPETITION_OF_ARINC664, \
                           TOTAL_Y_FOR_RETURN_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_OF_ARINC664, \
                           VL_DICT_OF_B_NET_OF_ARINC664, \
                           BANDWIDTH_OF_NODES_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_OF_ARINC664
                #if self.task == ""