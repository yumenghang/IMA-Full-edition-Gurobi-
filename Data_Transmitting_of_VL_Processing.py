import VL_Optimization_of_VL_Processing
import gc
import math

class DATA_TRANSMITTING_OF_VL_PROCESSING():
    def __init__(self,
                 INDICATOR,
                 SIZE,
                 DELAY,
                 PERIOD,
                 MESSAGES_GUID,
                 LOGICAL_DESTINATION,
                 PHYSICAL_DESTINATION,
                 DELAY_BOUND,
                 DELAY_OCCURRED,
                 MESSAGES_TYPE,
                 NET_TYPE,
                 UPPER_LIMIT_OF_THE_NUMBER_OF_MESSAGES,
                 AVERAGE_NUMBER_OF_MESSAGES
                 ):
        self.INDICATOR = INDICATOR
        self.SIZE = SIZE
        self.DELAY = DELAY
        self.PERIOD = PERIOD
        self.MESSAGES_GUID = MESSAGES_GUID
        self.LOGICAL_DESTINATION = LOGICAL_DESTINATION
        self.PHYSICAL_DESTINATION = PHYSICAL_DESTINATION
        self.DELAY_BOUND = DELAY_BOUND
        self.DELAY_OCCURRED = DELAY_OCCURRED
        self.MESSAGES_TYPE = MESSAGES_TYPE
        self.NET_TYPE = NET_TYPE
        self.UPPER_LIMIT_OF_THE_NUMBER_OF_MESSAGES = UPPER_LIMIT_OF_THE_NUMBER_OF_MESSAGES
        self.AVERAGE_NUMBER_OF_MESSAGES = AVERAGE_NUMBER_OF_MESSAGES

    def data_transmitting_of_vl_processing(self, GAP, TIMELIMITED, EXPANDED_COEFFICIENT, PHYSICAL_PORT_RATE):
        if self.INDICATOR == 0: # 表示是RDIU设备
            INFORMATION = [self.SIZE, self.DELAY, self.PERIOD, self.MESSAGES_GUID, self.LOGICAL_DESTINATION, self.PHYSICAL_DESTINATION, self.DELAY_BOUND, self.DELAY_OCCURRED]
            VL_OPTIMIZATION_OF_VL_PROCESSING = VL_Optimization_of_VL_Processing.VL_OPTIMIZATION_OF_VL_PROCESSING(INFORMATION, self.MESSAGES_TYPE, self.NET_TYPE)
            try:
                locals()["VL_INFORMATION_OF_" + self.NET_TYPE + "_NET"], bandwidth_cost = VL_OPTIMIZATION_OF_VL_PROCESSING.vl_of_rdiu_with_period(GAP, TIMELIMITED, PHYSICAL_PORT_RATE)
            except AttributeError:
                locals()["VL_INFORMATION_OF_" + self.NET_TYPE + "_NET"], bandwidth_cost = VL_OPTIMIZATION_OF_VL_PROCESSING.vl_of_rdiu_no_period(GAP, TIMELIMITED, PHYSICAL_PORT_RATE)
            del VL_OPTIMIZATION_OF_VL_PROCESSING
            gc.collect()
            return locals()["VL_INFORMATION_OF_" + self.NET_TYPE + "_NET"], bandwidth_cost
        else:
            """
            因为存在某些设备内消息数目过多，求解时间太长的现象
            我们设置UPPER_LIMIT_OF_THE_NUMBER_OF_MESSAGES, AVERAGE_NUMBER_OF_MESSAGES，将消息划分为若干个数目较少的子集进行处理
            当End System内消息数目大于UPPER_LIMIT_OF_THE_NUMBER_OF_MESSAGES时，我们将消息作拆分处理，以缩短求解时间
            具体拆分规则如下：
            假设End System内有N条消息（N >= UPPER_LIMIT_OF_THE_NUMBER_OF_MESSAGES）
            求得M = ceil( N/AVERAGE_NUMBER_OF_MESSAGES )，其中ceil表示向上取整
            每一个消息子集里消息的数目n = ceil( N/M )
            """
            if len(self.SIZE) >= self.UPPER_LIMIT_OF_THE_NUMBER_OF_MESSAGES:
                NUMBER_OF_SUBSET = math.ceil(len( self.SIZE)/self.AVERAGE_NUMBER_OF_MESSAGES)
                NUMBER_OF_MESSAGES_OF_SUBSET = math.ceil(len(self.SIZE)/NUMBER_OF_SUBSET)
            else:
                NUMBER_OF_SUBSET = 1
                NUMBER_OF_MESSAGES_OF_SUBSET = len(self.SIZE)

            TOTAL_VL_INFORMATION, TOTAL_BANDWIDTH = [], 0
            for subset_index in range(NUMBER_OF_SUBSET):
                if subset_index+1 == NUMBER_OF_SUBSET:
                    INFORMATION = [self.SIZE[NUMBER_OF_MESSAGES_OF_SUBSET*subset_index:],
                                   self.DELAY[NUMBER_OF_MESSAGES_OF_SUBSET*subset_index:],
                                   self.PERIOD[NUMBER_OF_MESSAGES_OF_SUBSET*subset_index:],
                                   self.MESSAGES_GUID[NUMBER_OF_MESSAGES_OF_SUBSET*subset_index:],
                                   self.LOGICAL_DESTINATION[NUMBER_OF_MESSAGES_OF_SUBSET*subset_index:],
                                   self.PHYSICAL_DESTINATION[NUMBER_OF_MESSAGES_OF_SUBSET*subset_index:],
                                   self.DELAY_BOUND[NUMBER_OF_MESSAGES_OF_SUBSET*subset_index:],
                                   self.DELAY_OCCURRED[NUMBER_OF_MESSAGES_OF_SUBSET*subset_index:]
                                  ]
                else:
                    INFORMATION = [self.SIZE[NUMBER_OF_MESSAGES_OF_SUBSET*subset_index : NUMBER_OF_MESSAGES_OF_SUBSET*(subset_index+1)],
                                   self.DELAY[NUMBER_OF_MESSAGES_OF_SUBSET*subset_index : NUMBER_OF_MESSAGES_OF_SUBSET*(subset_index+1)],
                                   self.PERIOD[NUMBER_OF_MESSAGES_OF_SUBSET*subset_index : NUMBER_OF_MESSAGES_OF_SUBSET*(subset_index+1)],
                                   self.MESSAGES_GUID[NUMBER_OF_MESSAGES_OF_SUBSET*subset_index : NUMBER_OF_MESSAGES_OF_SUBSET*(subset_index+1)],
                                   self.LOGICAL_DESTINATION[NUMBER_OF_MESSAGES_OF_SUBSET*subset_index : NUMBER_OF_MESSAGES_OF_SUBSET*(subset_index+1)],
                                   self.PHYSICAL_DESTINATION[NUMBER_OF_MESSAGES_OF_SUBSET*subset_index : NUMBER_OF_MESSAGES_OF_SUBSET*(subset_index+1)],
                                   self.DELAY_BOUND[NUMBER_OF_MESSAGES_OF_SUBSET*subset_index : NUMBER_OF_MESSAGES_OF_SUBSET*(subset_index+1)],
                                   self.DELAY_OCCURRED[NUMBER_OF_MESSAGES_OF_SUBSET*subset_index : NUMBER_OF_MESSAGES_OF_SUBSET*(subset_index+1)]
                                  ]
                VL_OPTIMIZATION_OF_VL_PROCESSING = VL_Optimization_of_VL_Processing.VL_OPTIMIZATION_OF_VL_PROCESSING(INFORMATION, self.MESSAGES_TYPE, self.NET_TYPE)
                try:
                    VL_INFORMATION, bandwidth_cost = VL_OPTIMIZATION_OF_VL_PROCESSING.vl_of_end_system(GAP, TIMELIMITED, PHYSICAL_PORT_RATE)
                except AttributeError:
                    print("*" * 20, "求解时间上限太短，需要进一步延长求解时间", "*" * 20)
                    timelimited = TIMELIMITED * EXPANDED_COEFFICIENT
                    VL_INFORMATION, bandwidth_cost = VL_OPTIMIZATION_OF_VL_PROCESSING.vl_of_end_system(GAP, timelimited, PHYSICAL_PORT_RATE)
                if TOTAL_VL_INFORMATION == []:
                    TOTAL_VL_INFORMATION = VL_INFORMATION
                    TOTAL_BANDWIDTH = bandwidth_cost
                else:
                    TOTAL_VL_INFORMATION += VL_INFORMATION
                    TOTAL_BANDWIDTH += bandwidth_cost
            return TOTAL_VL_INFORMATION, TOTAL_BANDWIDTH