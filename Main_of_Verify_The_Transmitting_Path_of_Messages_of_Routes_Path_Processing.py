import os
import numpy as np
import Verify_The_Transmitting_Path_of_Messages_of_Routes_Path_Processing
import Hyper_Parameters

class MAIN_OF_VERIFY_THE_TRANSMITTING_PATH_OF_MESSAGES_OF_ROUTES_PATH_PROCESSING():
    def __init__(self):
        self.MESSAGES_DICT_FILE_PATH = Hyper_Parameters.messages_routes_file
        self.messages_info = np.load(Hyper_Parameters.intermediate_data_file + "/messages_info.npy", allow_pickle="TRUE").item()

    def get_messages_dict_files(self):
        messages_dict_name_list = []
        if os.path.exists(self.MESSAGES_DICT_FILE_PATH):
            for messages_dict in os.listdir(self.MESSAGES_DICT_FILE_PATH):
                messages_dict_name_list.append(self.MESSAGES_DICT_FILE_PATH + "/" + messages_dict)
        return messages_dict_name_list

    def main(self):
        original_messages_dict_name_list = self.get_messages_dict_files()
        # 将messages_dict_name_list按照网络拓扑分类
        messages_dict_name_list_of_AFDX, messages_dict_name_list_of_ARINC664 = [], []
        for messages_dict_name in original_messages_dict_name_list:
            if messages_dict_name.find("AFDX") != -1:
                messages_dict_name_list_of_AFDX.append(messages_dict_name)
            if messages_dict_name.find("ARINC664") != -1:
                messages_dict_name_list_of_ARINC664.append(messages_dict_name)

        # 再将messages_dict_name_list_of_AFDX、messages_dict_name_list_of_ARINC664按照A、B网分类
        messages_dict_name_list_of_AFDX_OF_A_NET, messages_dict_name_list_of_ARINC664_OF_A_NET = [], []
        messages_dict_name_list_of_AFDX_OF_B_NET, messages_dict_name_list_of_ARINC664_OF_B_NET = [], []
        for messages_dict_name in messages_dict_name_list_of_AFDX:
            if messages_dict_name.find("A_NET") != -1:
                messages_dict_name_list_of_AFDX_OF_A_NET.append(messages_dict_name)
            if messages_dict_name.find("B_NET") != -1:
                messages_dict_name_list_of_AFDX_OF_B_NET.append(messages_dict_name)

        for messages_dict_name in messages_dict_name_list_of_ARINC664:
            if messages_dict_name.find("A_NET") != -1:
                messages_dict_name_list_of_ARINC664_OF_A_NET.append(messages_dict_name)
            if messages_dict_name.find("B_NET") != -1:
                messages_dict_name_list_of_ARINC664_OF_B_NET.append(messages_dict_name)

        # 开始检验消息传输路径的回溯结果的正确性
        VERIFY_THE_TRANSMITTING_PATH_OF_MESSAGES_OF_ROUTES_PATH_PROCESSING = \
            Verify_The_Transmitting_Path_of_Messages_of_Routes_Path_Processing.VERIFY_THE_TRANSMITTING_PATH_OF_MESSAGES_OF_ROUTES_PATH_PROCESSING(self.messages_info)
        VERIFY_THE_TRANSMITTING_PATH_OF_MESSAGES_OF_ROUTES_PATH_PROCESSING.verify_the_transmitting_path_of_messages_of_routes_path_processing(messages_dict_name_list_of_AFDX_OF_A_NET,
                                                                                                                                              messages_dict_name_list_of_ARINC664_OF_A_NET,
                                                                                                                                              messages_dict_name_list_of_AFDX_OF_B_NET,
                                                                                                                                              messages_dict_name_list_of_ARINC664_OF_B_NET
                                                                                                                                              )