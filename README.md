# 1  IMA-Full edition (Gurobi)

## 1.1  使用
__python__ __Main.py__ __-h__ __--help__ __--Data_Processing=[True, False]__ __--VL_Processing=[True, False]__ __--Round_BAG_of_Virtual_Links=[True, False]__ __--topology_type=[ARINC664, AFDX]__ __--Routes_Optimization[True, False]=__ __--task=[minimum_usage_of_bandwidth, minimum_and_balanced_usage_of_bandwidth, minimum_delay, minimum_and_balanced_delay, multi_tasks]__ __--net_type=[A, B]__ __--Routes_Path_Processing=[True, False]__ __--Verify_Transmitting_Path=[True, False]__ __--Verify_Bandwidth_Usage=[True, False]__ __--Generate_XML_File=[True, False]__ __--Comparison_of_ARINC664=[True, False]__ __--Comparison_of_AFDX=[True, False]__\ __--Shortest_path=[True, False]__\
__-h__: 无需参数值，打印程序help信息；\
__--help__: 无需参数值，打印程序help信息；

__--pology_type__: 网络拓扑类型，取值：ARINC664或AFDX，表示消息的处理范围是在ARINC664网络拓扑中还是在AFDX网络拓扑中；\
__--task__: 任务类型，取值：minimum_usage_of_bandwidth, minimum_and_balanced_usage_of_bandwidth, minimum_delay, minimum_and_balanced_delay, multi_tasks，表示优化虚拟链路的优化目标，包括：最高带宽余量、最高带宽余量且负载最均衡、最低传输延迟、最低传输延迟且延迟分布最均衡、兼顾低传输延迟、高带宽余量和网络均衡。这里：\
minimum_delay --> 获取最低传输延迟的路由；\
minimum_and_balanced_delay --> 获取最低传输延迟且延迟分布最均衡的路由；\
minimum_usage_of_bandwidth --> 获取最高带宽余量的路由；\
minimum_and_balanced_usage_of_bandwidth --> 获取最高带宽余量且负载最均衡的路由；\
multi_tasks --> 获取兼顾低传输延迟、高带宽余量和网络均衡的路由。\
__--net_type__: 网络属性，取值：A或B，表示A网或B网；

__--Data_Processing__: 参数取值True或False，表示是否处理原始数据。原始数据的处理结果存储在同一路径下的"./Intermediate data file/"文件夹中（注：此功能不需要：opology_type、task、net_type参数）；\
__--VL_Processing__: 参数取值True或者False，表示是否将消息以虚链路为单位进行划分。消息划分后得到的虚链路以字典的形式存储在同一路径下的"./Intermediate VL dict file/"文件夹中（注：此功能需要：topology_type参数）；\
__--Round_BAG_of_Virtual_Links__: 参数取值True或False，表示是否对上一步得到的VL dict中BAG的取值进行处理。这里主要原因是：求解器直接返回的BAG的取值并非严格的0.5的整数倍，而有可能取诸如.49999999999、.99999999之类的数值，因此需要对VL dict中BAG的取值进行处理，以使其为严格的0.5的整数倍（注：此功能不需要：opology_type、task、net_type参数）；\
__--Routes_Optimization__: 参数取值True或者False，表示是否对虚链路的路由进行优化。虚链路路由的优化结果得到后，包括一些中间数据，均存储在同一路径下的"./Intermediate routes file/"文件夹中（注：此功能需要：topology_type参数、task参数以及net_type参数）；\
__--Routes_Path_Processing__: 参数取值True或者False，表示是否根据得到的虚链路的路由，回溯消息的传输路径（注：此功能需要topology_type参数、task参数以及net_type参数）；\
__--Verify_Transmitting_Path__: 参数取值True或者False，表示验证回溯得到的消息的传输路径的正确性（注：验证文件夹："./Messages routes file/"下所有的Messages dict文件，此功能不需要：opology_type、task、net_type参数）；\
__--Verify_Bandwidth_Usage__: 参数取值True或者False，表示借助Routes_Path_Processing功能保留的路由信息，验证虚拟链路的带宽占用是否满足实际的物理链路带宽情况（注：此功能需要topology_type参数、task参数以及net_type参数）；\
__--Generate_XML_File__: 参数取值True或者False，表示生成与网络拓扑、任务相对应的VirtualLinks.xml文件，得到的VirtualLinks.xml文件存储在同一路径下的"./xml_file/"文件夹中（注：此时需要额外的参数：topology_type以及task）；\
__--Comparison_of_ARINC664__: 参数取值True或者False，表示：\
借助SwitchNetConfigOutput_baeline.xml, VirtualLinks_baseline.xml, switchNetConfigOutput_optimized.xml, VirtualLinks_optimized.xml四个文件，对比ARINC664网络拓扑中，两种方案的带宽情况、时延情况；\
（注：此时需要额外的参数：task）。
__Comparison_of_AFDX__: 参数取值True或者False，表示：\
借助"./SwitchNetConfigOutput/IMA Network Configuration/VL Architecture/RGW01_NonA664.xml~RGW16_NonA664.xml", "./SwitchNetConfigOutput/VirtualLinks_baseline.xml"以及"./Intermediate VL dict file/VL_DICT_OF_A_NET_OF_AFDX, VL_DICT_OF_B_NET_OF_AFDX, VL_DICT_OF_A_NET_OF_ARINC664, VL_DICT_OF_B_NET_OF_ARINC664"，对比AFDX网络拓扑中，两种方案下，RDIU设备物理端口的带宽占用、虚拟链路数目以及路由的跳数对比。
（注：此时需要额外的参数：task）；\
__--Shortest_path__:参数取值True或者False，表示求得ARINC664或AFDX网络拓扑下，各条消息的最短路径路由，并返回对应网络拓扑下，A网、B网以及全网消息的总跳数（注：此功能需要：topology_type参数）。


### 1.1.1  功能模块：
1、打印help信息；\
2、原始数据文件处理；\
3、消息分配及虚链路优化处理；\
4、虚拟链路BAG参数值处理；\
5、虚拟链路路由优化；\
6、消息传输路径回溯；\
7、验证消息传输路径的正确性；\
8、验证虚拟链路的带宽占用是否满足实际的物理链路带宽情况；\
9、生成用于测试的VirtualLinks.xml文件；\
10、对比ARINC664网络拓扑中baseline与optimized两种方案下路由的性能；\
11、对比AFDX网络拓扑中baseline与optimized两种方案下路由的性能；\
12、返回ARINC664或AFDX网络拓扑下，A网、B网以及全网消息的总跳数。

### 1.1.2  命令
__1、打印help信息：__\
python Main.py -h\
或者\
python Main.py --help

__2、处理原始数据文件：__\
python Main.py --Data_Processing=True

__3、优化处理消息分配及虚链路：__\
python Main.py --VL_Processing=True --topology_type=AFDX\
或者\
python Main.py --VL_Processing=True --topology_type=ARINC664

__4、虚拟链路BAG参数值处理：__\
python Main.py --Round_BAG_of_Virtual_Links=True

__5、优化虚链路路由：__\
python Main.py --Routes_Optimization=True --topology_type=AFDX --task=minimum_usage_of_bandwidth --net_type=A\
或者\
python Main.py --Routes_Optimization=True --topology_type=AFDX --task=minimum_usage_of_bandwidth --net_type=B\
或者\
python Main.py --Routes_Optimization=True --topology_type=AFDX --task=minimum_and_balanced_usage_of_bandwidth --net_type=A\
或者\
python Main.py --Routes_Optimization=True --topology_type=AFDX --task=minimum_and_balanced_usage_of_bandwidth --net_type=B\
或者\
python Main.py --Routes_Optimization=True --topology_type=AFDX --task=minimum_delay --net_type=A\
或者\
python Main.py --Routes_Optimization=True --topology_type=AFDX --task=minimum_delay --net_type=B\
或者\
python Main.py --Routes_Optimization=True --topology_type=AFDX --task=minimum_and_balanced_delay --net_type=A\
或者\
python Main.py --Routes_Optimization=True --topology_type=AFDX --task=minimum_and_balanced_delay --net_type=B\
或者\
python Main.py --Routes_Optimization=True --topology_type=ARINC664 --task=minimum_usage_of_bandwidth --net_type=A\
或者\
python Main.py --Routes_Optimization=True --topology_type=ARINC664 --task=minimum_usage_of_bandwidth --net_type=B\
或者\
python Main.py --Routes_Optimization=True --topology_type=ARINC664 --task=minimum_and_balanced_usage_of_bandwidth --net_type=A\
或者\
python Main.py --Routes_Optimization=True --topology_type=ARINC664 --task=minimum_and_balanced_usage_of_bandwidth --net_type=B\
或者\
python Main.py --Routes_Optimization=True --topology_type=ARINC664 --task=minimum_delay --net_type=A\
或者\
python Main.py --Routes_Optimization=True --topology_type=ARINC664 --task=minimum_delay --net_type=B\
或者\
python Main.py --Routes_Optimization=True --topology_type=ARINC664 --task=minimum_and_balanced_delay --net_type=A\
或者\
python Main.py --Routes_Optimization=True --topology_type=ARINC664 --task=minimum_and_balanced_delay --net_type=B

__6、回溯消息传输路径：__\
python Main.py --Routes_Path_Processing=True --topology_type=AFDX --task=minimum_usage_of_bandwidth --net_type=A\
或者\
python Main.py --Routes_Path_Processing=True --topology_type=AFDX --task=minimum_usage_of_bandwidth --net_type=B\
或者\
python Main.py --Routes_Path_Processing=True --topology_type=AFDX --task=minimum_and_balanced_usage_of_bandwidth --net_type=A\
或者\
python Main.py --Routes_Path_Processing=True --topology_type=AFDX --task=minimum_and_balanced_usage_of_bandwidth --net_type=B\
或者\
python Main.py --Routes_Path_Processing=True --topology_type=AFDX --task=minimum_delay --net_type=A\
或者\
python Main.py --Routes_Path_Processing=True --topology_type=AFDX --task=minimum_delay --net_type=B\
或者\
python Main.py --Routes_Path_Processing=True --topology_type=AFDX --task=minimum_and_balanced_delay --net_type=A\
或者\
python Main.py --Routes_Path_Processing=True --topology_type=AFDX --task=minimum_and_balanced_delay --net_type=B\
或者\
python Main.py --Routes_Path_Processing=True --topology_type=ARINC664 --task=minimum_usage_of_bandwidth --net_type=A\
或者\
python Main.py --Routes_Path_Processing=True --topology_type=ARINC664 --task=minimum_usage_of_bandwidth --net_type=B\
或者\
python Main.py --Routes_Path_Processing=True --topology_type=ARINC664 --task=minimum_and_balanced_usage_of_bandwidth --net_type=A\
或者\
python Main.py --Routes_Path_Processing=True --topology_type=ARINC664 --task=minimum_and_balanced_usage_of_bandwidth --net_type=B\
或者\
python Main.py --Routes_Path_Processing=True --topology_type=ARINC664 --task=minimum_delay --net_type=A\
或者\
python Main.py --Routes_Path_Processing=True --topology_type=ARINC664 --task=minimum_delay --net_type=B\
或者\
python Main.py --Routes_Path_Processing=True --topology_type=ARINC664 --task=minimum_and_balanced_delay --net_type=A\
或者\
python Main.py --Routes_Path_Processing=True --topology_type=ARINC664 --task=minimum_and_balanced_delay --net_type=B

__7、验证消息传输路径的正确性：__\
python Main.py --Verify_Transmitting_Path=True

__8、验证虚拟链路的带宽占用是否满足实际的物理链路带宽情况：__\
python Main.py --Verify_Bandwidth_Usage=True --topology_type=AFDX --task=minimum_usage_of_bandwidth --net_type=A\
或者\
python Main.py --Verify_Bandwidth_Usage=True --topology_type=AFDX --task=minimum_usage_of_bandwidth --net_type=B\
或者\
python Main.py --Verify_Bandwidth_Usage=True --topology_type=AFDX --task=minimum_and_balanced_usage_of_bandwidth --net_type=A\
或者\
python Main.py --Verify_Bandwidth_Usage=True --topology_type=AFDX --task=minimum_and_balanced_usage_of_bandwidth --net_type=B\
或者\
python Main.py --Verify_Bandwidth_Usage=True --topology_type=AFDX --task=minimum_delay --net_type=A\
或者\
python Main.py --Verify_Bandwidth_Usage=True --topology_type=AFDX --task=minimum_delay --net_type=B\
或者\
python Main.py --Verify_Bandwidth_Usage=True --topology_type=AFDX --task=minimum_and_balanced_delay --net_type=A\
或者\
python Main.py --Verify_Bandwidth_Usage=True --topology_type=AFDX --task=minimum_and_balanced_delay --net_type=B\
或者\
python Main.py --Verify_Bandwidth_Usage=True --topology_type=ARINC664 --task=minimum_usage_of_bandwidth --net_type=A\
或者\
python Main.py --Verify_Bandwidth_Usage=True --topology_type=ARINC664 --task=minimum_usage_of_bandwidth --net_type=B\
或者\
python Main.py --Verify_Bandwidth_Usage=True --topology_type=ARINC664 --task=minimum_and_balanced_usage_of_bandwidth --net_type=A\
或者\
python Main.py --Verify_Bandwidth_Usage=True --topology_type=ARINC664 --task=minimum_and_balanced_usage_of_bandwidth --net_type=B\
或者\
python Main.py --Verify_Bandwidth_Usage=True --topology_type=ARINC664 --task=minimum_delay --net_type=A\
或者\
python Main.py --Verify_Bandwidth_Usage=True --topology_type=ARINC664 --task=minimum_delay --net_type=B\
或者\
python Main.py --Verify_Bandwidth_Usage=True --topology_type=ARINC664 --task=minimum_and_balanced_delay --net_type=A\
或者\
python Main.py --Verify_Bandwidth_Usage=True --topology_type=ARINC664 --task=minimum_and_balanced_delay --net_type=B

__9、生成用于测试的VirtualLinks.xml文件：__\
python Main.py --Generate_XML_File=True --topology_type=AFDX --task=minimum_usage_of_bandwidth\
或者\
python Main.py --Generate_XML_File=True --topology_type=AFDX --task=minimum_and_balanced_usage_of_bandwidth\
或者\
python Main.py --Generate_XML_File=True --topology_type=AFDX --task=minimum_delay\
或者\
python Main.py --Generate_XML_File=True --topology_type=AFDX --task=minimum_and_balanced_delay\
或者\
python Main.py --Generate_XML_File=True --topology_type=ARINC664 --task=minimum_usage_of_bandwidth\
或者\
python Main.py --Generate_XML_File=True --topology_type=ARINC664 --task=minimum_and_balanced_usage_of_bandwidth\
或者\
python Main.py --Generate_XML_File=True --topology_type=ARINC664 --task=minimum_delay\
或者\
python Main.py --Generate_XML_File=True --topology_type=ARINC664 --task=minimum_and_balanced_delay

__10、对比ARINC664网络拓扑下baseline与optimized两种方案下路由的性能：__\
python Main.py --Comparison_of_ARINC664=True --task=minimum_usage_of_bandwidth\
或者\
python Main.py --Comparison_of_ARINC664=True --task=minimum_and_balanced_usage_of_bandwidth\
或者\
python Main.py --Comparison_of_ARINC664=True --task=minimum_delay\
或者\
python Main.py --Comparison_of_ARINC664=True --task=minimum_and_balanced_delay

__11、对比AFDX网络拓扑下baseline与optimized两种方案下路由的性能：__\
python Main.py --Comparison_of_AFDX=True --task=minimum_usage_of_bandwidth\
或者\
python Main.py --Comparison_of_AFDX=True --task=minimum_and_balanced_usage_of_bandwidth\
或者\
python Main.py --Comparison_of_AFDX=True --task=minimum_delay\
或者\
python Main.py --Comparison_of_AFDX=True --task=minimum_and_balanced_delay

__12、返回ARINC664或AFDX网络拓扑下，A网、B网以及全网消息的总跳数：__\
python Main.py --Shortest_path=True --topology_type=ARINC664\
或者\
python Main.py --Shortest_path=True --topology_type=AFDX

## 1.2  中间过程文件下载
因为中间过程文件占据存储空间较大，所以以交大云盘的形式进行共享，下面是链接，以供下载使用：\
https://jbox.sjtu.edu.cn/l/Q1PqGI \
注：中间过程文件如有更新，会第一时间替换更新掉云端文件。

## 1.3  中间过程文件介绍

### 1.3.1  Intermediate data file

#### 1.3.1.1  physical_ports_information
键（key）：物理端口的全称，表示为：physical port full name。形式为：物理端口所属物理设备+"."+物理端口名，如物理设备IDURIGHTOUTBOARD上的A端口--IDURIGHTOUTBOARD.A，或物理端口所属机柜+"."+物理端口所属设备+"."+物理端口名，如机柜CCR_LEFT中物理设备GPM_L6上的A端口--CCR_LEFT.GPM_L6.A\
值（value）：为一列表，按以下格式存储对应物理端口的相关信息：\
&emsp;&emsp;[\
&emsp;&emsp;&emsp;&emsp;物理端口类型, #0，包括：AswPhysPort, AesPhysPort, CANPhysPort, AnalogPhysPort, A429PhysPort, PwrPhysPort\
&emsp;&emsp;&emsp;&emsp;物理端口标识符, #1\
&emsp;&emsp;&emsp;&emsp;physical port full name, #2\
&emsp;&emsp;&emsp;&emsp;NameDef, #3\
&emsp;&emsp;&emsp;&emsp;GuidDef, #4\
&emsp;&emsp;&emsp;&emsp;物理端口方向, #5 表示该物理端口是用于发送消息、接收消息还是同时发送与接收消息（注：ARINC-664与CAN协议的物理端口为双工，ARINC-429与Analog协议的物理端口为单工）\
&emsp;&emsp;&emsp;&emsp;该物理端口所在物理设备名称, #6\
&emsp;&emsp;&emsp;&emsp;该物理端口的传输速率（单位：MB/s）, #7\
&emsp;&emsp;]

#### 1.3.1.2  physical_ports_adjacent_matrix
记录物理端口（除电源接口外的所有物理端口）之间的连接关系

#### 1.3.1.3  physical_ports_index
键（key）：物理端口的全称，physical port full name，如：CCR_LEFT.GPM_L6.A\
值（value）：该物理端口在邻接矩阵physical_ports_adjacent_matrix中的index

#### 1.3.1.4  physical_ports_index_reversed
键（key）：物理端口在邻接矩阵physical_ports_adjacent_matrix中的index\
值（value）：物理端口的全称，physical port full name

#### 1.3.1.5  switches_information
键（key）：交换机的标识符\
值（value）：为一列表，按以下格式存储对应交换机的相关信息：\
&emsp;&emsp;[\
&emsp;&emsp;&emsp;&emsp;交换机名称(注：一共有8台交换机，分别是：ARS_1A、ARS_2A、ARS_1B、ARS_2B、CCR_LEFT.ACS_LA、CCR_RIGHT.ACS_RA、CCR_LEFT.ACS_LB、CCR_RIGHT.ACS_RB), #0\
&emsp;&emsp;&emsp;&emsp;NameDef, #1\
&emsp;&emsp;&emsp;&emsp;GuidDef, #2\
&emsp;&emsp;&emsp;&emsp;[ physical port full name, ..., physical port full name  ], #3 （注：交换机内除电源接口外，共25个ARINC-664协议的物理端口）\
&emsp;&emsp;]

#### 1.3.1.6  RDIU_information
键（key）：RDIU名称(注：一共有16台交换机，分别是：RDIU_01、RDIU_02、RDIU_03、RDIU_04、RDIU_05、RDIU_06、RDIU_07、RDIU_08、RDIU_09、RDIU_10、RDIU_11、RDIU_12、RDIU_13、RDIU_14、RDIU_15、RDIU_16)\
值（value）：为一列表，按以下格式存储对应RDIU的相关信息：\
&emsp;&emsp;[\
&emsp;&emsp;&emsp;&emsp;RDIU名称, #0\
&emsp;&emsp;&emsp;&emsp;RDIU标识符, #1\
&emsp;&emsp;&emsp;&emsp;NameDef, #2\
&emsp;&emsp;&emsp;&emsp;GuidDef, #3\
&emsp;&emsp;&emsp;&emsp;[ physical port full name, ..., physical port full name ], #4\
&emsp;&emsp;]

#### 1.3.1.7  messages_info
键（key）：消息（包括：ARINC-664消息、ARINC-429消息、CAN消息、Analog消息）的标识符\
值（value）：为一列表，按以下格式存储对应消息的相关信息：\
&emsp;&emsp;[\
&emsp;&emsp;&emsp;&emsp;发送端消息的类型, #0\
&emsp;&emsp;&emsp;&emsp;发送端消息的大小, #1\
&emsp;&emsp;&emsp;&emsp;发送端消息的名称, #2\
&emsp;&emsp;&emsp;&emsp;发送端消息所在的物理设备名称, #3\
&emsp;&emsp;&emsp;&emsp;发送端的物理端口名称, #4\
&emsp;&emsp;&emsp;&emsp;发送端的逻辑端口标识符, #5\
&emsp;&emsp;&emsp;&emsp;发送端逻辑端口名称, #6\
&emsp;&emsp;&emsp;&emsp;发送端的消息发送周期, #7\
&emsp;&emsp;&emsp;&emsp;[接收端逻辑端口名称], #8 这一项用于在消息合并过程中判断消息的接收端是否被重复加入\
&emsp;&emsp;&emsp;&emsp;[\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;[接收端消息的类型, 接收端消息的大小, 接收端对消息的延迟要求, 接收端所在的物理设备名称, 接收端的物理端口名称（注：这里为一列表，针对ARINC-664消息可能从同一物理设备的A、B两个端口进行接收，然后再传输至相应逻辑端口）, 接收端的逻辑端口标识符, 接收端的逻辑端口名称],\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;... ...\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;[接收端消息的类型, 接收端消息的大小, 接收端对消息的延迟要求, 接收端所在的物理设备名称, 接收端的物理端口名称（注：这里为一列表，针对ARINC-664消息可能从同一物理设备的A、B两个端口进行接收，然后再传输至相应逻辑端口）, 接收端的逻辑端口标识符, 接收端的逻辑端口名称]\
&emsp;&emsp;&emsp;&emsp;] #9\
&emsp;&emsp;]

#### 1.3.1.8  messages_per_physical_port
键（key）：物理端口的全称，表示为：physical port full name。形式为：物理端口所属物理设备+"."+物理端口名，如物理设备IDURIGHTOUTBOARD上的A端口--IDURIGHTOUTBOARD.A，或物理端口所属机柜+"."+物理端口所属设备+"."+物理端口名，如机柜CCR_LEFT中物理设备GPM_L6上的A端口--CCR_LEFT.GPM_L6.A\
值（value）：为一列表，按以下格式存储对应物理端口的相关信息：\
&emsp;&emsp;[\
&emsp;&emsp;&emsp;&emsp;物理端口的全称, #0\
&emsp;&emsp;&emsp;&emsp;消息类型, #1，为一列表，包括：A664, CAN, A429, Analog\
&emsp;&emsp;&emsp;&emsp;消息大小, #2，为一列表，单位：Byte\
&emsp;&emsp;&emsp;&emsp;消息的系统延迟要求, #3，为一列表，单位：ms\
&emsp;&emsp;&emsp;&emsp;消息的发送周期, #4，为一列表，单位：ms\
&emsp;&emsp;&emsp;&emsp;消息的标识符, #5，为一列表\
&emsp;&emsp;&emsp;&emsp;消息的目的节点的逻辑端口, #6，因为同一消息可以被发送至多个目的节点，因此每一个消息的目的节点的逻辑端口是一个列表，因此此项是列表的列表，格式为：
[ [ logical_port_1, logical_port_2, ..., logical_port_m ], ... , [ logical_port_1, logical_port_2, ..., logical_port_n ] ]\
&emsp;&emsp;&emsp;&emsp;消息的目的节点的物理端口, #7，因为同一消息可以被发送至多个目的节点，而每一个目的节点的消息可能经由A、B两个端口同时转发，因此每一个消息的目的节点的物理端口是一个列表的列表，因此此项是列表的列表的列表，格式为：
[ [ [ physical_port_A, physical_port_B ], ... , [ physical_port_A, physical_port_B ] ], ..., [ [ physical_port_A ], ..., [ physical_port_B ] ] ]\
&emsp;&emsp;]


#### 1.3.1.9  arinc664_physical_ports_adjacent_matrix_for_A_NET
记录A网中ARINC-664协议物理端口之间的连接关系

#### 1.3.1.10  arinc664_physical_ports_index_for_A_NET
键（key）：A网中ARINC-664协议物理端口的全称，physical port full name，如：CCR_LEFT.GPM_L6.A\
值（value）：该物理端口在邻接矩阵arinc664_physical_ports_adjacent_matrix_for_A_NET中的index

#### 1.3.1.11  arinc664_physical_ports_index_reversed_for_A_NET
键（key）：A网中ARINC-664协议物理端口在邻接矩阵arinc664_physical_ports_adjacent_matrix_for_A_NET中的index\
值（value）：物理端口的全称，physical port full name

#### 1.3.1.12  arinc664_physical_ports_adjacent_matrix_for_B_NET
记录B网中ARINC-664协议物理端口之间的连接关系

#### 1.3.1.13  arinc664_physical_ports_index_for_B_NET
键（key）：B网中ARINC-664协议物理端口的全称，physical port full name，如：CCR_LEFT.GPM_L6.B\
值（value）：该物理端口在邻接矩阵arinc664_physical_ports_adjacent_matrix_for_B_NET中的index

#### 1.3.1.14  arinc664_physical_ports_index_reversed_for_B_NET
键（key）：B网中ARINC-664协议物理端口在邻接矩阵arinc664_physical_ports_adjacent_matrix_for_B_NET中的index\
值（value）：物理端口的全称，physical port full name

### 1.3.2  Intermediate VL dict file

#### 1.3.2.1  VL_DICT_OF_A_NET_OF_AFDX、VL_DICT_OF_A_NET_OF_ARINC664、VL_DICT_OF_B_NET_OF_AFDX、VL_DICT_OF_B_NET_OF_ARINC664
其中，AFDX与ARINC664表示网络拓扑类型；A、B表示网络类型（A网或B网）。\
键（key）：ARINC664协议的物理端口--messages_per_physical_port，包括：\
RDIU_01.A, RDIU_01.B, RDIU_02.A, RDIU_02.B, RDIU_03.A, RDIU_03.B, RDIU_04.A, RDIU_04.B, RDIU_05.A, RDIU_05.B,\
RDIU_06.A, RDIU_06.B, RDIU_07.A, RDIU_07.B, RDIU_08.A, RDIU_08.B, RDIU_09.A, RDIU_09.B, RDIU_10.A, RDIU_10.B,\
RDIU_11.A, RDIU_11.B, RDIU_12.A, RDIU_12.B, RDIU_13.A, RDIU_13.B, RDIU_14.A, RDIU_14.B, RDIU_15.A, RDIU_15.B,\
RDIU_16.A, RDIU_16.B, CCR_LEFT.GPM_L6.A, CCR_LEFT.GPM_L6.B, FCM_1.A, FCM_1.B, CCR_LEFT.GPM_L4.A, CCR_LEFT.GPM_L4.B,\
ADEC_L_CHA.A, FADEC_L_CHA.B, CCR_LEFT.GPM_L1.A, CCR_LEFT.GPM_L1.B, IDULEFTINBOARD.A, IDULEFTINBOARD.B,\
IDURIGHTINBOARD.A, IDURIGHTINBOARD.B, IDUCENTER.A, IDUCENTER.B, CCR_RIGHT.GPM_R1.A, CCR_RIGHT.GPM_R1.B,\
CCR_RIGHT.GPM_R5.A, 'CCR_RIGHT.GPM_R5.B, FADEC_R_CHA.A, FADEC_R_CHA.B, CCR_RIGHT.GPM_R3.A, CCR_RIGHT.GPM_R3.B,\
L_RPDU_A.A, L_RPDU_A.B, L_RPDU_B.A, L_RPDU_B.B, R_RPDU_A.A, R_RPDU_A.B, R_RPDU_B.A, R_RPDU_B.B, CCR_RIGHT.GPM_R6.A,\
CCR_RIGHT.GPM_R6.B, IDULEFTOUTBOARD.A, IDULEFTOUTBOARD.B, IDURIGHTOUTBOARD.A, IDURIGHTOUTBOARD.B,\
HARDWARE_AHMUINSTANCE.A, 'HARDWARE_AHMUINSTANCE.B, CCR_LEFT.GPM_L2.A, CCR_LEFT.GPM_L2.B, CCR_LEFT.GPM_L5.A,\
CCR_LEFT.GPM_L5.B, CCR_RIGHT.GPM_R4.A, CCR_RIGHT.GPM_R4.B, CCR_LEFT.GPM_L3.A, CCR_LEFT.GPM_L3.B,\
CCR_RIGHT.GPM_R2.A, CCR_RIGHT.GPM_R2.B, FCM_2.A, FCM_2.B, FCM_3.A, FCM_3.B, FADEC_L_CHB.A, FADEC_L_CHB.B,\
FADEC_R_CHB.A, FADEC_R_CHB.B, ISS_R.A, ISS_R.B, ISS_L.A, ISS_L.B, FWDEAFR.A, FWDEAFR.B, AFTEAFR.A, AFTEAFR.B,\
SYSTEST_PORT_LRU.A, SYSTEST_PORT_LRU.B, CCR_LEFT.ACS_LA.A, ARS_1B.B, ARS_2A.A, ARS_2B.B, CCR_LEFT.ACS_LB.B,\
ARS_1A.A, CCR_RIGHT.ACS_RA.A, CCR_RIGHT.ACS_RB.B\
值（value）：以该ARINC664协议的物理端口为转发端口的虚拟链路，为一列表，分别存储以下信息：
&emsp;&emsp;[\
&emsp;&emsp;&emsp;&emsp;[ BAG, MTU, BandWidth, [ [ message_guid of subVL0, ... ], [ message_guid of subVL1, ... ], [ message_guid of subVL2, ... ], [ message_guid of subVL3, ... ] ], [ [ logical_destination of subVL0, ... ], [ logical_destination of subVL1, ... ], [ logical_destination of subVL2, ... ], [ logical_destination of subVL3, ... ] ], [ [ physical_destination of subVL0, ... ], [ physical_destination of subVL1, ... ], [ physical_destination of subVL2, ... ], [ physical_destination of subVL3, ... ] ], [ [ delay_bound of subVL0, ... ], [ delay_bound of subVL1, ... ], [ delay_bound of subVL2, ... ], [ delay_bound of subVL3, ... ] ], [ [ delay_occurred of subVL0, ... ], [ delay_occurred of subVL1, ... ], [ delay_occurred of subVL2, ... ], [ delay_occurred of subVL3, ... ] ] ], #虚链路1\
&emsp;&emsp;&emsp;&emsp;[ BAG, MTU, BandWidth, [ [ message_guid of subVL0, ... ], [ message_guid of subVL1, ... ], [ message_guid of subVL2, ... ], [ message_guid of subVL3, ... ] ], [ [ logical_destination of subVL0, ... ], [ logical_destination of subVL1, ... ], [ logical_destination of subVL2, ... ], [ logical_destination of subVL3, ... ] ], [ [ physical_destination of subVL0, ... ], [ physical_destination of subVL1, ... ], [ physical_destination of subVL2, ... ], [ physical_destination of subVL3, ... ] ], [ [ delay_bound of subVL0, ... ], [ delay_bound of subVL1, ... ], [ delay_bound of subVL2, ... ], [ delay_bound of subVL3, ... ] ], [ [ delay_occurred of subVL0, ... ], [ delay_occurred of subVL1, ... ], [ delay_occurred of subVL2, ... ], [ delay_occurred of subVL3, ... ] ] ], #虚链路2\
&emsp;&emsp;&emsp;&emsp;..., #2\
&emsp;&emsp;&emsp;&emsp;[ BAG, MTU, BandWidth, [ [ message_guid of subVL0, ... ], [ message_guid of subVL1, ... ], [ message_guid of subVL2, ... ], [ message_guid of subVL3, ... ] ], [ [ logical_destination of subVL0, ... ], [ logical_destination of subVL1, ... ], [ logical_destination of subVL2, ... ], [ logical_destination of subVL3, ... ] ], [ [ physical_destination of subVL0, ... ], [ physical_destination of subVL1, ... ], [ physical_destination of subVL2, ... ], [ physical_destination of subVL3, ... ] ], [ [ delay_bound of subVL0, ... ], [ delay_bound of subVL1, ... ], [ delay_bound of subVL2, ... ], [ delay_bound of subVL3, ... ] ], [ [ delay_occurred of subVL0, ... ], [ delay_occurred of subVL1, ... ], [ delay_occurred of subVL2, ... ], [ delay_occurred of subVL3, ... ] ] ] #虚链路n\
&emsp;&emsp;]

### 1.3.3  Intermediate Intermediate routes file
根据不同的网络拓扑类型（ARINC664或AFDX）、网络类型（A或B）以及任务类型（usage或usage_and_loading），确定虚链路的转发路由。以下是关于不同网络拓扑类型、网络类型以及任务类型的虚链路转发路由。
#### 1.3.3.1  TOTAL_Y_FOR_RETURN_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_OF_AFDX
#### 1.3.3.2  TOTAL_Y_FOR_RETURN_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_OF_ARINC664
#### 1.3.3.3  TOTAL_Y_FOR_RETURN_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_OF_AFDX
#### 1.3.3.4  TOTAL_Y_FOR_RETURN_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_OF_ARINC664
#### 1.3.3.5  TOTAL_Y_FOR_RETURN_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_OF_AFDX
#### 1.3.3.6  TOTAL_Y_FOR_RETURN_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_OF_ARINC664
#### 1.3.3.7  TOTAL_Y_FOR_RETURN_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_OF_AFDX
#### 1.3.3.8  TOTAL_Y_FOR_RETURN_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_OF_ARINC664
具体格式为：
三维数组
第一维：虚链路index
第二维、第三维：网络类型（A网或B网）中physical port的index，如：
TOTAL_Y_FOR_RETURN_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_OF_AFDX[ VL_index ][ previous port ][ following port ]表示AFDX网络拓扑中、A网下关于最高带宽余量且负载最均衡的路由中，编号为VL_index的虚链路是否由物理链路previous port->following port转发。\
其中，路径"./Intermediate Intermediate routes file/"下包含大量其他存储文件，是用来在下一个程序功能--消息转发路径回溯中，回溯消息的转发路径所需要用到的信息，具体细节这里可以不用过多考虑。

### 1.3.4  Messages routes file
根据上述所有中间过程文件，最终回溯得到并存储不同网络拓扑类型、网络类型以及任务类型下消息的转发路由，共包括以下8个字典文件：
#### 1.3.4.1  MESSAGES_DICT_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_OF_AFDX
#### 1.3.4.2  MESSAGES_DICT_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_A_NET_OF_ARINC664
#### 1.3.4.3  MESSAGES_DICT_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_OF_AFDX
#### 1.3.4.4  MESSAGES_DICT_OF_MINIMUM_AND_BALANCING_USAGE_OF_BANDWIDTH_OF_B_NET_OF_ARINC664
#### 1.3.4.5  MESSAGES_DICT_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_OF_AFDX
#### 1.3.4.6  MESSAGES_DICT_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_A_NET_OF_ARINC664
#### 1.3.4.7  MESSAGES_DICT_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_OF_AFDX
#### 1.3.4.8  MESSAGES_DICT_OF_MINIMUM_USAGE_OF_BANDWIDTH_OF_B_NET_OF_ARINC664
具体格式为：
键（key）：消息的标识符
值（value）：为一列表，分别存储以下相关信息：\
&emsp;&emsp;[\
&emsp;&emsp;&emsp;&emsp;message guid,\
&emsp;&emsp;&emsp;&emsp;[ source logical port, [ source physical port, physical port, physical port, ..., physical port, destination physical port ], destination logical port ]\
&emsp;&emsp;&emsp;&emsp;... ...\
&emsp;&emsp;&emsp;&emsp;[ source logical port, [ source physical port, physical port, physical port, ..., physical port, destination physical port ], destination logical port ]\
&emsp;&emsp;]
