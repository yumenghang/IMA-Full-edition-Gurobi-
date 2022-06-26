# IMA-Full edition (Gurobi)

## 使用
python Main.py -h --help --Data_Processing= --VL_Processing= --topology_type= --Routes_Optimization= --task= --net_type= --Routes_Path_Processing=
-h: 打印help信息；\
--help: 打印help信息；\
--Data_Processing: True或者False，表示是否处理原始数据。原始数据的处理结果存储在同一路径下的"./Intermediate data file/"文件夹中（注：此时不需要额外的参数）；\
--VL_Processing: True或者False，表示是否将消息以虚链路为单位进行划分。消息划分后得到的虚链路以字典的形式存储在同一路径下的"./Intermediate VL dict file/"文件夹中（注：此时需要额外的参数：topology_type）；\
--topology_type: AFDX或者ARINC6664，表示消息、虚链路的处理范围是在AFDX网络拓扑中还是在ARINC664网络拓扑中；\
--Routes_Optimization: True或者False，表示是否对虚链路的路由进行优化。虚链路路由的优化结果得到后，包括一些中间数据，均存储在同一路径下的"./Intermediate routes file/"文件夹中（注：此时需要额外的参数：topology_type、task以及net_type）；\
--task: usage或者usage_and_loading，表示虚链路路由的优化过程中，需要遵循的既定前提条件，包括：最低传输延迟、最低传输延迟且延迟分布最均衡、最高带宽余量、最高带宽余量且负载最均衡等。这里：\
xxxx --> 获取最低传输延迟的路由；；
xxxxx --> 获取最低传输延迟且延迟分布最均衡的路由；
usage --> 获取最高带宽余量的路由；
usage_and_loading --> 获取最高带宽余量且负载最均衡的路由；
--net_type: A或者B，表示消息、虚链路的处理范围是在A网还是B网中；\
--Routes_Path_Processing: True或者False，表示是否根据得到的虚链路的路由，回溯消息的传输路径（注：此时需要额外的参数：topology_type、task以及net_type）。\

### 功能模块：\
1、打印help信息
2、原始数据文件处理；\
3、消息分配及虚链路优化处理；\
4、虚链路路由优化；\
5、消息传输路径回溯。\

### 命令
1、打印help信息：\
python Main.py -h\
或者\
python Main.py --help\

2、处理原始数据文件：\
python Main.py -Data_Processing=True\

3、优化处理消息分配及虚链路：\
python Main.py -VL_Processing=True --topology_type=AFDX\
或者\
python Main.py -VL_Processing=True --topology_type=ARINC664\

4、优化虚链路路由：\
python Main.py -Routes_Optimization=True --topology_type=AFDX --task=usage --net_type=A\
或者\
python Main.py -Routes_Optimization=True --topology_type=AFDX --task=usage --net_type=B\
或者\
python Main.py -Routes_Optimization=True --topology_type=AFDX --task=usage_and_loading --net_type=A\
或者\
python Main.py -Routes_Optimization=True --topology_type=AFDX --task=usage_and_loading --net_type=B\
或者\
python Main.py -Routes_Optimization=True --topology_type=ARINC664 --task=usage --net_type=A\
或者\
python Main.py -Routes_Optimization=True --topology_type=ARINC664 --task=usage --net_type=B\
或者\
python Main.py -Routes_Optimization=True --topology_type=ARINC664 --task=usage_and_loading --net_type=A\
或者\
python Main.py -Routes_Optimization=True --topology_type=ARINC664 --task=usage_and_loading --net_type=B\

5、回溯消息传输路径：\
python Main.py -h 或者 python Main.py --help\
python Main.py -Routes_Path_Processing=True --topology_type=AFDX --task=usage --net_type=A\
或者\
python Main.py -Routes_Path_Processing=True --topology_type=AFDX --task=usage --net_type=B\
或者\
python Main.py -Routes_Path_Processing=True --topology_type=AFDX --task=usage_and_loading --net_type=A\
或者\
python Main.py -Routes_Path_Processing=True --topology_type=AFDX --task=usage_and_loading --net_type=B\
或者\
python Main.py -Routes_Path_Processing=True --topology_type=ARINC664 --task=usage --net_type=A\
或者\
python Main.py -Routes_Path_Processing=True --topology_type=ARINC664 --task=usage --net_type=B\
或者\
python Main.py -Routes_Path_Processing=True --topology_type=ARINC664 --task=usage_and_loading --net_type=A\
或者\
python Main.py -Routes_Path_Processing=True --topology_type=ARINC664 --task=usage_and_loading --net_type=B\
