import Supplementary_Routing_Optimization

class GET_THE_TRANSMITTING_PATH_OF_MESSAGES_OF_ROUTES_PATH_PROCESSING():
    def __init__( self, physical_ports_information, messages_info, physical_ports_adjacent_matrix, physical_ports_index, physical_ports_index_reversed, BANDWIDTH_OF_NODES, GAP, TIMELIMITED ):
        self.physical_ports_information = physical_ports_information
        self.messages_info = messages_info
        self.PHYSICAL_PORTS_ADJACENT_MATRIX = physical_ports_adjacent_matrix # 加载全网所有物理端口的邻接矩阵
        self.PHYSICAL_PORTS_INDEX = physical_ports_index
        self.PHYSICAL_PORTS_INDEX_REVERSED = physical_ports_index_reversed
        self.BANDWIDTH_OF_NODES = BANDWIDTH_OF_NODES
        self.GAP = GAP
        self.TIMELIMITED = TIMELIMITED

    def find_following_physical_port( self, non_a664_physical_port_name ):
        for index in range( len( self.PHYSICAL_PORTS_ADJACENT_MATRIX ) ):
            if self.PHYSICAL_PORTS_ADJACENT_MATRIX[ self.PHYSICAL_PORTS_INDEX[ non_a664_physical_port_name ] ][ index ] == 1:  # 说明此非664消息经物理端口physical_port_name向RDIU中下标为index的物理端口传输数据
                if self.physical_ports_information[ self.PHYSICAL_PORTS_INDEX_REVERSED[ index ] ][ 6 ][ 0:4 ] == "RDIU":  # 下标为index的物理端口所在物理设备为RDIU
                    return self.PHYSICAL_PORTS_INDEX_REVERSED[ index ]

    def find_previous_physical_port( self, non_a664_physical_port_name ):
        for index in range( len( self.PHYSICAL_PORTS_ADJACENT_MATRIX ) ):
            if self.PHYSICAL_PORTS_ADJACENT_MATRIX[ index ][ self.PHYSICAL_PORTS_INDEX[ non_a664_physical_port_name ] ] == 1:  # 说明此非664消息经物理端口physical_port_name向RDIU中下标为index的物理端口传输数据
                if self.physical_ports_information[ self.PHYSICAL_PORTS_INDEX_REVERSED[ index ] ][ 6 ][ 0:4 ] == "RDIU":  # 下标为index的物理端口所在物理设备为RDIU
                    return self.PHYSICAL_PORTS_INDEX_REVERSED[ index ]

    def get_the_transmitting_path_of_messages_in_ARINC664(self,
                                                          NET_TYPE,
                                                          ADJACENT_MATRIX,
                                                          PHYSICAL_PORTS_INDEX,
                                                          PHYSICAL_PORTS_INDEX_REVERSED,
                                                          SOURCE,
                                                          ARINC664_DESTINATIONS_NO_REPETITION,
                                                          MTU,
                                                          BAG,
                                                          DELAY_BOUND_LEFT,
                                                          TOTAL_Y_FOR_RETURN,
                                                          VL_DICT
                                                          ):
        NUMBER_OF_NODES = len(ADJACENT_MATRIX)
        MESSAGES_DICT = {}
        for VL_index in range(len(SOURCE)):
            source = SOURCE[VL_index]
            PATH_DICT = {} # 键：目的地；值：从源节点到此目的地的路径
            for destination_of_no_repetition_index in range(len(ARINC664_DESTINATIONS_NO_REPETITION[VL_index])):
                destination_of_no_repetition = ARINC664_DESTINATIONS_NO_REPETITION[VL_index][destination_of_no_repetition_index]
                following_node = destination_of_no_repetition
                path_reversed = [following_node]  # 该列表为倒序记录从目的地到源节点的路径
                OUTER_INDICATOR = 0 # 标志尚未回说到源节点
                while not OUTER_INDICATOR:
                    INNER_INDICATOR = 0
                    for previous_node in range(NUMBER_OF_NODES):
                        if TOTAL_Y_FOR_RETURN[VL_index][previous_node][following_node] == 1:
                            INNER_INDICATOR = 1
                            if previous_node == source:
                                OUTER_INDICATOR = 1
                            else:
                                following_node = previous_node
                            path_reversed.append(previous_node)
                    if not INNER_INDICATOR:
                        break
                if OUTER_INDICATOR == 1: # 存在针对此虚拟链路的关于SOURCE[ VL_index ]以及destination_of_no_repetition的路由
                    path = list(reversed( path_reversed))
                    PATH_DICT[destination_of_no_repetition] = path
                else: # 不存在针对此虚拟链路的关于SOURCE[ VL_index ]以及destination_of_no_repetition的路由
                    print("Need to find a new route for source:%d and destination:%d once more!" % (source, destination_of_no_repetition))
                    #因此，需要针对SOURCE[ VL_index ]以及destination_of_no_repetition，额外寻找其传输路由
                    supplementary_routing_optimiza = Supplementary_Routing_Optimization.supplementary_routing_optimize(self.physical_ports_information, self.BANDWIDTH_OF_NODES)
                    Y_FOR_RETURN, BANDWIDTH_COST_FOR_RETURN, delay_of_destination, self.BANDWIDTH_OF_NODES = supplementary_routing_optimiza.routing_optimize(ADJACENT_MATRIX,
                                                                                                                                                             source,
                                                                                                                                                             destination_of_no_repetition,
                                                                                                                                                             MTU[ VL_index ],
                                                                                                                                                             BAG[ VL_index ],
                                                                                                                                                             DELAY_BOUND_LEFT[ VL_index ][ destination_of_no_repetition_index ],
                                                                                                                                                             self.GAP,
                                                                                                                                                             self.TIMELIMITED
                                                                                                                                                             )
                    following_node = destination_of_no_repetition
                    path_reversed = [following_node]  # 该列表为倒序记录从目的地到源节点的路径
                    OUTER_INDICATOR = 0  # 标志尚未回说到源节点
                    while not OUTER_INDICATOR:
                        INNER_INDICATOR = 0
                        for previous_node in range(NUMBER_OF_NODES):
                            if Y_FOR_RETURN[previous_node][following_node] == 1:
                                INNER_INDICATOR = 1
                                if previous_node == source:
                                    OUTER_INDICATOR = 1
                                else:
                                    following_node = previous_node
                                path_reversed.append(previous_node)
                        if not INNER_INDICATOR:
                            break
                    if OUTER_INDICATOR == 1:  # 存在针对此虚拟链路的关于SOURCE[ VL_index ]以及destination_of_no_repetition的路由
                        print("Find the routes between source:%d and destination:%d!" % (source, destination_of_no_repetition))
                        path = list(reversed(path_reversed))
                        PATH_DICT[destination_of_no_repetition] = path


            # 遍历此虚拟链路中的消息，根据消息的目的节点，为其指定路由
            COUNTING_OF_VL = 0
            INDICATOR = 1
            for device in list(VL_DICT.keys()):
                for vl_index in range(len(VL_DICT[ device ])):
                    if COUNTING_OF_VL == VL_index and INDICATOR == 1:
                        DEVICE = device
                        index_of_vl = vl_index
                        INDICATOR = 0
                        break
                    else:
                        COUNTING_OF_VL += 1
                if INDICATOR == 0:
                    break

            INFORMATION_OF_VL = VL_DICT[DEVICE][index_of_vl]
            print("Length of SOURCE:", len( SOURCE ), "VL_index:", VL_index, "COUNTING_OF_VL:", COUNTING_OF_VL, "INFORMATION_OF_VL:", INFORMATION_OF_VL)
            for subVL_index in range(len(INFORMATION_OF_VL[3])):
                for message_index in range(len(INFORMATION_OF_VL[3][subVL_index])):
                    message_guid = INFORMATION_OF_VL[3][ subVL_index ][ message_index ]
                    FULL_PATH = [message_guid] # 因为一条消息可以被同时转发至多个不同的目的节点，因此，以列表的形式进行记录
                    # 每一条消息会被同时转发至多个逻辑端口，且每个逻辑端口的消息可能会经A、B两网转发
                    for logical_port_index in range(len(self.messages_info[message_guid][9])):
                        """
                        因为在消息聚合为虚链路的过程中，我们没有对以下消息进行区分：
                        1, 消息的类型为非ARINC664，且发送设备与接收设备相同：即不需要转发至RDIU；
                        2, 消息的类型为非ARINC664，且发送设备与接收设备不同，但接收设备为转发至的RDIU设备，即：消息合并、转换为虚链路后，不需要转发出RDIU；
                        3, 消息的类型为非ARINC664，且发送设备与接收设备不同，且接收设备也不是转发至的RDIU设备，即：消息合并、转换为虚链路后，需要转发出RDIU；
                        4, 消息的类型为ARINC664，且发送端设备和接收端设备相同；
                        5, 消息的类型为ARINC664，且发送端设备和接收端设备不相同。
                        """
                        if self.messages_info[message_guid][0] != "A664": # 消息的类型为非ARINC664
                            if self.messages_info[message_guid][3] == self.messages_info[message_guid][9][logical_port_index ][3]: # 消息的类型为非ARINC664，且发送设备与接收设备相同：即不需要转发至RDIU
                                # 经过验证，当消息的发送端设备和接收端设备相同时，消息的发送类型和接受类型也一定相同
                                path_not_including_logical_port = [] # 没有转发路径，因为不需要转发出此物理设备
                                path_including_logical_port = [self.messages_info[message_guid][4], path_not_including_logical_port, self.messages_info[message_guid][9][logical_port_index][6]]
                            else:
                                # 消息的类型为非ARINC664，且发送设备与接收设备不相同
                                # 首先找出该消息需要传输至的RDIU设备
                                non_a664_physical_port_name = self.messages_info[message_guid][4][0] # 物理端口是一列表，且因为消息的类型为非ARINC664，该物理端口列表的长度必定为1
                                following_nona664_physical_port_name = self.find_following_physical_port(non_a664_physical_port_name) # 与non_a664_physical_port_name相连的属于RDIU的物理端口
                                following_RDIU_name = self.physical_ports_information[following_nona664_physical_port_name][6]
                                # 如果消息的一个目的地就是此RDIU设备，那么其不需要经过合并、转换等操作
                                if self.messages_info[message_guid][9][logical_port_index][3] == following_RDIU_name:
                                    print("存在非ARINC664消息转发至RDIU，且消息的发送类型为：", self.messages_info[message_guid][0], "消息的接收类型为：", self.messages_info[message_guid][9][logical_port_index][0])
                                    path_not_including_logical_port = [non_a664_physical_port_name, following_nona664_physical_port_name]  # 没有转发路径，因为不需要转发出此物理设备
                                    path_including_logical_port = [self.messages_info[message_guid][4], path_not_including_logical_port, self.messages_info[message_guid][9][logical_port_index][6]]
                                else: # 消息的目的地不是此RDIU设备，那么其需要经过合并、转换等操作
                                    # 首先判断目的地节点是否为ARINC664端口
                                    for destination_physical_port_index in range(len(self.messages_info[message_guid][9][logical_port_index][4])):
                                        destination_physical_port_name = self.messages_info[message_guid][9][logical_port_index][4][destination_physical_port_index]
                                        if self.physical_ports_information[destination_physical_port_name][0] not in ["AswPhysPort", "AesPhysPort"]: # 目的节点物理端口为非ARINC664
                                            if NET_TYPE == "B":
                                                continue
                                            if NET_TYPE == "A":
                                                # 找到与此非ARINC664目的节点物理端口相连的属于RDIU设备的非ARINC664物理端口
                                                previous_nona664_physical_port_name = self.find_previous_physical_port(destination_physical_port_name)
                                                previous_RDIU_name = self.physical_ports_information[previous_nona664_physical_port_name][6]
                                                a664_physical_port_name = previous_RDIU_name + ".A"
                                                # 存在一类消息，转发路径如下：source设备（非ARINC664物理端口）->RDIU->destination设备
                                                if PHYSICAL_PORTS_INDEX[a664_physical_port_name] == SOURCE[VL_index]: # 即：消息的转发路径为source设备（非ARINC664物理端口）->RDIU->destination设备
                                                    path_not_including_logical_port = [non_a664_physical_port_name, following_nona664_physical_port_name, previous_nona664_physical_port_name, destination_physical_port_name]
                                                    path_including_logical_port = [self.messages_info[message_guid][4], path_not_including_logical_port, self.messages_info[message_guid][9][logical_port_index][6]]
                                                else:
                                                    try:
                                                        index_path = PATH_DICT[PHYSICAL_PORTS_INDEX[a664_physical_port_name]]
                                                    except KeyError:
                                                        print("PATH_DICT keys:", list(PATH_DICT.keys()), PHYSICAL_PORTS_INDEX[a664_physical_port_name])
                                                        print("destination_physical_port_name:", destination_physical_port_name, "previous_nona664_physical_port_name:", previous_nona664_physical_port_name, "previous_RDIU_name:", previous_RDIU_name)
                                                    path_not_including_logical_port = [non_a664_physical_port_name, following_nona664_physical_port_name]
                                                    for a664port_index in index_path:
                                                        path_not_including_logical_port.append(PHYSICAL_PORTS_INDEX_REVERSED[a664port_index])
                                                    path_not_including_logical_port.append(previous_nona664_physical_port_name)
                                                    path_not_including_logical_port.append(destination_physical_port_name )
                                                    path_including_logical_port = [self.messages_info[message_guid][4], path_not_including_logical_port, self.messages_info[message_guid][9][logical_port_index][6]]
                                        else: # 目的节点物理端口为ARINC664
                                            # 首先判断端口所属的网络与NET_TYPE是否一致
                                            if destination_physical_port_name[-2:] == "." + NET_TYPE:
                                                index_path = PATH_DICT[PHYSICAL_PORTS_INDEX[ destination_physical_port_name]]
                                                path_not_including_logical_port = [non_a664_physical_port_name, following_nona664_physical_port_name]
                                                for a664port_index in index_path:
                                                    path_not_including_logical_port.append(PHYSICAL_PORTS_INDEX_REVERSED[a664port_index])
                                                path_including_logical_port = [self.messages_info[ message_guid][4], path_not_including_logical_port, self.messages_info[message_guid][9][logical_port_index][6]]
                                            else:
                                                continue
                        else: #消息的类型为ARINC664
                            if self.messages_info[message_guid][3] == self.messages_info[message_guid][9][logical_port_index][3]:  # 消息的类型为ARINC664，且发送设备与接收设备相同：即不需要转发至RDIU
                                # 经过验证，当消息的发送端设备和接收端设备相同时，消息的发送类型和接受类型也一定相同
                                path_not_including_logical_port = [] # 没有转发路径，因为不需要转发出此物理设备
                                path_including_logical_port = [self.messages_info[ message_guid][4], path_not_including_logical_port, self.messages_info[message_guid][9][logical_port_index][6]]
                            else:
                                # 消息的类型为ARINC664，且发送设备与接收设备不相同
                                # 因为消息的发送类型为ARINC664，因此消息的接收端类型也必为ARINC664
                                for destination_physical_port_index in range(len(self.messages_info[message_guid][9][logical_port_index][4])):
                                    destination_physical_port_name = self.messages_info[message_guid][9][logical_port_index][4][destination_physical_port_index]
                                    # 首先判断端口所属的网络与NET_TYPE是否一致
                                    if destination_physical_port_name[-2:] == "." + NET_TYPE:
                                        index_path = PATH_DICT[PHYSICAL_PORTS_INDEX[destination_physical_port_name]]
                                        path_not_including_logical_port = []
                                        for a664port_index in index_path:
                                            path_not_including_logical_port.append(PHYSICAL_PORTS_INDEX_REVERSED[a664port_index])
                                        path_including_logical_port = [self.messages_info[message_guid][4], path_not_including_logical_port, self.messages_info[message_guid][9][logical_port_index][6]]
                        #print( "path_including_logical_port:", path_including_logical_port )
                    FULL_PATH.append(path_including_logical_port)
                    MESSAGES_DICT[message_guid] = FULL_PATH
        return MESSAGES_DICT

    def get_the_transmitting_path_of_messages_in_AFDX(self,
                                                      NET_TYPE,
                                                      ADJACENT_MATRIX,
                                                      PHYSICAL_PORTS_INDEX,
                                                      PHYSICAL_PORTS_INDEX_REVERSED,
                                                      SOURCE,
                                                      ARINC664_DESTINATIONS_NO_REPETITION,
                                                      MTU,
                                                      BAG,
                                                      DELAY_BOUND_LEFT,
                                                      TOTAL_Y_FOR_RETURN,
                                                      VL_DICT
                                                      ):
        NUMBER_OF_NODES = len(ADJACENT_MATRIX)
        MESSAGES_DICT = {}
        for VL_index in range(len(SOURCE)):
            source = SOURCE[VL_index]
            PATH_DICT = {} # 键：目的地；值：从源节点到此目的地的路径
            for destination_of_no_repetition_index in range(len(ARINC664_DESTINATIONS_NO_REPETITION[VL_index])):
                destination_of_no_repetition = ARINC664_DESTINATIONS_NO_REPETITION[VL_index][destination_of_no_repetition_index]
                following_node = destination_of_no_repetition
                path_reversed = [following_node]  # 该列表为倒序记录从目的地到源节点的路径
                OUTER_INDICATOR = 0 # 标志尚未回说到源节点
                while not OUTER_INDICATOR:
                    INNER_INDICATOR = 0
                    for previous_node in range(NUMBER_OF_NODES):
                        if TOTAL_Y_FOR_RETURN[VL_index][previous_node][following_node] == 1:
                            INNER_INDICATOR = 1
                            if previous_node == source:
                                OUTER_INDICATOR = 1
                            else:
                                following_node = previous_node
                            path_reversed.append(previous_node)
                    if not INNER_INDICATOR:
                        break
                if OUTER_INDICATOR == 1: # 存在针对此虚拟链路的关于SOURCE[ VL_index ]以及destination_of_no_repetition的路由
                    path = list( reversed(path_reversed))
                    PATH_DICT[destination_of_no_repetition] = path
                else: # 不存在针对此虚拟链路的关于SOURCE[ VL_index ]以及destination_of_no_repetition的路由
                    print( "Need to find a new route for source:%d and destination:%d once more!" % (source, destination_of_no_repetition))
                    #因此，需要针对SOURCE[ VL_index ]以及destination_of_no_repetition，额外寻找其传输路由
                    supplementary_routing_optimiza = Supplementary_Routing_Optimization.supplementary_routing_optimize(self.physical_ports_information, self.BANDWIDTH_OF_NODES)
                    Y_FOR_RETURN, BANDWIDTH_COST_FOR_RETURN, delay_of_destination, self.BANDWIDTH_OF_NODES = supplementary_routing_optimiza.routing_optimize(ADJACENT_MATRIX,
                                                                                                                                                             source,
                                                                                                                                                             destination_of_no_repetition,
                                                                                                                                                             MTU[ VL_index ],
                                                                                                                                                             BAG[ VL_index ],
                                                                                                                                                             DELAY_BOUND_LEFT[ VL_index ][ destination_of_no_repetition_index ],
                                                                                                                                                             self.GAP,
                                                                                                                                                             self.TIMELIMITED
                                                                                                                                                             )
                    following_node = destination_of_no_repetition
                    path_reversed = [following_node]  # 该列表为倒序记录从目的地到源节点的路径
                    OUTER_INDICATOR = 0  # 标志尚未回说到源节点
                    while not OUTER_INDICATOR:
                        INNER_INDICATOR = 0
                        for previous_node in range(NUMBER_OF_NODES):
                            if Y_FOR_RETURN[previous_node][following_node] == 1:
                                INNER_INDICATOR = 1
                                if previous_node == source:
                                    OUTER_INDICATOR = 1
                                else:
                                    following_node = previous_node
                                path_reversed.append(previous_node)
                        if not INNER_INDICATOR:
                            break
                    if OUTER_INDICATOR == 1:  # 存在针对此虚拟链路的关于SOURCE[ VL_index ]以及destination_of_no_repetition的路由
                        print("Find the routes between source:%d and destination:%d!" % (source, destination_of_no_repetition))
                        path = list(reversed(path_reversed))
                        PATH_DICT[destination_of_no_repetition] = path


            # 遍历此虚拟链路中的消息，根据消息的目的节点，为其指定路由
            COUNTING_OF_VL = 0
            INDICATOR = 1
            for device in list(VL_DICT.keys()):
                for vl_index in range(len(VL_DICT[ device])):
                    if COUNTING_OF_VL == VL_index and INDICATOR == 1:
                        DEVICE = device
                        index_of_vl = vl_index
                        INDICATOR = 0
                        break
                    else:
                        COUNTING_OF_VL += 1
                if INDICATOR == 0:
                    break

            INFORMATION_OF_VL = VL_DICT[DEVICE][index_of_vl]
            print("Length of SOURCE:", len( SOURCE ), "VL_index:", VL_index, "COUNTING_OF_VL:", COUNTING_OF_VL, "INFORMATION_OF_VL:", INFORMATION_OF_VL)
            for subVL_index in range(len(INFORMATION_OF_VL[ 3 ])):
                for message_index in range(len(INFORMATION_OF_VL[3][subVL_index])):
                    message_guid = INFORMATION_OF_VL[3][subVL_index][message_index]
                    FULL_PATH = [message_guid] # 因为一条消息可以被同时转发至多个不同的目的节点，因此，以列表的形式进行记录
                    # 每一条消息会被同时转发至多个逻辑端口，且每个逻辑端口的消息可能会经A、B两网转发
                    for logical_port_index in range(len(self.messages_info[message_guid][9])):
                        """
                        因为在消息聚合为虚链路的过程中，我们没有对以下消息进行区分：
                        1, 消息的类型为非ARINC664，且发送设备与接收设备相同：即不需要转发至RDIU；
                        2, 消息的类型为非ARINC664，且发送设备与接收设备不同，但接收设备为转发至的RDIU设备，即：消息合并、转换为虚链路后，不需要转发出RDIU；
                        3, 消息的类型为非ARINC664，且发送设备与接收设备不同，且接收设备也不是转发至的RDIU设备，即：消息合并、转换为虚链路后，需要转发出RDIU；
                        4, 消息的类型为ARINC664，且发送端设备和接收端设备相同；
                        5, 消息的类型为ARINC664，且发送端设备和接收端设备不相同。
                        """
                        if self.messages_info[message_guid][0] != "A664": # 消息的类型为非ARINC664
                            if self.messages_info[message_guid][3] == self.messages_info[message_guid][9][logical_port_index][3]: # 消息的类型为非ARINC664，且发送设备与接收设备相同：即不需要转发至RDIU
                                # 经过验证，当消息的发送端设备和接收端设备相同时，消息的发送类型和接受类型也一定相同
                                path_not_including_logical_port = [] # 没有转发路径，因为不需要转发出此物理设备
                                path_including_logical_port = [self.messages_info[message_guid][4], path_not_including_logical_port, self.messages_info[message_guid][9][logical_port_index][6]]
                            else:
                                # 消息的类型为非ARINC664，且发送设备与接收设备不相同
                                # 首先找出该消息需要传输至的RDIU设备
                                non_a664_physical_port_name = self.messages_info[message_guid][4][0] # 物理端口是一列表，且因为消息的类型为非ARINC664，该物理端口列表的长度必定为1
                                following_nona664_physical_port_name = self.find_following_physical_port(non_a664_physical_port_name) # 与non_a664_physical_port_name相连的属于RDIU的物理端口
                                following_RDIU_name = self.physical_ports_information[following_nona664_physical_port_name][6]
                                # 如果消息的一个目的地就是此RDIU设备，那么其不需要经过合并、转换等操作
                                if self.messages_info[message_guid][9][logical_port_index][3] == following_RDIU_name:
                                    print("存在非ARINC664消息转发至RDIU，且消息的发送类型为：", self.messages_info[ message_guid][0], "消息的接收类型为：", self.messages_info[message_guid][9][logical_port_index][0])
                                    path_not_including_logical_port = [non_a664_physical_port_name, following_nona664_physical_port_name ]  # 没有转发路径，因为不需要转发出此物理设备
                                    path_including_logical_port = [self.messages_info[message_guid][4], path_not_including_logical_port, self.messages_info[message_guid][9][logical_port_index][6]]
                                else: # 消息的目的地不是此RDIU设备，那么其需要经过合并、转换等操作
                                    # 首先判断目的地节点是否为ARINC664端口
                                    for destination_physical_port_index in range(len(self.messages_info[message_guid][9][logical_port_index][4])):
                                        destination_physical_port_name = self.messages_info[message_guid][9][logical_port_index][4][destination_physical_port_index]
                                        if self.physical_ports_information[destination_physical_port_name][0] not in ["AswPhysPort", "AesPhysPort"]: # 目的节点物理端口为非ARINC664
                                            if NET_TYPE == "B":
                                                continue
                                            if NET_TYPE == "A":
                                                # 找到与此非ARINC664目的节点物理端口相连的属于RDIU设备的非ARINC664物理端口
                                                previous_nona664_physical_port_name = self.find_previous_physical_port(destination_physical_port_name)
                                                previous_RDIU_name = self.physical_ports_information[previous_nona664_physical_port_name][6]
                                                a664_physical_port_name = previous_RDIU_name + ".A"
                                                # 存在一类消息，转发路径如下：source设备（非ARINC664物理端口）->RDIU->destination设备
                                                if PHYSICAL_PORTS_INDEX[a664_physical_port_name] == SOURCE[VL_index]: # 即：消息的转发路径为source设备（非ARINC664物理端口）->RDIU->destination设备
                                                    path_not_including_logical_port = [non_a664_physical_port_name, following_nona664_physical_port_name, previous_nona664_physical_port_name, destination_physical_port_name]
                                                    path_including_logical_port = [self.messages_info[message_guid][4], path_not_including_logical_port, self.messages_info[message_guid][9][logical_port_index][6]]
                                                else:
                                                    try:
                                                        index_path = PATH_DICT[PHYSICAL_PORTS_INDEX[a664_physical_port_name]]
                                                    except KeyError:
                                                        print("PATH_DICT keys:", list(PATH_DICT.keys()), PHYSICAL_PORTS_INDEX[a664_physical_port_name])
                                                        print("destination_physical_port_name:", destination_physical_port_name, "previous_nona664_physical_port_name:", previous_nona664_physical_port_name, "previous_RDIU_name:", previous_RDIU_name)
                                                    path_not_including_logical_port = [non_a664_physical_port_name, following_nona664_physical_port_name]
                                                    for a664port_index in index_path:
                                                        path_not_including_logical_port.append(PHYSICAL_PORTS_INDEX_REVERSED[a664port_index])
                                                    path_not_including_logical_port.append(previous_nona664_physical_port_name)
                                                    path_not_including_logical_port.append(destination_physical_port_name)
                                                    path_including_logical_port = [self.messages_info[message_guid][4], path_not_including_logical_port, self.messages_info[message_guid][9][logical_port_index][6]]
                                        else: # 目的节点物理端口为ARINC664
                                            # 首先判断端口所属的网络与NET_TYPE是否一致
                                            if destination_physical_port_name[-2:] == "." + NET_TYPE:
                                                index_path = PATH_DICT[ PHYSICAL_PORTS_INDEX[destination_physical_port_name]]
                                                path_not_including_logical_port = [non_a664_physical_port_name, following_nona664_physical_port_name]
                                                for a664port_index in index_path:
                                                    path_not_including_logical_port.append(PHYSICAL_PORTS_INDEX_REVERSED[a664port_index])
                                                path_including_logical_port = [self.messages_info[ message_guid][4], path_not_including_logical_port, self.messages_info[message_guid][9][logical_port_index][6]]
                                            else:
                                                continue
                        else: #消息的类型为ARINC664
                            if self.messages_info[message_guid][3] == self.messages_info[message_guid][9][logical_port_index][3]:  # 消息的类型为ARINC664，且发送设备与接收设备相同：即不需要转发至RDIU
                                # 经过验证，当消息的发送端设备和接收端设备相同时，消息的发送类型和接受类型也一定相同
                                path_not_including_logical_port = [] # 没有转发路径，因为不需要转发出此物理设备
                                path_including_logical_port = [self.messages_info[message_guid][4], path_not_including_logical_port, self.messages_info[message_guid][9][logical_port_index][6]]
                            else:
                                # 消息的类型为ARINC664，且发送设备与接收设备不相同
                                # 因为消息的发送类型为ARINC664，因此消息的接收端类型也必为ARINC664
                                for destination_physical_port_index in range(len(self.messages_info[message_guid][9][logical_port_index][4])):
                                    destination_physical_port_name = self.messages_info[message_guid][9][logical_port_index][4][destination_physical_port_index]
                                    # 首先判断端口所属的网络与NET_TYPE是否一致
                                    if destination_physical_port_name[-2:] == "." + NET_TYPE:
                                        index_path = PATH_DICT[PHYSICAL_PORTS_INDEX[destination_physical_port_name]]
                                        path_not_including_logical_port = []
                                        for a664port_index in index_path:
                                            path_not_including_logical_port.append(PHYSICAL_PORTS_INDEX_REVERSED[a664port_index])
                                        path_including_logical_port = [self.messages_info[message_guid][4], path_not_including_logical_port, self.messages_info[message_guid][9][logical_port_index][6]]
                        #print( "path_including_logical_port:", path_including_logical_port )
                    FULL_PATH.append(path_including_logical_port)
                    MESSAGES_DICT[message_guid] = FULL_PATH
        return MESSAGES_DICT