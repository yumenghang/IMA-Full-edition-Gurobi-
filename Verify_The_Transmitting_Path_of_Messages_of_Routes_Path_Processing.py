#!/usr/bin/python
# 对于消息是否已在对应文件中分配的检验
# 若无输出说明所有消息已正确分配

import numpy as np

class VERIFY_THE_TRANSMITTING_PATH_OF_MESSAGES_OF_ROUTES_PATH_PROCESSING():
    def __init__(self, messages_info):
        self.messages_info = messages_info

    def verify_the_transmitting_path_of_messages_of_routes_path_processing(
                                                                           self,
                                                                           messages_dict_name_list_of_AFDX_OF_A_NET,
                                                                           messages_dict_name_list_of_ARINC664_OF_A_NET,
                                                                           messages_dict_name_list_of_AFDX_OF_B_NET,
                                                                           messages_dict_name_list_of_ARINC664_OF_B_NET
                                                                          ):
        for messages_dict_name in messages_dict_name_list_of_AFDX_OF_A_NET:
            locals()[messages_dict_name] = np.load(messages_dict_name, allow_pickle=True).item()
        for messages_dict_name in messages_dict_name_list_of_ARINC664_OF_A_NET:
            locals()[messages_dict_name] = np.load(messages_dict_name, allow_pickle=True).item()
        for messages_dict_name in messages_dict_name_list_of_AFDX_OF_B_NET:
            locals()[messages_dict_name] = np.load(messages_dict_name, allow_pickle=True).item()
        for messages_dict_name in messages_dict_name_list_of_ARINC664_OF_B_NET:
            locals()[messages_dict_name] = np.load(messages_dict_name, allow_pickle=True).item()

        # 检验是否每条消息都已被分配
        for message_guid, message_info in self.messages_info.items():
            if message_info[0] == 'A664':  # 即消息为ARINC664类型，需要在所有文件中考虑
                for physical_port in message_info[4]:  # 对于A664类型消息，可以直接根据其发送端物理端口名称判断其位于A网还是B网
                    last_two_ch = physical_port[-2:]  # 选取发送端物理端口全称最后两位字符判断'.A' 还是'.B'
                    if last_two_ch == '.A':
                        for messages_dict_name in messages_dict_name_list_of_AFDX_OF_A_NET:
                            if message_guid not in locals()[messages_dict_name]:
                                print("标识符为%s的消息未在文件%s中分配" % (message_guid, messages_dict_name))
                        for messages_dict_name in messages_dict_name_list_of_ARINC664_OF_A_NET:
                            if message_guid not in locals()[messages_dict_name]:
                                print("标识符为%s的消息未在文件%s中分配" % (message_guid, messages_dict_name))
                    else:
                        for messages_dict_name in messages_dict_name_list_of_AFDX_OF_B_NET:
                            if message_guid not in locals()[messages_dict_name]:
                                print("标识符为%s的消息未在文件%s中分配" % (message_guid, messages_dict_name))
                        for messages_dict_name in messages_dict_name_list_of_ARINC664_OF_B_NET:
                            if message_guid not in locals()[messages_dict_name]:
                                print("标识符为%s的消息未在文件%s中分配" % (message_guid, messages_dict_name))
            else:  # 即消息为非ARINC664类型，只需要在AFDX文件中考虑
                # 由于是非664格式，根据接收端消息的类型和所在网络为A、B网判断
                Is_reciption_message_A664 = 0  # 判断是否有接收端消息格式为664，若是取值为1，否则为0
                Is_reciption_message_in_A = 0  # 判断是否有接收端消息的接受端物理端口在A网
                Is_reciption_message_in_B = 0  # 判断是否有接收端消息的接受端物理端口在B网
                for reciption_message in message_info[9]:  # 一条消息以不同格式发往不同端口，对传到每一接收端的消息遍历
                    if reciption_message[0] == 'A664':
                        Is_reciption_message_A664 = 1
                        for t in reciption_message[4]:
                            if t[-2:] == '.A':
                                Is_reciption_message_in_A = 1
                            if t[-2:] == '.B':
                                Is_reciption_message_in_B = 1
                # 根据不同判断结果在不同的AFDX文件中查找以检验是否分配
                if Is_reciption_message_A664 == 1:
                    if Is_reciption_message_in_A == 1:
                        for messages_dict_name in messages_dict_name_list_of_AFDX_OF_A_NET:
                            if message_guid not in locals()[messages_dict_name]:
                                print("标识符为%s的消息未在文件%s中分配" % (message_guid, messages_dict_name))
                    if Is_reciption_message_in_B == 1:
                        for messages_dict_name in messages_dict_name_list_of_AFDX_OF_B_NET:
                            if message_guid not in locals()[messages_dict_name]:
                                print("标识符为%s的消息未在文件%s中分配" % (message_guid, messages_dict_name))
                else: # 此时只在A网进行传输
                    for messages_dict_name in messages_dict_name_list_of_AFDX_OF_A_NET:
                        if message_guid not in locals()[messages_dict_name]:
                            print("标识符为%s的消息未在文件%s中分配" % (message_guid, messages_dict_name))