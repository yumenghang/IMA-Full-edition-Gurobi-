help_information = \
    "python Main -h, --help, --Data_Processing, --VL_Processing, --topology_type, --Routes_Optimization, --task, --net_type, --Routes_Path_Processing \n" \
    "-h: Print help information. \n" \
    "--help: Print help information. \n" \
    "--Data_Processing=(True, False): Whether to process the raw data and get the intermediate data. \n" \
    "--VL_Processing=(True, False): Whether to divide the messages into virtual links. \n" \
    "--topology_type=(ARINC664, AFDX): The type of network topology. \n" \
    "--Routes_Optimization=(True, False): Whether to optimize the routes of virtual links. \n" \
    "--task=(usage, usage_and_loading): The type of task. \n" \
    "--net_type=(A, B): The type of network. \n" \
    "--Routes_Path_Processing=(True, False): Whether to find the routes of messages. \n"
delta = 47 # 帧头大小

# 原始数据处理过程中需要的超参数
root_path = "./Data Info/" # 原始数据的存放路径
intermediate_data_file = "./Intermediate data file/" # 原始数据处理后得到的中间过程数据文件的存放路径
can_message_size = 8
arinc429_message_size = 4
analog_message_size = 2
system_latency_upper_limit = 300000

# 将消息划分到虚链路以及虚链路参数优化过程中需要的超参数
vl_dict_file = "./Intermediate VL dict File/" # 原始数据处理后得到的中间过程数据文件的存放路径
allocated_rate_coefficient = 0.5 # RDIU设备既有ARINC664消息，也有非ARINC664消息。因此，对于RDIU设备，将物理端口的带宽分别分配给非ARINC664消息以及ARINC664消息
gap_for_vl_optimization = None  # 设置求解gap，即：精度
time_limited_for_vl_optimization = 300  # 设置求解时间上限，600s为一个单位
expanded_coefficient = 5  # 设置当单位求解时间上限（600s)不足以得到解时，求解时间的扩大系数
upper_limit_of_the_number_of_messages = 25 # 当End System内消息数目大于upper_limit_of_the_number_of_messages时，我们将消息作拆分处理，以缩短求解时间
average_number_of_messages = 9 # average_number_of_messages为拆分后，每一个消息子集中消息的数目的上限

# 寻找路由过程中需要的超参数
routes_file = "./Intermediate routes file/" # 返回的各条虚拟链路的路由（包括：TOTAL_X_FOR_RETURN, TOTAL_Y_FOR_RETURN）的存储路径
min_latency = 1e+6
average_number_of_vl = 50 # 平均每次求解数目为AVERAGE_NUMBER_OF_VL的虚链路的路径
gap_for_routes_optimization = 0.01 # 设置求解精度
time_limited_for_routes_optimization = None # 设置求解时间上限
upper_bound = 100000

# 建立消息的路由记录的过程中的超参数
messages_routes_file = "./Messages routes file/" # 消息的路由记录的存储路径
gap_for_routes_path_processing = None # 设置求解精度
time_limited_for_routes_path_processing = None # 设置求解时间上限