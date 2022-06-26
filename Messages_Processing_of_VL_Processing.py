import Data_Transmitting_of_VL_Processing

class MESSAGES_PROCESSING_OF_VL_PROCESSING():
    def messages_preprocessing_of_vl_of_arinc664(
                                                 self,
                                                 messages_of_physical_port,
                                                 physical_ports_information,
                                                 VL_DICT_OF_A_NET_OF_ARINC664,
                                                 VL_DICT_OF_B_NET_OF_ARINC664,
                                                 GAP,
                                                 TIMELIMITED,
                                                 EXPANDED_COEFFICIENT,
                                                 UPPER_LIMIT_OF_THE_NUMBER_OF_MESSAGES,
                                                 AVERAGE_NUMBER_OF_MESSAGES,
                                                 ALLOCATED_RATE_COEFFICIENT # RDIU设备既有ARINC664消息，又有非ARINC664消息，因此，需要将带宽在非ARINC664以及ARINC664消息间进行分配。具体分配原则：非ARINC占 ORIGINAL_RATE * ALLOCATED_RATE_COEFFICIENT
                                                 ):
        print("Physical device:", messages_of_physical_port[0])
        if messages_of_physical_port[0] in ["RDIU_01", "RDIU_02", "RDIU_03", "RDIU_04", "RDIU_05", "RDIU_06", "RDIU_07", "RDIU_08",
                                            "RDIU_09", "RDIU_10", "RDIU_11", "RDIU_12", "RDIU_13", "RDIU_14", "RDIU_15", "RDIU_16"]:
            """
            因为ARINC664网络里不考虑非ARINC664消息的合并与转换
            因此，当消息的输出物理端口为：
            "RDIU_01", "RDIU_02", "RDIU_03", "RDIU_04", "RDIU_05", "RDIU_06", "RDIU_07", "RDIU_08", "RDIU_09", "RDIU_10", "RDIU_11", "RDIU_12", "RDIU_13", "RDIU_14", "RDIU_15", "RDIU_16"
            时，不予考虑
            """
            return [VL_DICT_OF_A_NET_OF_ARINC664, VL_DICT_OF_B_NET_OF_ARINC664]
        else:
            """
            首先判断目的物理端口的类型：ARINC664或非ARINC664
            若目的物理端口类型为ARINC664，则进一步判断是A网端口还是B网端口；
            1、若目的物理端口类型为ARINC664且为A网端口，或者目的物理端口为非ARINC664，则将消息划分进A网的虚链路中
            2、若目的物理端口类型为ARINC664且为B网端口，则将消息划分进B网的虚链路中
            """
            net_type = messages_of_physical_port[0][-1:]  # 该ARINC664端口属于A网还是B网
            locals()["A664_SIZE_OF_" + net_type + "_NET"] = []
            locals()["A664_DELAY_OF_" + net_type + "_NET"] = []
            locals()["A664_PERIOD_OF_" + net_type + "_NET" ] = []
            locals()["A664_DICT_OF_" + net_type + "_NET"] = dict()
            locals()["A664_INDEX_OF_" + net_type + "_NET"] = 0
            locals()["A664_MESSAGES_GUID_OF_" + net_type + "_NET"] = []
            locals()["A664_LOGICAL_DESTINATION_OF_" + net_type + "_NET"] = []
            locals()["A664_PHYSICAL_PORT_OF_" + net_type + "_NET"] = []
            locals()["A664_DELAY_BOUND_OF_" + net_type + "_NET"] = []
            locals()["A664_DELAY_OCCURRED_OF_" + net_type + "_NET"] = []
            for Non_ARINC664_messages_index in range(len(messages_of_physical_port[1])):
                message_type = messages_of_physical_port[1][Non_ARINC664_messages_index] # A664
                INDICATOR = 1
                if message_type != "A664":
                    print("There is an error in message type!")
                    break
                locals()["A664_logical_destination_of_" + net_type + "_NET"], locals()["A664_physical_destination_of_" + net_type + "_NET"] = [], []
                locals()["A664_delay_bound_of_" + net_type + "_NET"], locals()["A664_delay_occurred_of_" + net_type + "_NET"] = [], []
                for logical_port_index in range(len(messages_of_physical_port[6][Non_ARINC664_messages_index])): # len( messages_of_physical_port[6][Non_ARINC664_messages_index] )表示该消息被发送至逻辑端口的数目
                    for physical_port_index in range(len(messages_of_physical_port[7][Non_ARINC664_messages_index][logical_port_index])): # 发送至同一个逻辑端口的消息可能途径A、B网的两个物理端口
                        physical_port_name = messages_of_physical_port[7][Non_ARINC664_messages_index][logical_port_index][physical_port_index]
                        if physical_ports_information[ physical_port_name ][0] == "AswPhysPort" or physical_ports_information[ physical_port_name ][0] == "AesPhysPort": # 目的物理端口是ARINC664端口
                            if physical_port_name[-2:] == "." + net_type:
                                if INDICATOR == 1:
                                    locals()[message_type + "_SIZE_OF_" + net_type + "_NET"].append(messages_of_physical_port[2][Non_ARINC664_messages_index])
                                    locals()[message_type + "_DELAY_OF_" + net_type + "_NET"].append(messages_of_physical_port[3][Non_ARINC664_messages_index])
                                    locals()[message_type + "_PERIOD_OF_" + net_type + "_NET"].append(messages_of_physical_port[4][Non_ARINC664_messages_index])
                                    locals()[message_type + "_DICT_OF_" + net_type + "_NET"][locals()[message_type + "_INDEX_OF_" + net_type + "_NET"]] = Non_ARINC664_messages_index
                                    locals()[message_type + "_INDEX_OF_" + net_type + "_NET"] += 1
                                    locals()[message_type + "_MESSAGES_GUID_OF_" + net_type + "_NET"].append(messages_of_physical_port[5][Non_ARINC664_messages_index])
                                    INDICATOR = 0
                                locals()[message_type + "_logical_destination_of_" + net_type + "_NET"].append(messages_of_physical_port[6][Non_ARINC664_messages_index][logical_port_index])
                                locals()[message_type + "_physical_destination_of_" + net_type + "_NET"].append(messages_of_physical_port[7][Non_ARINC664_messages_index][logical_port_index][physical_port_index])
                                locals()[message_type + "_delay_bound_of_" + net_type + "_NET"].append(messages_of_physical_port[8][Non_ARINC664_messages_index][logical_port_index])
                                locals()[message_type + "_delay_occurred_of_" + net_type + "_NET"].append(messages_of_physical_port[9][Non_ARINC664_messages_index][logical_port_index])
                        else: # 目的物理端口是非ARINC664端口
                            if INDICATOR == 1:
                                locals()[message_type + "_SIZE_OF_" + net_type + "_NET"].append(messages_of_physical_port[2][Non_ARINC664_messages_index])
                                locals()[message_type + "_DELAY_OF_" + net_type + "_NET"].append(messages_of_physical_port[3][Non_ARINC664_messages_index])
                                locals()[message_type + "_PERIOD_OF_" + net_type + "_NET"].append(messages_of_physical_port[4][Non_ARINC664_messages_index])
                                locals()[message_type + "_DICT_OF_" + net_type + "_NET"][locals()[message_type + "_INDEX_OF_" + net_type + "_NET"]] = Non_ARINC664_messages_index
                                locals()[message_type + "_INDEX_OF_" + net_type + "_NET"] += 1
                                locals()[message_type + "_MESSAGES_GUID_OF_" + net_type + "_NET"].append(messages_of_physical_port[5][Non_ARINC664_messages_index])
                                INDICATOR = 0
                            locals()[message_type + "_logical_destination_of_" + net_type + "_NET"].append(messages_of_physical_port[6][Non_ARINC664_messages_index][ logical_port_index])
                            locals()[message_type + "_physical_destination_of_" + net_type + "_NET"].append(messages_of_physical_port[7][Non_ARINC664_messages_index][ logical_port_index][physical_port_index])
                            locals()[message_type + "_delay_bound_of_" + net_type + "_NET"].append(messages_of_physical_port[8][Non_ARINC664_messages_index][logical_port_index])
                            locals()[message_type + "_delay_occurred_of_" + net_type + "_NET"].append(messages_of_physical_port[9][Non_ARINC664_messages_index][logical_port_index])
                if locals()[message_type + "_logical_destination_of_" + net_type + "_NET"] != []:
                    locals()[message_type + "_LOGICAL_DESTINATION_OF_" + net_type + "_NET"].append(locals()[message_type + "_logical_destination_of_" + net_type + "_NET"])
                    locals()[message_type + "_PHYSICAL_PORT_OF_" + net_type + "_NET"].append(locals()[message_type + "_physical_destination_of_" + net_type + "_NET"])
                    locals()[message_type + "_DELAY_BOUND_OF_" + net_type + "_NET"].append(locals()[message_type + "_delay_bound_of_" + net_type + "_NET"])
                    locals()[message_type + "_DELAY_OCCURRED_OF_" + net_type + "_NET"].append(locals()[message_type + "_delay_occurred_of_" + net_type + "_NET"])

            # 考虑到从同一物理端口转发的不同消息，可能具有相同的目的地。
            # 因此，先统一下不同目的地的数目，然后将相同目的地的消息放在一起进行合并与转发
            locals()["A664_DIFFERENT_PHYSICAL_PORT_OF_" + net_type + "_NET"] = []
            for logical_destination in locals()["A664_PHYSICAL_PORT_OF_" + net_type + "_NET"]:
                indicator = 0  # 标志destination是否已经存在于DIFFERENT_DESTINATIONS中
                for different_logical_destination in locals()["A664_DIFFERENT_PHYSICAL_PORT_OF_" + net_type + "_NET"]:
                    if set(logical_destination) == set(different_logical_destination):
                        indicator = 1
                if indicator == 0:
                    locals()["A664_DIFFERENT_PHYSICAL_PORT_OF_" + net_type + "_NET"].append(logical_destination)

            # 统计消息分组的类别数
                locals()["NUMBER_OF_DIFFERENT_SET_OF_MESSAGES_OF_" + net_type + "_NET"] = len( locals()["A664_DIFFERENT_PHYSICAL_PORT_OF_" + net_type + "_NET"])

            RATE_OF_PHYSICAL_PORT = physical_ports_information[messages_of_physical_port[0]][7] * 1000 # 物理端口原始的速率（带宽）
            if messages_of_physical_port[0][0:7] in ["RDIU_01", "RDIU_02", "RDIU_03", "RDIU_04", "RDIU_05", "RDIU_06", "RDIU_07", "RDIU_08",
                                                     "RDIU_09", "RDIU_10", "RDIU_11", "RDIU_12", "RDIU_13", "RDIU_14", "RDIU_15", "RDIU_16"]:
                ALLOCATED_RATE_OF_PHYSICAL_PORT = RATE_OF_PHYSICAL_PORT * (1-ALLOCATED_RATE_COEFFICIENT)
            else:
                ALLOCATED_RATE_OF_PHYSICAL_PORT = RATE_OF_PHYSICAL_PORT
            PHYSICAL_PORT_RATE = ALLOCATED_RATE_OF_PHYSICAL_PORT

            locals()["MESSAGES_NUMBER_OF_A664_DIFFERENT_PHYSICAL_PORT_OF_" + net_type + "_NET"] = []
            for different_destination in locals()["A664_DIFFERENT_PHYSICAL_PORT_OF_" + net_type + "_NET"]:
                NUMBER_OF_MESSAGES = 0
                for destination_index in range( len( locals()["A664_PHYSICAL_PORT_OF_" + net_type + "_NET" ])):
                    if set(locals()["A664_PHYSICAL_PORT_OF_" + net_type + "_NET"][destination_index]) == set(different_destination):
                        NUMBER_OF_MESSAGES += 1
                locals()["MESSAGES_NUMBER_OF_A664_DIFFERENT_PHYSICAL_PORT_OF_" + net_type + "_NET"].append(NUMBER_OF_MESSAGES)
            SORTED = sorted(enumerate(locals()["MESSAGES_NUMBER_OF_A664_DIFFERENT_PHYSICAL_PORT_OF_" + net_type + "_NET"]), key=lambda x: x[1])
            idx = [ i[0] for i in SORTED]
            nums = [ i[1] for i in SORTED]
            for different_destination_index in idx[::-1]:
                different_destination = locals()["A664_DIFFERENT_PHYSICAL_PORT_OF_" + net_type + "_NET"][different_destination_index]
                SIZE, DELAY, PERIOD, MESSAGES_GUID, LOGICAL_DESTINATION, PHYSICAL_DESTINATION, DELAY_BOUND, DELAY_OCCURRED = [], [], [], [], [], [], [], []
                for destination_index in range(len(locals()["A664_PHYSICAL_PORT_OF_" + net_type + "_NET"])):
                    if set(locals()[ "A664_PHYSICAL_PORT_OF_" + net_type + "_NET"][destination_index]) == set(different_destination):
                        SIZE.append(locals()["A664_SIZE_OF_" + net_type + "_NET"][destination_index])
                        DELAY.append(locals()["A664_DELAY_OF_" + net_type + "_NET"][destination_index])
                        PERIOD.append(locals()["A664_PERIOD_OF_" + net_type + "_NET"][destination_index])
                        MESSAGES_GUID.append(locals()["A664_MESSAGES_GUID_OF_" + net_type + "_NET"][destination_index])
                        LOGICAL_DESTINATION.append(locals()["A664_LOGICAL_DESTINATION_OF_" + net_type + "_NET"][destination_index])
                        PHYSICAL_DESTINATION.append(locals()["A664_PHYSICAL_PORT_OF_" + net_type + "_NET"][destination_index])
                        DELAY_BOUND.append(locals()["A664_DELAY_BOUND_OF_" + net_type + "_NET"][destination_index])
                        DELAY_OCCURRED.append(locals()["A664_DELAY_OCCURRED_OF_" + net_type + "_NET"][destination_index])

                DATA_TRANSMITTING_OF_VL_PROCESSING = Data_Transmitting_of_VL_Processing.DATA_TRANSMITTING_OF_VL_PROCESSING(
                                                                                                                           1,
                                                                                                                           SIZE,
                                                                                                                           DELAY,
                                                                                                                           PERIOD,
                                                                                                                           MESSAGES_GUID,
                                                                                                                           LOGICAL_DESTINATION,
                                                                                                                           PHYSICAL_DESTINATION,
                                                                                                                           DELAY_BOUND,
                                                                                                                           DELAY_OCCURRED,
                                                                                                                           "ARINC664",
                                                                                                                           net_type,
                                                                                                                           UPPER_LIMIT_OF_THE_NUMBER_OF_MESSAGES,
                                                                                                                           AVERAGE_NUMBER_OF_MESSAGES
                                                                                                                           )
                VL_INFORMATION, bandwidth_cost = DATA_TRANSMITTING_OF_VL_PROCESSING.data_transmitting_of_vl_processing(GAP, TIMELIMITED, EXPANDED_COEFFICIENT, PHYSICAL_PORT_RATE)
                print("ORIGINAL PHYSICAL_PORT_RATE: %f and bandwidth of VL is: %f!" % (PHYSICAL_PORT_RATE, bandwidth_cost))
                PHYSICAL_PORT_RATE -= bandwidth_cost
                if net_type == "A":
                    if messages_of_physical_port[0] in VL_DICT_OF_A_NET_OF_ARINC664:
                        VL_DICT_OF_A_NET_OF_ARINC664[messages_of_physical_port[0]] += VL_INFORMATION
                    else:
                        if VL_INFORMATION != []:
                                VL_DICT_OF_A_NET_OF_ARINC664[messages_of_physical_port[0]] = VL_INFORMATION
                else:
                    if messages_of_physical_port[0] in VL_DICT_OF_B_NET_OF_ARINC664:
                        VL_DICT_OF_B_NET_OF_ARINC664[messages_of_physical_port[0]] += VL_INFORMATION
                    else:
                        if VL_INFORMATION != []:
                                VL_DICT_OF_B_NET_OF_ARINC664[messages_of_physical_port[0]] = VL_INFORMATION
            return [VL_DICT_OF_A_NET_OF_ARINC664, VL_DICT_OF_B_NET_OF_ARINC664]

    def messages_preprocessing_of_vl_of_afdx(
                                             self,
                                             messages_of_physical_port,
                                             physical_ports_information,
                                             VL_DICT_OF_A_NET_OF_AFDX,
                                             VL_DICT_OF_B_NET_OF_AFDX,
                                             GAP,
                                             TIMELIMITED,
                                             EXPANDED_COEFFICIENT,
                                             UPPER_LIMIT_OF_THE_NUMBER_OF_MESSAGES,
                                             AVERAGE_NUMBER_OF_MESSAGES,
                                             ALLOCATED_RATE_COEFFICIENT # RDIU设备既有ARINC664消息，又有非ARINC664消息，因此，需要将带宽在非ARINC664以及ARINC664消息间进行分配。具体分配原则：非ARINC占 ORIGINAL_RATE * ALLOCATED_RATE_COEFFICIENT
                                             ):
        print("Physical device:", messages_of_physical_port[0])
        if messages_of_physical_port[0] in ["RDIU_01", "RDIU_02", "RDIU_03", "RDIU_04", "RDIU_05", "RDIU_06", "RDIU_07", "RDIU_08",
                                            "RDIU_09", "RDIU_10", "RDIU_11", "RDIU_12", "RDIU_13", "RDIU_14", "RDIU_15", "RDIU_16"]:
            """
            首先判断目的物理端口的类型：ARINC664或非ARINC664
            若目的物理端口类型为ARINC664，则进一步判断是A网端口还是B网端口；
            1、若目的物理端口类型为ARINC664且为A网端口，或者目的物理端口为非ARINC664，则将消息划分进A网的虚链路中
            2、若目的物理端口类型为ARINC664且为B网端口，则将消息划分进B网的虚链路中
            """
            for MESSAGE_TYPE in ["CAN", "A429", "Analog"]:
                for NET_TYPE in ["A", "B"]:
                    locals()[ MESSAGE_TYPE + "_SIZE_OF_" + NET_TYPE + "_NET" ] = []
                    locals()[ MESSAGE_TYPE + "_DELAY_OF_" + NET_TYPE + "_NET" ] = []
                    locals()[ MESSAGE_TYPE + "_PERIOD_OF_" + NET_TYPE + "_NET" ] = []
                    locals()[ MESSAGE_TYPE + "_DICT_OF_" + NET_TYPE + "_NET" ] = dict()
                    locals()[ MESSAGE_TYPE + "_INDEX_OF_" + NET_TYPE + "_NET" ] = 0
                    locals()[ MESSAGE_TYPE + "_MESSAGES_GUID_OF_" + NET_TYPE + "_NET" ] = []
                    locals()[ MESSAGE_TYPE + "_LOGICAL_DESTINATION_OF_" + NET_TYPE + "_NET" ] = []
                    locals()[ MESSAGE_TYPE + "_PHYSICAL_PORT_OF_" + NET_TYPE + "_NET" ] = []
                    locals()[ MESSAGE_TYPE + "_DELAY_BOUND_OF_" + NET_TYPE + "_NET" ] = []
                    locals()[ MESSAGE_TYPE + "_DELAY_OCCURRED_OF_" + NET_TYPE + "_NET" ] = []
            # 先将消息按照类型以及所属网络分类
            for Non_ARINC664_messages_index in range(len(messages_of_physical_port[1])):
                message_type = messages_of_physical_port[1][Non_ARINC664_messages_index]
                INDICATOR_OF_A_NET, INDICATOR_OF_B_NET = 1, 1 # 标志此消息是否已归属到相对应的网络中
                for NET_TYPE in ["A", "B"]:
                    locals()[message_type + "_logical_destination_of_" + NET_TYPE + "_NET"], locals()[message_type + "_physical_destination_of_" + NET_TYPE + "_NET"] = [], []
                    locals()[message_type + "_delay_bound_of_" + NET_TYPE + "_NET"], locals()[message_type + "_delay_occurred_of_" + NET_TYPE + "_NET"] = [], []
                for logical_port_index in range(len(messages_of_physical_port[6][Non_ARINC664_messages_index])): # len( messages_of_physical_port[6][Non_ARINC664_messages_index] )表示该消息被发送至逻辑端口的数目
                    for physical_port_index in range(len( messages_of_physical_port[7][Non_ARINC664_messages_index][logical_port_index])): # 发送至同一个逻辑端口的消息可能途径A、B网的两个物理端口
                        physical_port_name = messages_of_physical_port[7][Non_ARINC664_messages_index][logical_port_index][physical_port_index]
                        if (physical_ports_information[physical_port_name][0] == "AswPhysPort" or physical_ports_information[physical_port_name][0] == "AesPhysPort") and physical_port_name[-2:] == ".B": # 目的物理端口是A664协议且属于B网络
                            if INDICATOR_OF_B_NET == 1:
                                locals()[message_type + "_SIZE_OF_B_NET"].append(messages_of_physical_port[2][ Non_ARINC664_messages_index])
                                locals()[message_type + "_DELAY_OF_B_NET"].append(messages_of_physical_port[3][ Non_ARINC664_messages_index])
                                locals()[message_type + "_PERIOD_OF_B_NET"].append(messages_of_physical_port[4][ Non_ARINC664_messages_index])
                                locals()[message_type + "_DICT_OF_B_NET"][locals()[message_type + "_INDEX_OF_B_NET"]] = Non_ARINC664_messages_index
                                locals()[message_type + "_INDEX_OF_B_NET"] += 1
                                locals()[message_type + "_MESSAGES_GUID_OF_B_NET"].append(messages_of_physical_port[5][Non_ARINC664_messages_index])
                                INDICATOR_OF_B_NET = 0
                            locals()[message_type + "_logical_destination_of_B_NET"].append(messages_of_physical_port[6][Non_ARINC664_messages_index][logical_port_index])
                            locals()[message_type + "_physical_destination_of_B_NET"].append(messages_of_physical_port[7][Non_ARINC664_messages_index][logical_port_index][physical_port_index])
                            locals()[message_type + "_delay_bound_of_B_NET"].append(messages_of_physical_port[8][Non_ARINC664_messages_index][logical_port_index])
                            locals()[message_type + "_delay_occurred_of_B_NET"].append(messages_of_physical_port[9][Non_ARINC664_messages_index][logical_port_index])
                        else:
                            if INDICATOR_OF_A_NET == 1:
                                locals()[message_type + "_SIZE_OF_A_NET"].append(messages_of_physical_port[2][Non_ARINC664_messages_index])
                                locals()[message_type + "_DELAY_OF_A_NET"].append(messages_of_physical_port[3][Non_ARINC664_messages_index])
                                locals()[message_type + "_PERIOD_OF_A_NET"].append(messages_of_physical_port[4][Non_ARINC664_messages_index])
                                locals()[message_type + "_DICT_OF_A_NET"][locals()[message_type + "_INDEX_OF_A_NET"]] = Non_ARINC664_messages_index
                                locals()[message_type + "_INDEX_OF_A_NET"] += 1
                                locals()[message_type + "_MESSAGES_GUID_OF_A_NET"].append(messages_of_physical_port[5][Non_ARINC664_messages_index])
                                INDICATOR_OF_A_NET = 0
                            locals()[message_type + "_logical_destination_of_A_NET"].append(messages_of_physical_port[6][Non_ARINC664_messages_index][logical_port_index])
                            locals()[message_type + "_physical_destination_of_A_NET"].append(messages_of_physical_port[7][Non_ARINC664_messages_index ][logical_port_index][physical_port_index])
                            locals()[message_type + "_delay_bound_of_A_NET"].append(messages_of_physical_port[8][Non_ARINC664_messages_index][logical_port_index])
                            locals()[message_type + "_delay_occurred_of_A_NET"].append(messages_of_physical_port[9][Non_ARINC664_messages_index][logical_port_index])
                for NET_TYPE in ["A", "B"]:
                    if locals()[message_type + "_logical_destination_of_" + NET_TYPE + "_NET"] != []:
                        locals()[message_type + "_LOGICAL_DESTINATION_OF_" + NET_TYPE + "_NET"].append(locals()[message_type + "_logical_destination_of_" + NET_TYPE + "_NET"])
                        locals()[message_type + "_PHYSICAL_PORT_OF_" + NET_TYPE + "_NET"].append(locals()[message_type + "_physical_destination_of_" + NET_TYPE + "_NET"])
                        locals()[message_type + "_DELAY_BOUND_OF_" + NET_TYPE + "_NET"].append(locals()[message_type + "_delay_bound_of_" + NET_TYPE + "_NET"])
                        locals()[message_type + "_DELAY_OCCURRED_OF_" + NET_TYPE + "_NET"].append( locals()[message_type + "_delay_occurred_of_" + NET_TYPE + "_NET"])

            # 考虑到从同一物理端口转发的不同消息，可能具有相同的目的地。
            # 因此，先统一下不同目的地的数目，然后将相同目的地的消息放在一起进行合并与转发
            for MESSAGE_TYPE in ["CAN", "A429", "Analog"]:
                for NET_TYPE in ["A", "B"]:
                    locals()["DIFFERENT_PHYSICAL_PORT_OF_" + MESSAGE_TYPE + "_OF_" + NET_TYPE + "_NET"] = []
                    for physical_destination in locals()[MESSAGE_TYPE + "_PHYSICAL_PORT_OF_" + NET_TYPE + "_NET"]:
                        indicator = 0  # 标志destination是否已经存在于DIFFERENT_DESTINATIONS中
                        for different_physical_destination in locals()["DIFFERENT_PHYSICAL_PORT_OF_" + MESSAGE_TYPE + "_OF_" + NET_TYPE + "_NET"]:
                            if set(physical_destination) == set(different_physical_destination):
                                indicator = 1
                        if indicator == 0:
                            locals()["DIFFERENT_PHYSICAL_PORT_OF_" + MESSAGE_TYPE + "_OF_" + NET_TYPE + "_NET"].append(physical_destination)

            # 统计归属不同网络的消息分组的类别数
            for NET_TYPE in ["A", "B"]:
                locals()["NUMBER_OF_DIFFERENT_SET_OF_MESSAGES_OF_" + NET_TYPE + "_NET"] = 0
            for NET_TYPE in ["A", "B"]:
                for MESSAGE_TYPE in ["CAN", "A429", "Analog"]:
                    locals()["NUMBER_OF_DIFFERENT_SET_OF_MESSAGES_OF_" + NET_TYPE + "_NET"] += len( locals()["DIFFERENT_PHYSICAL_PORT_OF_" + MESSAGE_TYPE + "_OF_" + NET_TYPE + "_NET"])

            RATE_OF_PHYSICAL_PORT = physical_ports_information[messages_of_physical_port[0] + "." + NET_TYPE][7] * 1000  # 物理端口原始的速率（带宽）
            ALLOCATED_RATE_OF_PHYSICAL_PORT = RATE_OF_PHYSICAL_PORT * ALLOCATED_RATE_COEFFICIENT
            for NET_TYPE in ["A", "B"]:
                PHYSICAL_PORT_RATE = ALLOCATED_RATE_OF_PHYSICAL_PORT
                for MESSAGE_TYPE in ["CAN", "A429", "Analog"]:
                    for different_destination in locals()["DIFFERENT_PHYSICAL_PORT_OF_" + MESSAGE_TYPE + "_OF_" + NET_TYPE + "_NET"]:
                        SIZE, DELAY, PERIOD, MESSAGES_GUID, LOGICAL_DESTINATION, PHYSICAL_DESTINATION, DELAY_BOUND, DELAY_OCCURRED = [], [], [], [], [], [], [], []
                        for destination_index in range(len(locals()[MESSAGE_TYPE + "_PHYSICAL_PORT_OF_" + NET_TYPE + "_NET"])):
                            if set(locals()[MESSAGE_TYPE + "_PHYSICAL_PORT_OF_" + NET_TYPE + "_NET"][destination_index]) == set(different_destination):
                                SIZE.append(locals()[MESSAGE_TYPE + "_SIZE_OF_" + NET_TYPE + "_NET"][destination_index])
                                DELAY.append(locals()[MESSAGE_TYPE + "_DELAY_OF_" + NET_TYPE + "_NET"][destination_index])
                                PERIOD.append(locals()[MESSAGE_TYPE + "_PERIOD_OF_" + NET_TYPE + "_NET"][destination_index])
                                MESSAGES_GUID.append(locals()[MESSAGE_TYPE + "_MESSAGES_GUID_OF_" + NET_TYPE + "_NET"][destination_index])
                                LOGICAL_DESTINATION.append(locals()[MESSAGE_TYPE + "_LOGICAL_DESTINATION_OF_" + NET_TYPE + "_NET"][destination_index])
                                PHYSICAL_DESTINATION.append(locals()[MESSAGE_TYPE + "_PHYSICAL_PORT_OF_" + NET_TYPE + "_NET"][destination_index])
                                DELAY_BOUND.append(locals()[MESSAGE_TYPE + "_DELAY_BOUND_OF_" + NET_TYPE + "_NET" ][ destination_index])
                                DELAY_OCCURRED.append(locals()[MESSAGE_TYPE + "_DELAY_OCCURRED_OF_" + NET_TYPE + "_NET"][destination_index])

                        DATA_TRANSMITTING_OF_VL_PROCESSING = Data_Transmitting_of_VL_Processing.DATA_TRANSMITTING_OF_VL_PROCESSING(
                                                                                                                                   0,
                                                                                                                                   SIZE,
                                                                                                                                   DELAY,
                                                                                                                                   PERIOD,
                                                                                                                                   MESSAGES_GUID,
                                                                                                                                   LOGICAL_DESTINATION,
                                                                                                                                   PHYSICAL_DESTINATION,
                                                                                                                                   DELAY_BOUND,
                                                                                                                                   DELAY_OCCURRED,
                                                                                                                                   MESSAGE_TYPE,
                                                                                                                                   NET_TYPE,
                                                                                                                                   UPPER_LIMIT_OF_THE_NUMBER_OF_MESSAGES,
                                                                                                                                   AVERAGE_NUMBER_OF_MESSAGES
                                                                                                                                   )
                        locals()["VL_INFORMATION_OF_" + NET_TYPE + "_NET"], bandwidth_cost = DATA_TRANSMITTING_OF_VL_PROCESSING.data_transmitting_of_vl_processing(GAP, TIMELIMITED, EXPANDED_COEFFICIENT, PHYSICAL_PORT_RATE)
                        print("ORIGINAL PHYSICAL_PORT_RATE: %f and bandwidth of VL is: %f!" % (PHYSICAL_PORT_RATE, bandwidth_cost))
                        PHYSICAL_PORT_RATE -= bandwidth_cost

                        if NET_TYPE == "A":
                            if messages_of_physical_port[0] + ".A" in VL_DICT_OF_A_NET_OF_AFDX:
                                VL_DICT_OF_A_NET_OF_AFDX[messages_of_physical_port[0] + ".A"] += locals()["VL_INFORMATION_OF_" + NET_TYPE + "_NET"]
                            else:
                                if locals()["VL_INFORMATION_OF_" + NET_TYPE + "_NET"] != []:
                                    VL_DICT_OF_A_NET_OF_AFDX[messages_of_physical_port[0] + ".A"] = locals()["VL_INFORMATION_OF_" + NET_TYPE + "_NET"]
                        else:
                            if messages_of_physical_port[0] + ".B" in VL_DICT_OF_B_NET_OF_AFDX:
                                VL_DICT_OF_B_NET_OF_AFDX[messages_of_physical_port[0] + ".B"] += locals()["VL_INFORMATION_OF_" + NET_TYPE + "_NET"]
                            else:
                                if locals()["VL_INFORMATION_OF_" + NET_TYPE + "_NET"] != []:
                                    VL_DICT_OF_B_NET_OF_AFDX[messages_of_physical_port[0] + ".B"] = locals()["VL_INFORMATION_OF_" + NET_TYPE + "_NET"]
            return [VL_DICT_OF_A_NET_OF_AFDX, VL_DICT_OF_B_NET_OF_AFDX]
        else:
            """
            首先判断目的物理端口的类型：ARINC664或非ARINC664
            若目的物理端口类型为ARINC664，则进一步判断是A网端口还是B网端口；
            1、若目的物理端口类型为ARINC664且为A网端口，或者目的物理端口为非ARINC664，则将消息划分进A网的虚链路中
            2、若目的物理端口类型为ARINC664且为B网端口，则将消息划分进B网的虚链路中
            """
            net_type = messages_of_physical_port[0][-1:]  # 该ARINC664端口属于A网还是B网
            locals()["A664_SIZE_OF_" + net_type + "_NET"] = []
            locals()["A664_DELAY_OF_" + net_type + "_NET"] = []
            locals()["A664_PERIOD_OF_" + net_type + "_NET" ] = []
            locals()["A664_DICT_OF_" + net_type + "_NET"] = dict()
            locals()["A664_INDEX_OF_" + net_type + "_NET"] = 0
            locals()["A664_MESSAGES_GUID_OF_" + net_type + "_NET"] = []
            locals()["A664_LOGICAL_DESTINATION_OF_" + net_type + "_NET"] = []
            locals()["A664_PHYSICAL_PORT_OF_" + net_type + "_NET"] = []
            locals()["A664_DELAY_BOUND_OF_" + net_type + "_NET"] = []
            locals()["A664_DELAY_OCCURRED_OF_" + net_type + "_NET"] = []
            for Non_ARINC664_messages_index in range(len(messages_of_physical_port[1])):
                message_type = messages_of_physical_port[1][Non_ARINC664_messages_index] # A664
                INDICATOR = 1
                if message_type != "A664":
                    print("There is an error in message type!")
                    break
                locals()["A664_logical_destination_of_" + net_type + "_NET"], locals()["A664_physical_destination_of_" + net_type + "_NET"] = [], []
                locals()["A664_delay_bound_of_" + net_type + "_NET"], locals()["A664_delay_occurred_of_" + net_type + "_NET"] = [], []
                for logical_port_index in range(len(messages_of_physical_port[6][Non_ARINC664_messages_index])): # len( messages_of_physical_port[6][Non_ARINC664_messages_index] )表示该消息被发送至逻辑端口的数目
                    for physical_port_index in range(len(messages_of_physical_port[7][Non_ARINC664_messages_index][logical_port_index])): # 发送至同一个逻辑端口的消息可能途径A、B网的两个物理端口
                        physical_port_name = messages_of_physical_port[7][Non_ARINC664_messages_index][logical_port_index][physical_port_index]
                        if physical_ports_information[ physical_port_name ][0] == "AswPhysPort" or physical_ports_information[ physical_port_name ][0] == "AesPhysPort": # 目的物理端口是ARINC664端口
                            if physical_port_name[-2:] == "." + net_type:
                                if INDICATOR == 1:
                                    locals()[message_type + "_SIZE_OF_" + net_type + "_NET"].append(messages_of_physical_port[2][Non_ARINC664_messages_index])
                                    locals()[message_type + "_DELAY_OF_" + net_type + "_NET"].append(messages_of_physical_port[3][Non_ARINC664_messages_index])
                                    locals()[message_type + "_PERIOD_OF_" + net_type + "_NET"].append(messages_of_physical_port[4][Non_ARINC664_messages_index])
                                    locals()[message_type + "_DICT_OF_" + net_type + "_NET"][locals()[message_type + "_INDEX_OF_" + net_type + "_NET"]] = Non_ARINC664_messages_index
                                    locals()[message_type + "_INDEX_OF_" + net_type + "_NET"] += 1
                                    locals()[message_type + "_MESSAGES_GUID_OF_" + net_type + "_NET"].append(messages_of_physical_port[5][Non_ARINC664_messages_index])
                                    INDICATOR = 0
                                locals()[message_type + "_logical_destination_of_" + net_type + "_NET"].append(messages_of_physical_port[6][Non_ARINC664_messages_index][logical_port_index])
                                locals()[message_type + "_physical_destination_of_" + net_type + "_NET"].append(messages_of_physical_port[7][Non_ARINC664_messages_index][logical_port_index][physical_port_index])
                                locals()[message_type + "_delay_bound_of_" + net_type + "_NET"].append(messages_of_physical_port[8][Non_ARINC664_messages_index][logical_port_index])
                                locals()[message_type + "_delay_occurred_of_" + net_type + "_NET"].append(messages_of_physical_port[9][Non_ARINC664_messages_index][logical_port_index])
                        else: # 目的物理端口是非ARINC664端口
                            if INDICATOR == 1:
                                locals()[message_type + "_SIZE_OF_" + net_type + "_NET"].append(messages_of_physical_port[2][Non_ARINC664_messages_index])
                                locals()[message_type + "_DELAY_OF_" + net_type + "_NET"].append(messages_of_physical_port[3][Non_ARINC664_messages_index])
                                locals()[message_type + "_PERIOD_OF_" + net_type + "_NET"].append(messages_of_physical_port[4][Non_ARINC664_messages_index])
                                locals()[message_type + "_DICT_OF_" + net_type + "_NET"][locals()[message_type + "_INDEX_OF_" + net_type + "_NET"]] = Non_ARINC664_messages_index
                                locals()[message_type + "_INDEX_OF_" + net_type + "_NET"] += 1
                                locals()[message_type + "_MESSAGES_GUID_OF_" + net_type + "_NET"].append(messages_of_physical_port[5][Non_ARINC664_messages_index])
                                INDICATOR = 0
                            locals()[message_type + "_logical_destination_of_" + net_type + "_NET"].append(messages_of_physical_port[6][Non_ARINC664_messages_index][ logical_port_index])
                            locals()[message_type + "_physical_destination_of_" + net_type + "_NET"].append(messages_of_physical_port[7][Non_ARINC664_messages_index][ logical_port_index][physical_port_index])
                            locals()[message_type + "_delay_bound_of_" + net_type + "_NET"].append(messages_of_physical_port[8][Non_ARINC664_messages_index][logical_port_index])
                            locals()[message_type + "_delay_occurred_of_" + net_type + "_NET"].append(messages_of_physical_port[9][Non_ARINC664_messages_index][logical_port_index])
                if locals()[message_type + "_logical_destination_of_" + net_type + "_NET"] != []:
                    locals()[message_type + "_LOGICAL_DESTINATION_OF_" + net_type + "_NET"].append(locals()[message_type + "_logical_destination_of_" + net_type + "_NET"])
                    locals()[message_type + "_PHYSICAL_PORT_OF_" + net_type + "_NET"].append(locals()[message_type + "_physical_destination_of_" + net_type + "_NET"])
                    locals()[message_type + "_DELAY_BOUND_OF_" + net_type + "_NET"].append(locals()[message_type + "_delay_bound_of_" + net_type + "_NET"])
                    locals()[message_type + "_DELAY_OCCURRED_OF_" + net_type + "_NET"].append(locals()[message_type + "_delay_occurred_of_" + net_type + "_NET"])

            # 考虑到从同一物理端口转发的不同消息，可能具有相同的目的地。
            # 因此，先统一下不同目的地的数目，然后将相同目的地的消息放在一起进行合并与转发
            locals()["A664_DIFFERENT_PHYSICAL_PORT_OF_" + net_type + "_NET"] = []
            for logical_destination in locals()["A664_PHYSICAL_PORT_OF_" + net_type + "_NET"]:
                indicator = 0  # 标志destination是否已经存在于DIFFERENT_DESTINATIONS中
                for different_logical_destination in locals()["A664_DIFFERENT_PHYSICAL_PORT_OF_" + net_type + "_NET"]:
                    if set(logical_destination) == set(different_logical_destination):
                        indicator = 1
                if indicator == 0:
                    locals()["A664_DIFFERENT_PHYSICAL_PORT_OF_" + net_type + "_NET"].append(logical_destination)

            # 统计消息分组的类别数
                locals()["NUMBER_OF_DIFFERENT_SET_OF_MESSAGES_OF_" + net_type + "_NET"] = len( locals()["A664_DIFFERENT_PHYSICAL_PORT_OF_" + net_type + "_NET"])

            RATE_OF_PHYSICAL_PORT = physical_ports_information[messages_of_physical_port[0]][7] * 1000 # 物理端口原始的速率（带宽）
            if messages_of_physical_port[0][0:7] in ["RDIU_01", "RDIU_02", "RDIU_03", "RDIU_04", "RDIU_05", "RDIU_06", "RDIU_07", "RDIU_08",
                                                    "RDIU_09", "RDIU_10", "RDIU_11", "RDIU_12", "RDIU_13", "RDIU_14", "RDIU_15", "RDIU_16"]:
                ALLOCATED_RATE_OF_PHYSICAL_PORT = RATE_OF_PHYSICAL_PORT * (1-ALLOCATED_RATE_COEFFICIENT)
            else:
                ALLOCATED_RATE_OF_PHYSICAL_PORT = RATE_OF_PHYSICAL_PORT
            PHYSICAL_PORT_RATE = ALLOCATED_RATE_OF_PHYSICAL_PORT

            locals()["MESSAGES_NUMBER_OF_A664_DIFFERENT_PHYSICAL_PORT_OF_" + net_type + "_NET"] = []
            for different_destination in locals()["A664_DIFFERENT_PHYSICAL_PORT_OF_" + net_type + "_NET"]:
                NUMBER_OF_MESSAGES = 0
                for destination_index in range( len( locals()["A664_PHYSICAL_PORT_OF_" + net_type + "_NET" ])):
                    if set(locals()["A664_PHYSICAL_PORT_OF_" + net_type + "_NET"][destination_index]) == set(different_destination):
                        NUMBER_OF_MESSAGES += 1
                locals()["MESSAGES_NUMBER_OF_A664_DIFFERENT_PHYSICAL_PORT_OF_" + net_type + "_NET"].append(NUMBER_OF_MESSAGES)
            SORTED = sorted(enumerate(locals()["MESSAGES_NUMBER_OF_A664_DIFFERENT_PHYSICAL_PORT_OF_" + net_type + "_NET"]), key=lambda x: x[1])
            idx = [ i[0] for i in SORTED]
            nums = [ i[1] for i in SORTED]
            for different_destination_index in idx[::-1]:
                different_destination = locals()["A664_DIFFERENT_PHYSICAL_PORT_OF_" + net_type + "_NET"][different_destination_index]
                SIZE, DELAY, PERIOD, MESSAGES_GUID, LOGICAL_DESTINATION, PHYSICAL_DESTINATION, DELAY_BOUND, DELAY_OCCURRED = [], [], [], [], [], [], [], []
                for destination_index in range(len(locals()["A664_PHYSICAL_PORT_OF_" + net_type + "_NET"])):
                    if set(locals()[ "A664_PHYSICAL_PORT_OF_" + net_type + "_NET"][destination_index]) == set(different_destination):
                        SIZE.append(locals()["A664_SIZE_OF_" + net_type + "_NET"][destination_index])
                        DELAY.append(locals()["A664_DELAY_OF_" + net_type + "_NET"][destination_index])
                        PERIOD.append(locals()["A664_PERIOD_OF_" + net_type + "_NET"][destination_index])
                        MESSAGES_GUID.append(locals()["A664_MESSAGES_GUID_OF_" + net_type + "_NET"][destination_index])
                        LOGICAL_DESTINATION.append(locals()["A664_LOGICAL_DESTINATION_OF_" + net_type + "_NET"][destination_index])
                        PHYSICAL_DESTINATION.append(locals()["A664_PHYSICAL_PORT_OF_" + net_type + "_NET"][destination_index])
                        DELAY_BOUND.append(locals()["A664_DELAY_BOUND_OF_" + net_type + "_NET"][destination_index])
                        DELAY_OCCURRED.append(locals()["A664_DELAY_OCCURRED_OF_" + net_type + "_NET"][destination_index])

                DATA_TRANSMITTING_OF_VL_PROCESSING = Data_Transmitting_of_VL_Processing.DATA_TRANSMITTING_OF_VL_PROCESSING(
                                                                                                                           1,
                                                                                                                           SIZE,
                                                                                                                           DELAY,
                                                                                                                           PERIOD,
                                                                                                                           MESSAGES_GUID,
                                                                                                                           LOGICAL_DESTINATION,
                                                                                                                           PHYSICAL_DESTINATION,
                                                                                                                           DELAY_BOUND,
                                                                                                                           DELAY_OCCURRED,
                                                                                                                           "ARINC664",
                                                                                                                           net_type,
                                                                                                                           UPPER_LIMIT_OF_THE_NUMBER_OF_MESSAGES,
                                                                                                                           AVERAGE_NUMBER_OF_MESSAGES
                                                                                                                           )
                VL_INFORMATION, bandwidth_cost = DATA_TRANSMITTING_OF_VL_PROCESSING.data_transmitting_of_vl_processing(GAP, TIMELIMITED, EXPANDED_COEFFICIENT, PHYSICAL_PORT_RATE)
                print("ORIGINAL PHYSICAL_PORT_RATE: %f and bandwidth of VL is: %f!" % (PHYSICAL_PORT_RATE, bandwidth_cost))
                PHYSICAL_PORT_RATE -= bandwidth_cost
                if net_type == "A":
                    if messages_of_physical_port[0] in VL_DICT_OF_A_NET_OF_AFDX:
                        VL_DICT_OF_A_NET_OF_AFDX[messages_of_physical_port[0]] += VL_INFORMATION
                    else:
                        if VL_INFORMATION != []:
                                VL_DICT_OF_A_NET_OF_AFDX[messages_of_physical_port[0]] = VL_INFORMATION
                else:
                    if messages_of_physical_port[0] in VL_DICT_OF_B_NET_OF_AFDX:
                        VL_DICT_OF_B_NET_OF_AFDX[messages_of_physical_port[0]] += VL_INFORMATION
                    else:
                        if VL_INFORMATION != []:
                                VL_DICT_OF_B_NET_OF_AFDX[messages_of_physical_port[0]] = VL_INFORMATION
            return [VL_DICT_OF_A_NET_OF_AFDX, VL_DICT_OF_B_NET_OF_AFDX]