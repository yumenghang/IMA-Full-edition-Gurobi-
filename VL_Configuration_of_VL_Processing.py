import numpy as np
import math
import os
import time
import Hyper_Parameters
import Messages_Processing_of_VL_Processing

class VL_CONFIGURATION_OF_VL_PROCESSING():
    def __init__(self):
        self.SAVE_FILE = Hyper_Parameters.vl_dict_file
        self.messages_per_physical_port = np.load(Hyper_Parameters.intermediate_data_file + "messages_per_physical_port.npy", allow_pickle='TRUE').item()
        self.physical_ports_information = np.load(Hyper_Parameters.intermediate_data_file + "physical_ports_information.npy", allow_pickle='TRUE').item()
        self.GAP = Hyper_Parameters.gap_for_vl_optimization # 设置求解精度
        self.TIMELIMITED = Hyper_Parameters.time_limited_for_vl_optimization # 设置求解时间上限，600s为一个单位
        self.EXPANDED_COEFFICIENT = Hyper_Parameters.expanded_coefficient # 设置当单位求解时间上限--600s内无法求出解时，求解时间的扩大系数
        self.ALLOCATED_RATE_COEFFICIENT = Hyper_Parameters.allocated_rate_coefficient # RDIU设备物理端口带宽在非ARINC664消息以及ARINC664消息间的分配比例
        self.UPPER_LIMIT_OF_THE_NUMBER_OF_MESSAGES = 25 # 当End System内消息数目大于UPPER_LIMIT_OF_THE_NUMBER_OF_MESSAGES时，我们将消息作拆分处理，以缩短求解时间
        # 具体拆分规则：假设End System内有N条消息（N>=UPPER_LIMIT_OF_THE_NUMBER_OF_MESSAGES），求得M=ceil( N/AVERAGE_NUMBER_OF_MESSAGES )，其中ceil表示向上取整，每一个消息子集里消息的数目n=ceil(N/M)
        self.AVERAGE_NUMBER_OF_MESSAGES = 9

    def vl_configuration_of_vl_processing_of_arinc664(self):
        if not os.path.exists(self.SAVE_FILE):
            print("%s does not exist!" % (self.SAVE_FILE))
            os.makedirs(self.SAVE_FILE)
            print("Successfully creat %s!" % (self.SAVE_FILE))
        VL_DICT_OF_A_NET_OF_ARINC664, VL_DICT_OF_B_NET_OF_ARINC664 = dict(), dict()
        start_time = time.time()
        for key in list(self.messages_per_physical_port.keys()):
            messages_of_physical_port = self.messages_per_physical_port[key]
            MESSAGES_PROCESSING_OF_VL_PROCESSING = Messages_Processing_of_VL_Processing.MESSAGES_PROCESSING_OF_VL_PROCESSING()
            try:
                RETURNED_VL_DICT_LIST = MESSAGES_PROCESSING_OF_VL_PROCESSING.messages_preprocessing_of_vl_of_arinc664(
                                                                                                                      messages_of_physical_port,
                                                                                                                      self.physical_ports_information,
                                                                                                                      VL_DICT_OF_A_NET_OF_ARINC664,
                                                                                                                      VL_DICT_OF_B_NET_OF_ARINC664,
                                                                                                                      self.GAP,
                                                                                                                      self.TIMELIMITED,
                                                                                                                      self.EXPANDED_COEFFICIENT,
                                                                                                                      self.UPPER_LIMIT_OF_THE_NUMBER_OF_MESSAGES,
                                                                                                                      self.AVERAGE_NUMBER_OF_MESSAGES,
                                                                                                                      self.ALLOCATED_RATE_COEFFICIENT
                                                                                                                      )
            except AttributeError:
                print("VL_Configuration_of_VL_Processing.py (line 41): There is an error in %s!" % messages_of_physical_port)
                continue
            if RETURNED_VL_DICT_LIST != []:
                VL_DICT_OF_A_NET_OF_ARINC664, VL_DICT_OF_B_NET_OF_ARINC664 = RETURNED_VL_DICT_LIST[0], RETURNED_VL_DICT_LIST[1]
                """
                保存文件
                先删除已有的VL dict文件
                再存储更新过后的VL dict文件
                """
                if os.path.exists(self.SAVE_FILE + "VL_DICT_OF_A_NET_OF_ARINC664.npy"):
                    os.remove(self.SAVE_FILE + "VL_DICT_OF_A_NET_OF_ARINC664.npy")
                if os.path.exists(self.SAVE_FILE + "VL_DICT_OF_B_NET_OF_ARINC664.npy"):
                    os.remove(self.SAVE_FILE + "VL_DICT_OF_B_NET_OF_ARINC664.npy")
                np.save(self.SAVE_FILE + "VL_DICT_OF_A_NET_OF_ARINC664.npy", VL_DICT_OF_A_NET_OF_ARINC664)
                np.save(self.SAVE_FILE + "VL_DICT_OF_B_NET_OF_ARINC664.npy", VL_DICT_OF_B_NET_OF_ARINC664)
        end_time = time.time()
        TOTAL_SECONDS = end_time-start_time
        HOURS = math.floor( TOTAL_SECONDS/3600 )
        MINUTES = math.floor( ( TOTAL_SECONDS-3600*HOURS )/60 )
        SECONDS = math.floor( TOTAL_SECONDS-3600*HOURS-60*MINUTES )
        print("Time costed for VL processing of ARINC664 is: %dhours:%dminutes:%dseconds!" % ( HOURS, MINUTES, SECONDS ) )

    def vl_configuration_of_vl_processing_of_afdx(self):
        if not os.path.exists(self.SAVE_FILE):
            print("%s does not exist!" % (self.SAVE_FILE))
            os.makedirs(self.SAVE_FILE)
            print("Successfully creat %s!" % (self.SAVE_FILE))
        VL_DICT_OF_A_NET_OF_AFDX, VL_DICT_OF_B_NET_OF_AFDX = dict(), dict()
        start_time = time.time()
        for key in list(self.messages_per_physical_port.keys()):
            messages_of_physical_port = self.messages_per_physical_port[key]
            MESSAGES_PROCESSING_OF_VL_PROCESSING = Messages_Processing_of_VL_Processing.MESSAGES_PROCESSING_OF_VL_PROCESSING()
            try:
                RETURNED_VL_DICT_LIST = MESSAGES_PROCESSING_OF_VL_PROCESSING.messages_preprocessing_of_vl_of_afdx(messages_of_physical_port,
                                                                                                                  self.physical_ports_information,
                                                                                                                  VL_DICT_OF_A_NET_OF_AFDX,
                                                                                                                  VL_DICT_OF_B_NET_OF_AFDX,
                                                                                                                  self.GAP,
                                                                                                                  self.TIMELIMITED,
                                                                                                                  self.EXPANDED_COEFFICIENT,
                                                                                                                  self.UPPER_LIMIT_OF_THE_NUMBER_OF_MESSAGES,
                                                                                                                  self.AVERAGE_NUMBER_OF_MESSAGES,
                                                                                                                  self.ALLOCATED_RATE_COEFFICIENT
                                                                                                                  )
            except AttributeError:
                print("VL_Configuration_of_VL_Processing.py (line 41): There is an error in %s!" % messages_of_physical_port)
                continue
            if RETURNED_VL_DICT_LIST != []:
                VL_DICT_OF_A_NET_OF_AFDX, VL_DICT_OF_B_NET_OF_AFDX = RETURNED_VL_DICT_LIST[0], RETURNED_VL_DICT_LIST[1]
                """
                保存文件
                先删除已有的VL dict文件
                再存储更新过后的VL dict文件
                """
                if os.path.exists(self.SAVE_FILE + "VL_DICT_OF_A_NET_OF_AFDX.npy"):
                    os.remove(self.SAVE_FILE + "VL_DICT_OF_A_NET_OF_AFDX.npy")
                if os.path.exists(self.SAVE_FILE + "VL_DICT_OF_B_NET_OF_AFDX.npy"):
                    os.remove(self.SAVE_FILE + "VL_DICT_OF_B_NET_OF_AFDX.npy")
                np.save(self.SAVE_FILE + "VL_DICT_OF_A_NET_OF_AFDX.npy", VL_DICT_OF_A_NET_OF_AFDX)
                np.save(self.SAVE_FILE + "VL_DICT_OF_B_NET_OF_AFDX.npy", VL_DICT_OF_B_NET_OF_AFDX)
        end_time = time.time()
        TOTAL_SECONDS = end_time-start_time
        HOURS = math.floor( TOTAL_SECONDS/3600 )
        MINUTES = math.floor( ( TOTAL_SECONDS-3600*HOURS )/60 )
        SECONDS = math.floor( TOTAL_SECONDS-3600*HOURS-60*MINUTES )
        print("Time costed for VL processing of AFDX is: %dhours:%dminutes:%dseconds!" % ( HOURS, MINUTES, SECONDS ) )