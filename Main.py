"""

"""
import sys
import getopt
import Hyper_Parameters
import Main_of_Data_Processing
import Main_of_VL_Processing
import Main_of_Routes_Optimization
import Main_of_Routes_Path_Processing
import Main_of_Verify_The_Transmitting_Path_of_Messages_of_Routes_Path_Processing


if __name__ == "__main__":
    arguments_names_list = ["help", "Data_Processing=", "VL_Processing=", "topology_type=", "Routes_Optimization=", "task=", "net_type=", "Routes_Path_Processing=", "Verify_Transmitting_Path="]
    arguments_list = ["--help", "--Data_Processing", "--VL_Processing", "--topology_type", "--Routes_Optimization", "--task", "--net_type", "--Routes_Path_Processing", "--Verify_Transmitting_Path"]
    arguments_values_list = [[], ["True", "False"], ["True", "False"], ["ARINC664", "AFDX"], ["True", "False"], ["usage", "usage_and_loading"], ["A", "B"], ["True", "False"], ["True", "False"]]
    opts, args = getopt.getopt(sys.argv[1:], "-h", arguments_names_list)
    # 五大功能模块，执行标志默认为：0，即默认：不执行
    Data_Processing, VL_Processing, Routes_Optimization, Routes_Path_Processing, Verify_Transmitting_Path = "False", "False", "False", "False", "False"
    topology_type, task, net_type = "", "", ""
    for opt_name, opt_value in opts:
        if opt_name in ["-h", "--help"]:
            print(Hyper_Parameters.help_information)  # 打印程序使用信息
            exit()
        else:
            opt_name_index = arguments_list.index(opt_name)
            if opt_value not in arguments_values_list[opt_name_index]:
                print("Wrong input for %s" % (arguments_names_list[opt_name_index][:-1]))
                exit()
            if opt_name_index == 1:
                Data_Processing = opt_value
            if opt_name_index == 2:
                VL_Processing = opt_value
            if opt_name_index == 3:
                topology_type = opt_value
            if opt_name_index == 4:
                Routes_Optimization = opt_value
            if opt_name_index == 5:
                task = opt_value
            if opt_name_index == 6:
                net_type = opt_value
            if opt_name_index == 7:
                Routes_Path_Processing = opt_value
            if opt_name_index == 8:
                Verify_Transmitting_Path = opt_value

    if Data_Processing == "True":
        print("The raw data is being processed...")
        MAIN_OF_DATA_PROCESSING = Main_of_Data_Processing.MAIN_OF_DATA_PROCESSING()
        MAIN_OF_DATA_PROCESSING.main()
        print("The raw data has been precessed!")
    if VL_Processing == "True":
        if topology_type == "":
            print("Wrong input for topology_type!")
            exit()
        print("The VLs of %s are being processed..." % (topology_type))
        MAIN_OF_VL_PROCESSING = Main_of_VL_Processing.MAIN_OF_VL_PROCESSING(topology_type)
        MAIN_OF_VL_PROCESSING.main()
        print("The VLs of %s has been precessed!" % (topology_type))
    if Routes_Optimization == "True":
        if topology_type == "" and task == "" or net_type == "":
            print("Wrong input for topology_type, task and net_type!")
            exit()
        print("The routes of VLs of %s topology_type, %s task and net %s are being processed..." % (topology_type, task, net_type))
        MAIN_OF_ROUTES_OPTIMIZATION = Main_of_Routes_Optimization.MAIN_OF_ROUTES_OPTIMIZATION(topology_type, task, net_type)
        MAIN_OF_ROUTES_OPTIMIZATION.main()
        print("The routes of VLs of %s topology_type, %s task and net %s has been precessed!" % (topology_type, task, net_type))
    if Routes_Path_Processing == "True":
        print("The routes of messages of %s topology_type, %s task and net %s are being processed..." % (topology_type, task, net_type))
        MAIN_OF_ROUTES_PATH_PROCESSING = Main_of_Routes_Path_Processing.MAIN_OF_ROUTES_PATH_PROCESSING(topology_type, task, net_type)
        MAIN_OF_ROUTES_PATH_PROCESSING.main()
        print("The routes of messages of %s topology_type, %s task and net %s has been precessed!" % (topology_type, task, net_type))
    if Verify_Transmitting_Path == "True":
        print("The transmitting path of messages is being Verified...")
        # 检验消息传输路径回溯结果的正确性
        MAIN_OF_VERIFY_THE_TRANSMITTING_PATH_OF_MESSAGES_OF_ROUTES_PATH_PROCESSING = \
            Main_of_Verify_The_Transmitting_Path_of_Messages_of_Routes_Path_Processing.MAIN_OF_VERIFY_THE_TRANSMITTING_PATH_OF_MESSAGES_OF_ROUTES_PATH_PROCESSING()
        MAIN_OF_VERIFY_THE_TRANSMITTING_PATH_OF_MESSAGES_OF_ROUTES_PATH_PROCESSING.main()
        print("The transmitting path of messages has been Verified!")