import Hyper_Parameters
import numpy as np

class DATA_LOADING_AND_PROCESSING_OF_ROUTES_OPTIMIZATION():
    def __init__(self, topology_type):
        if topology_type == "AFDX":
            self.VL_DICT_OF_A_NET_PATH = Hyper_Parameters.vl_dict_file + "VL_DICT_OF_A_NET_OF_AFDX.npy"
            self.VL_DICT_OF_B_NET_PATH = Hyper_Parameters.vl_dict_file + "VL_DICT_OF_B_NET_OF_AFDX.npy"
        else:
            self.VL_DICT_OF_A_NET_PATH = Hyper_Parameters.vl_dict_file + "VL_DICT_OF_A_NET_OF_ARINC664.npy"
            self.VL_DICT_OF_B_NET_PATH = Hyper_Parameters.vl_dict_file + "VL_DICT_OF_B_NET_OF_ARINC664.npy"
        self.MESSAGES_PER_PHYSICAL_PORT_PATH = Hyper_Parameters.intermediate_data_file + "messages_per_physical_port.npy"
        self.PHYSICAL_PORTS_INFORMATION_PATH = Hyper_Parameters.intermediate_data_file + "physical_ports_information.npy"
        self.MESSAGES_INFO_PATH = Hyper_Parameters.intermediate_data_file + "messages_info.npy"
        self.PHYSICAL_PORTS_ADJACENT_MATRIX_PATH = Hyper_Parameters.intermediate_data_file + "physical_ports_adjacent_matrix.txt"
        self.PHYSICAL_PORTS_INDEX_PATH = Hyper_Parameters.intermediate_data_file + "physical_ports_index.npy"
        self.PHYSICAL_PORTS_INDEX_REVERSED_PATH = Hyper_Parameters.intermediate_data_file + "physical_ports_index_reversed.npy"
        self.ARINC664_PHYSICAL_PORTS_CONNECTIONS_OF_A_NET_PATH = Hyper_Parameters.intermediate_data_file + "ARINC664_PHYSICAL_PORTS_CONNECTIONS_OF_NET_A.txt"
        self.ARINC664_PHYSICAL_PORTS_INDEX_FOR_A_NET_PATH = Hyper_Parameters.intermediate_data_file + "ARINC664_PHYSICAL_PORTS_INDEX_FOR_A_NET.npy"
        self.ARINC664_PHYSICAL_PORTS_INDEX_REVERSED_FOR_A_NET_PATH = Hyper_Parameters.intermediate_data_file + "ARINC664_PHYSICAL_PORTS_INDEX_REVERSED_FOR_A_NET.npy"
        self.ARINC664_PHYSICAL_PORTS_CONNECTIONS_OF_B_NET_PATH = Hyper_Parameters.intermediate_data_file + "ARINC664_PHYSICAL_PORTS_CONNECTIONS_OF_NET_B.txt"
        self.ARINC664_PHYSICAL_PORTS_INDEX_FOR_B_NET_PATH = Hyper_Parameters.intermediate_data_file + "ARINC664_PHYSICAL_PORTS_INDEX_FOR_B_NET.npy"
        self.ARINC664_PHYSICAL_PORTS_INDEX_REVERSED_FOR_B_NET_PATH = Hyper_Parameters.intermediate_data_file + "ARINC664_PHYSICAL_PORTS_INDEX_REVERSED_FOR_B_NET.npy"


    def load_data( self ):
        # 加载全网信息
        VL_DICT_OF_A_NET = np.load(self.VL_DICT_OF_A_NET_PATH, allow_pickle="TRUE").item()
        VL_DICT_OF_B_NET = np.load(self.VL_DICT_OF_B_NET_PATH, allow_pickle="TRUE").item()
        messages_per_physical_port = np.load(self.MESSAGES_PER_PHYSICAL_PORT_PATH, allow_pickle="TRUE").item()
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

        # 加载A网信息
        arinc664_physical_ports_index_for_A_net = np.load(self.ARINC664_PHYSICAL_PORTS_INDEX_FOR_A_NET_PATH, allow_pickle="TRUE").item()
        arinc664_physical_ports_index_reversed_for_A_net = np.load(self.ARINC664_PHYSICAL_PORTS_INDEX_REVERSED_FOR_A_NET_PATH, allow_pickle="TRUE").item()
        arinc664_physical_ports_connections_for_A_net = []
        f_read = open(self.ARINC664_PHYSICAL_PORTS_CONNECTIONS_OF_A_NET_PATH, "r")
        for line in f_read:
            intermediate = []
            records = line
            records = records.split()
            for record in records:
                intermediate.append(int(record))
            arinc664_physical_ports_connections_for_A_net.append(intermediate)

        # 加载B网信息
        arinc664_physical_ports_index_for_B_net = np.load(self.ARINC664_PHYSICAL_PORTS_INDEX_FOR_B_NET_PATH, allow_pickle="TRUE").item()
        arinc664_physical_ports_index_reversed_for_B_net = np.load(self.ARINC664_PHYSICAL_PORTS_INDEX_REVERSED_FOR_B_NET_PATH, allow_pickle="TRUE").item()
        arinc664_physical_ports_connections_for_B_net = []
        f_read = open(self.ARINC664_PHYSICAL_PORTS_CONNECTIONS_OF_B_NET_PATH, "r")
        for line in f_read:
            intermediate = []
            records = line
            records = records.split()
            for record in records:
                intermediate.append(int(record))
            arinc664_physical_ports_connections_for_B_net.append(intermediate)

        return VL_DICT_OF_A_NET, \
               VL_DICT_OF_B_NET, \
               messages_per_physical_port, \
               physical_ports_information, \
               messages_info, \
               physical_ports_adjacent_matrix, \
               physical_ports_index, \
               physical_ports_index_reversed, \
               arinc664_physical_ports_connections_for_A_net, \
               arinc664_physical_ports_index_for_A_net, \
               arinc664_physical_ports_index_reversed_for_A_net, \
               arinc664_physical_ports_connections_for_B_net, \
               arinc664_physical_ports_index_for_B_net, \
               arinc664_physical_ports_index_reversed_for_B_net

    def find_previous_physical_port(
                                    self,
                                    NET_TYPE,
                                    Non_ARINC664_PHYSICAL_PORT_NAME,
                                    physical_ports_information,
                                    physical_ports_adjacent_matrix,
                                    physical_ports_index,
                                    physical_ports_index_reversed
                                    ):
        # 寻找NET_TYPE (A or B)网中，与非ARINC664物理端口Non_ARINC664_PHYSICAL_PORT_NAME相连接的、RDIU设备中相对应的、属于同一NET_TYPE (A or B)网中物理端口名
        index_of_Non_ARINC664_PHYSICAL_PORT_NAME = physical_ports_index[Non_ARINC664_PHYSICAL_PORT_NAME] # 物理端口Non_ARINC664_PHYSICAL_PORT_NAME的index
        for row_index in range(len(physical_ports_adjacent_matrix)):
            if physical_ports_adjacent_matrix[row_index][index_of_Non_ARINC664_PHYSICAL_PORT_NAME] == 1:
                previous_physical_port_name = physical_ports_index_reversed[row_index]
                if physical_ports_information[previous_physical_port_name][6] in ["RDIU_01", "RDIU_02", "RDIU_03", "RDIU_04", "RDIU_05", "RDIU_06", "RDIU_07", "RDIU_08",
                                                                                  "RDIU_09", "RDIU_10", "RDIU_11", "RDIU_12", "RDIU_13", "RDIU_14", "RDIU_15", "RDIU_16"]:
                    if NET_TYPE == "A":
                        return physical_ports_information[previous_physical_port_name][6]+".A"
                    else:
                        return physical_ports_information[previous_physical_port_name][6]+".B"
                #else:
                    #print( physical_ports_information[ previous_physical_port_name ][ 6 ], " There are errors in logical buses! " )

    def process_data(
                     self,
                     VL_DICT_OF_A_NET,
                     VL_DICT_OF_B_NET,
                     physical_ports_information,
                     arinc664_physical_ports_index_for_A_net,
                     arinc664_physical_ports_index_for_B_net,
                     physical_ports_adjacent_matrix,
                     physical_ports_index,
                     physical_ports_index_reversed
                     ):
        SOURCE_OF_A_NET, ARINC664_DESTINATIONS_OF_A_NET, DESTINATIONS_OF_A_NET, LOGICAL_DESTINATIONS_OF_A_NET = [], [], [], []
        MTU_OF_A_NET, BAG_OF_A_NET = [], []
        DELAY_BOUND_OF_A_NET, DELAY_OCCURRED_OF_A_NET = [], []
        SOURCE_OF_B_NET, ARINC664_DESTINATIONS_OF_B_NET, DESTINATIONS_OF_B_NET, LOGICAL_DESTINATIONS_OF_B_NET = [], [], [], []
        MTU_OF_B_NET, BAG_OF_B_NET = [], []
        DELAY_BOUND_OF_B_NET, DELAY_OCCURRED_OF_B_NET = [], []
        # 先处理A网数据
        for key in list(VL_DICT_OF_A_NET.keys()):
            NET_TYPE = "A"
            for VL_index in range(len(VL_DICT_OF_A_NET[key])):
                arinc664_physical_destinations, physical_destination, logical_destinations = [], [], []
                SOURCE_OF_A_NET.append(arinc664_physical_ports_index_for_A_net[key])
                MTU_OF_A_NET.append(VL_DICT_OF_A_NET[key][VL_index][1])
                BAG_OF_A_NET.append(VL_DICT_OF_A_NET[key][VL_index][0])
                delay_bound, delay_occurred = [], []
                for subVL_index in range(len(VL_DICT_OF_A_NET[key][VL_index][5])):
                    for physical_port_name_index in range(len(VL_DICT_OF_A_NET[key][VL_index][5][subVL_index])):
                        physical_port_name = VL_DICT_OF_A_NET[ key ][ VL_index ][ 5][subVL_index][physical_port_name_index]
                        logical_port_name = VL_DICT_OF_A_NET[ key ][ VL_index ][ 4][subVL_index][physical_port_name_index]
                        if physical_ports_information[ physical_port_name ][ 0 ] in [ "AswPhysPort", "AesPhysPort" ]:
                            arinc664_physical_destinations.append( arinc664_physical_ports_index_for_A_net[ physical_port_name ] ) # 该物理端口在A网中的index
                            physical_destination.append( physical_port_name )
                            logical_destinations.append( logical_port_name )
                            delay_bound.append(VL_DICT_OF_A_NET[key][VL_index][6][subVL_index][physical_port_name_index])
                            delay_occurred.append(VL_DICT_OF_A_NET[key][VL_index][7][subVL_index][physical_port_name_index])
                        else:
                            arinc664_destination = self.find_previous_physical_port(
                                                                                    NET_TYPE,
                                                                                    physical_port_name,
                                                                                    physical_ports_information,
                                                                                    physical_ports_adjacent_matrix,
                                                                                    physical_ports_index,
                                                                                    physical_ports_index_reversed
                                                                                    )
                            arinc664_physical_destinations.append(arinc664_physical_ports_index_for_A_net[arinc664_destination])
                            physical_destination.append(physical_port_name)
                            logical_destinations.append(logical_port_name)
                            delay_bound.append(VL_DICT_OF_A_NET[key][VL_index][6][subVL_index][physical_port_name_index])
                            delay_occurred.append(VL_DICT_OF_A_NET[key][VL_index][7][subVL_index][physical_port_name_index])
                ARINC664_DESTINATIONS_OF_A_NET.append( arinc664_physical_destinations)
                DESTINATIONS_OF_A_NET.append(physical_destination)
                LOGICAL_DESTINATIONS_OF_A_NET.append(logical_destinations)
                DELAY_BOUND_OF_A_NET.append(delay_bound)
                DELAY_OCCURRED_OF_A_NET.append( delay_occurred)

        # 再处理B网数据
        for key in list(VL_DICT_OF_B_NET.keys()):
            NET_TYPE = "B"
            for VL_index in range(len( VL_DICT_OF_B_NET[key])):
                arinc664_physical_destinations, physical_destination, logical_destinations = [], [], []
                SOURCE_OF_B_NET.append(arinc664_physical_ports_index_for_B_net[key])
                MTU_OF_B_NET.append(VL_DICT_OF_B_NET[key][VL_index][1])
                BAG_OF_B_NET.append(VL_DICT_OF_B_NET[ key ][ VL_index ][ 0 ] )
                delay_bound, delay_occurred = [], []
                for subVL_index in range( len( VL_DICT_OF_B_NET[ key ][ VL_index ][ 5 ] ) ):
                    for physical_port_name_index in range( len( VL_DICT_OF_B_NET[ key ][ VL_index ][ 5 ][ subVL_index ] ) ):
                        physical_port_name = VL_DICT_OF_B_NET[ key ][ VL_index ][ 5 ][ subVL_index ][ physical_port_name_index ]
                        logical_port_name = VL_DICT_OF_B_NET[ key ][ VL_index ][ 4 ][ subVL_index ][ physical_port_name_index ]
                        if physical_ports_information[ physical_port_name ][ 0 ] in [ "AswPhysPort", "AesPhysPort" ]:
                            arinc664_physical_destinations.append( arinc664_physical_ports_index_for_B_net[ physical_port_name ] ) # 该物理端口在A网中的index
                            physical_destination.append( physical_port_name )
                            logical_destinations.append( logical_port_name )
                            delay_bound.append(VL_DICT_OF_B_NET[key][VL_index][6][subVL_index][physical_port_name_index])
                            delay_occurred.append(VL_DICT_OF_B_NET[key][VL_index][7][subVL_index][physical_port_name_index])
                        else:
                            arinc664_destination = self.find_previous_physical_port( NET_TYPE, physical_port_name, physical_ports_information, physical_ports_adjacent_matrix, physical_ports_index, physical_ports_index_reversed )
                            arinc664_physical_destinations.append( arinc664_physical_ports_index_for_B_net[ arinc664_destination ] )
                            physical_destination.append( physical_port_name )
                            logical_destinations.append( logical_port_name )
                            delay_bound.append(VL_DICT_OF_B_NET[key][VL_index][6][subVL_index][physical_port_name_index])
                            delay_occurred.append(VL_DICT_OF_B_NET[key][VL_index][7][subVL_index][physical_port_name_index])
                ARINC664_DESTINATIONS_OF_B_NET.append( arinc664_physical_destinations )
                DESTINATIONS_OF_B_NET.append( physical_destination )
                LOGICAL_DESTINATIONS_OF_B_NET.append( logical_destinations )
                DELAY_BOUND_OF_B_NET.append( delay_bound )
                DELAY_OCCURRED_OF_B_NET.append( delay_occurred )

        return SOURCE_OF_A_NET,\
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
               DELAY_OCCURRED_OF_B_NET

    def main( self ):
        VL_DICT_OF_A_NET, \
        VL_DICT_OF_B_NET, \
        messages_per_physical_port, \
        physical_ports_information, \
        messages_info, \
        physical_ports_adjacent_matrix, \
        physical_ports_index, \
        physical_ports_index_reversed, \
        arinc664_physical_ports_connections_for_A_net, \
        arinc664_physical_ports_index_for_A_net, \
        arinc664_physical_ports_index_reversed_for_A_net, \
        arinc664_physical_ports_connections_for_B_net, \
        arinc664_physical_ports_index_for_B_net, \
        arinc664_physical_ports_index_reversed_for_B_net = self.load_data()

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
        DELAY_OCCURRED_OF_B_NET = self.process_data(
                                                    VL_DICT_OF_A_NET,
                                                    VL_DICT_OF_B_NET,
                                                    physical_ports_information,
                                                    arinc664_physical_ports_index_for_A_net,
                                                    arinc664_physical_ports_index_for_B_net,
                                                    physical_ports_adjacent_matrix,
                                                    physical_ports_index,
                                                    physical_ports_index_reversed
                                                    )

        return VL_DICT_OF_A_NET, \
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
               physical_ports_index_reversed