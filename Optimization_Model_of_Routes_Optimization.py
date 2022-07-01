from gurobipy import *
import Hyper_Parameters
"""
SOURCE = [ source-1, source-2, ..., source-n ]
DESTINATION = [ [ destination-1-1, destination-1-2, ... ], [ destination-2-1, destination-2-2, ... ], ..., [ destination-n-1, destination-n-2, ... ] ]
DELAY_BOUND_OF_MESSAGES = [ [ [ bound-1, bound-2, ... ], [ bound-1, bound-2, ... ], ... ], [ [ bound-1, bound-2, ... ], [ bound-1, bound-2, ... ], ... ], ..., [ [ bound-1, bound-2, ... ], [ bound-1, bound-2, ... ], ... ] ]
DELAY_OCCURRED = [ [ [ occurred-1, occurred-2, ... ], [ occurred-1, occurred-2, ... ], ... ], [ [ occurred-1, occurred-2, ... ], [ occurred-1, occurred-2, ... ], ... ], ..., [ [ occurred-1, occurred-2, ... ], [ occurred-1, occurred-2, ... ], ... ] ]
"""



class OPTIMIZATION_MODEL_OF_ROUTES_OPTIMIZATION():
    def __init__(self, physical_ports_information, BANDWIDTH_OF_NODES):
        self.physical_ports_information = physical_ports_information
        self.BANDWIDTH_OF_NODES = BANDWIDTH_OF_NODES
        self.UPPER_BOUND = Hyper_Parameters.upper_bound
        self.DELTA = Hyper_Parameters.delta

    def calculate_bandwidth(self, MTU, BAG):
        BANDWIDTH_OF_VLs = []
        for index in range(len(MTU)):
            BANDWIDTH_OF_VLs.append((MTU[index] + self.DELTA) / BAG[index])
        return BANDWIDTH_OF_VLs

    def counting_the_number_of_existing_pyisical_links(self, ADJACENT_MATRIX):
        NUMBER_OF_EXISTING_PHYSICAL_LINKS = 0
        for previous_node in range(len(ADJACENT_MATRIX)):
            for following_node in range(len(ADJACENT_MATRIX)):
                if ADJACENT_MATRIX[previous_node][following_node] == 1:
                    NUMBER_OF_EXISTING_PHYSICAL_LINKS += 1
        return NUMBER_OF_EXISTING_PHYSICAL_LINKS

    def arinc664_routing_optimize_for_minimum_bandwidth_usage(self, ADJACENT_MATRIX, SOURCE, DESTINATION, MTU, BAG, DELAY_BOUND_LEFT, GAP, TIMELIMITED):
        NUMBER_OF_NODES, NUMBER_OF_VL = len(ADJACENT_MATRIX), len(SOURCE)
        BANDWIDTH_OF_VLs = self.calculate_bandwidth(MTU, BAG)
        print("BANDWIDTH OF NODES:", self.BANDWIDTH_OF_NODES)

        md = Model( 'MSP' )
        X, X_IN, X_OUT = {}, {}, {}
        for VL_index in range( NUMBER_OF_VL ):
            for previous_node in range( NUMBER_OF_NODES ):
                for following_node in range( NUMBER_OF_NODES ):
                    X[ VL_index, previous_node, following_node ] = md.addVar( lb=0, ub=len( DESTINATION[ VL_index ] ), vtype=GRB.INTEGER, name="X_" + str( VL_index ) + "_" + str( previous_node ) + "_" + str( following_node ) )

        for VL_index in range( NUMBER_OF_VL ):
            for node in range( NUMBER_OF_NODES ):
                X_IN[ VL_index, node ] = md.addVar( lb=0, ub=len( DESTINATION[ VL_index ] ), vtype=GRB.INTEGER, name="X_IN_" + str( VL_index ) + "_" + str( node ) )

        for VL_index in range( NUMBER_OF_VL ):
            for node in range( NUMBER_OF_NODES ):
                X_OUT[ VL_index, node ] = md.addVar( lb=0, ub=len( DESTINATION[ VL_index ] ), vtype=GRB.INTEGER, name="X_OUT_" + str( VL_index ) + "_" + str( node ) )

        Y = {}
        for VL_index in range( NUMBER_OF_VL ):
            for previous_node in range( NUMBER_OF_NODES ):
                for following_node in range( NUMBER_OF_NODES ):
                    Y[ VL_index, previous_node, following_node ] = md.addVar( vtype=GRB.BINARY, name="Y_" + str( VL_index ) + "_" + str( previous_node ) + "_" + str( following_node ) )

        DELAY_OF_NODES = md.addVars( NUMBER_OF_VL, NUMBER_OF_NODES, vtype=GRB.CONTINUOUS, name="DELAY_OF_NODES" )

        BANDWIDTH_COST_OF_VL = md.addVars( NUMBER_OF_VL, vtype=GRB.CONTINUOUS, name="BANDWIDTH_COST_OF_VL" )
        TOTAL_BANDWIDTH_COST = md.addVar( vtype=GRB.CONTINUOUS, name="TOTAL_BANDWIDTH_COST" )

        """
        开始添加约束
        """

        """
        添加约束：约束X与Y之间的大小对应关系: 1, 当Y取0时，X必然也取0; 2, 当Y取1时，X必然取值大于0
        因此下述相关X与Y的取值的约束，只对Y进行约束即可
        """
        for VL_index in range(NUMBER_OF_VL):
            for previous_node in range( NUMBER_OF_NODES ):
                for following_node in range( NUMBER_OF_NODES ):
                    md.addConstr( Y[ VL_index, previous_node, following_node ] <= X[ VL_index, previous_node, following_node ] )
                    md.addConstr( self.UPPER_BOUND * Y[ VL_index, previous_node, following_node ] >= X[ VL_index, previous_node, following_node ] )

        # 添加约束：节点到节点本身没有环路
        for VL_index in range( NUMBER_OF_VL ):
            for node in range( NUMBER_OF_NODES ):
                md.addConstr( Y[ VL_index, node, node ] == 0 )

        # 添加约束：物理链路不存在时，对应的Y的取值必然也为0
        for VL_index in range( NUMBER_OF_VL ):
            for previous_node in range( NUMBER_OF_NODES ):
                for following_node in range( NUMBER_OF_NODES ):
                    md.addConstr( Y[ VL_index, previous_node, following_node ] <= ADJACENT_MATRIX[ previous_node ][ following_node ] )

        # 添加约束：对任意一条虚拟链路VL，没有节点向源节点传输数据，即：没有节点路由至源节点
        for VL_index in range( NUMBER_OF_VL ):
            source_node = SOURCE[ VL_index ]
            for previous_node in range( NUMBER_OF_NODES ):
                md.addConstr( Y[ VL_index, previous_node, source_node ] == 0 )  # 没有节点向源节点传输数据

        # 添加约束：对任意一条虚拟链路的一个目的节点，有且仅有一个节点向目的节点路由
        for VL_index in range( NUMBER_OF_VL ):
            for destination_node in DESTINATION[ VL_index ]:
                md.addConstr( quicksum( Y[ VL_index, previous_node, destination_node ] for previous_node in range( NUMBER_OF_NODES ) ) == 1 )  # 只有一个节点向目的节点传输数据

        # 添加约束：对于任意一条虚拟链路的节点，除源节点以及目的节点外，所有节点有且最多有一个节点路由向它本身
        for VL_index in range( NUMBER_OF_VL ):
            for following_node in range( NUMBER_OF_NODES ):
                if following_node != SOURCE[ VL_index ] and following_node not in DESTINATION[ VL_index ]:
                    md.addConstr( quicksum( Y[ VL_index, previous_node, following_node ] for previous_node in range( NUMBER_OF_NODES ) ) <= 1 )

        # 添加约束：对于任意一条虚拟链路，进入某个节点的虚链路需要寻址的节点数 以及出该节点的虚链路需要寻址的目的数
        for VL_index in range(NUMBER_OF_VL):
            for node in range(NUMBER_OF_NODES):
                md.addConstr( X_IN[ VL_index, node ] == quicksum( X[ VL_index, previous_node, node ] for previous_node in range( NUMBER_OF_NODES ) ) )
                md.addConstr( X_OUT[ VL_index, node ] == quicksum( X[ VL_index, node, following_node ] for following_node in range( NUMBER_OF_NODES ) ) )

        for VL_index in range(NUMBER_OF_VL):
            for node in range(NUMBER_OF_NODES):
                if node == SOURCE[ VL_index ]:
                    md.addConstr( X_IN[ VL_index, node ] - X_OUT[ VL_index, node ] == -len( DESTINATION[ VL_index ] ) )
                elif node in DESTINATION[ VL_index ]:
                    md.addConstr( X_IN[ VL_index, node ] - X_OUT[ VL_index, node ] == 1 )
                else:
                    md.addConstr( X_IN[ VL_index, node ] == X_OUT[ VL_index, node ] )

        """
        TOTAL_MESSAGE_SIZE_TRANSMITTED_BY_PHYSICAL_PORTS = md.addVars( NUMBER_OF_NODES, NUMBER_OF_NODES, vtype=GRB.INTEGER, name="TOTAL_MESSAGE_SIZE_TRANSMITTED_BY_PHYSICAL_PORTS" ) # 二维数组：记录每一条物理链路传输的虚拟链路的MTU之和
        # 添加约束：每一条物理链路传输的虚拟链路的MTU之和等于所有经此虚拟链路传输的虚拟链路的MTU之和
        for previous_node in range( NUMBER_OF_NODES ):
            for following_node in range( NUMBER_OF_NODES ):
                md.addConstr( TOTAL_MESSAGE_SIZE_TRANSMITTED_BY_PHYSICAL_PORTS[ previous_node, following_node ] == quicksum( Y[ VL_index, previous_node, following_node ] * MTU[ VL_index ] for VL_index in range( NUMBER_OF_VL ) ) )
        # 添加约束：每一条物理链路必须（有足够带宽）将所有经此物理链路传输的虚拟链路的MTU之和在一个BAG内转发完毕
        for previous_node in range( NUMBER_OF_NODES ):
            for following_node in range( NUMBER_OF_NODES ):
                for VL_index in range( NUMBER_OF_VL ):
                    md.addConstr( BAG[ VL_index ] * BANDWIDTH_OF_NODES[ previous_node ] >= TOTAL_MESSAGE_SIZE_TRANSMITTED_BY_PHYSICAL_PORTS[ previous_node, following_node ] * Y[ VL_index, previous_node, following_node ] )
        """

        # 添加约束：任意一条物理链路传输的虚拟链路的带宽占用之和，不应当超过该条物理链路的带宽
        for previous_node in range( NUMBER_OF_NODES ):
            for following_node in range( NUMBER_OF_NODES ):
                md.addConstr( quicksum( Y[ VL_index, previous_node, following_node ] * BANDWIDTH_OF_VLs[ VL_index ] for VL_index in range( NUMBER_OF_VL ) ) <= self.BANDWIDTH_OF_NODES[ previous_node ] )

        for VL_index in range( NUMBER_OF_VL ):
            md.addConstr( DELAY_OF_NODES[ VL_index, SOURCE[ VL_index ] ] == 0 )
        for VL_index in range( NUMBER_OF_VL ):
            for following_node in range( NUMBER_OF_NODES ):
                md.addConstr( DELAY_OF_NODES[ VL_index, following_node ] == quicksum( ( DELAY_OF_NODES[ VL_index, previous_node ] + 2 * MTU[ VL_index ]/self.BANDWIDTH_OF_NODES[ previous_node ] ) * Y[ VL_index, previous_node, following_node ] for previous_node in range( NUMBER_OF_NODES ) ) )
        for VL_index in range( NUMBER_OF_VL ):
            for destination_index in range( len( DESTINATION[ VL_index ] ) ):
                destination = DESTINATION[ VL_index ][ destination_index ]
                md.addConstr( DELAY_OF_NODES[ VL_index, destination ] <= DELAY_BOUND_LEFT[ VL_index ][ destination_index ] )

        for VL_index in range( NUMBER_OF_VL ):
            md.addConstr( BANDWIDTH_COST_OF_VL[ VL_index ] == quicksum( quicksum( Y[ VL_index, previous_node, following_node ] * BANDWIDTH_OF_VLs[ VL_index ] for previous_node in range( NUMBER_OF_NODES ) ) for following_node in range( NUMBER_OF_NODES ) ) )

        # set objective function，目标函数
        md.addConstr( TOTAL_BANDWIDTH_COST == quicksum( BANDWIDTH_COST_OF_VL[ VL_index ] for VL_index in range( NUMBER_OF_VL ) ) )

        md.setObjective( TOTAL_BANDWIDTH_COST, GRB.MINIMIZE )

        md.Params.NonConvex = 2
        if GAP != None:
            md.Params.MIPGap = GAP  # 设置求解混合整数规划的Gap为GAP
        if TIMELIMITED != None:
            md.Params.TimeLimit = TIMELIMITED  # 设置最长求解时间为 TIMELIMITED 秒
        md.optimize()

        X_FOR_RETURN, Y_FOR_RETURN = [], []
        for VL_index in range( NUMBER_OF_VL ):
            x_of_vl, y_of_vl = [], []
            for row_index in range( NUMBER_OF_NODES ):
                x_of_row, y_of_row = [], []
                for column_index in range( NUMBER_OF_NODES ):
                    if X[ VL_index, row_index, column_index ].x >= Hyper_Parameters.threshold_for_binary:
                        x_of_row.append(1)
                    else:
                        x_of_row.append(0)
                    if Y[ VL_index, row_index, column_index ].x >= Hyper_Parameters.threshold_for_binary:
                        y_of_row.append(1)
                    else:
                        y_of_row.append(0)
                x_of_vl.append( x_of_row )
                y_of_vl.append( y_of_row )
            X_FOR_RETURN.append( x_of_vl )
            Y_FOR_RETURN.append( y_of_vl )

        DELAY_OF_NODES_FOR_RETURN = []
        for VL_index in range( NUMBER_OF_VL ):
            delay_of_vl = []
            for node in DESTINATION[ VL_index ]:
                delay_of_vl.append( float( DELAY_OF_NODES[ VL_index, node ].x ) )
            DELAY_OF_NODES_FOR_RETURN.append( delay_of_vl )

        TOTAL_BANDWIDTH_COST_FOR_RETURN = TOTAL_BANDWIDTH_COST.x

        # 更新节点带宽
        # 验证物理端口传输虚拟链路的带宽是否超出物理端口的传输速率
        for previous_node in range( NUMBER_OF_NODES ):
            bandwidth_cost = 0
            for VL_index in range( NUMBER_OF_VL ):
                for following_node in range( NUMBER_OF_NODES ):
                    if Y_FOR_RETURN[ VL_index ][ previous_node ][ following_node ] == 1:
                        bandwidth_cost += ( MTU[ VL_index ] + self.DELTA ) / BAG[ VL_index ]
            self.BANDWIDTH_OF_NODES[ previous_node ] -= bandwidth_cost

        return X_FOR_RETURN, Y_FOR_RETURN, TOTAL_BANDWIDTH_COST_FOR_RETURN, DELAY_OF_NODES_FOR_RETURN, self.BANDWIDTH_OF_NODES

    def arinc664_routing_optimize_for_minimum_bandwidth_usage_and_load_balancing( self, ADJACENT_MATRIX, SOURCE, DESTINATION, MTU, BAG, DELAY_BOUND_LEFT, GAP, TIMELIMITED ):
        NUMBER_OF_NODES, NUMBER_OF_VL = len( ADJACENT_MATRIX ), len( SOURCE )
        NUMBER_OF_EXISTING_PHYSICAL_LINKS = self.counting_the_number_of_existing_pyisical_links( ADJACENT_MATRIX )
        BANDWIDTH_OF_VLs = self.calculate_bandwidth( MTU, BAG )
        print( "BANDWIDTH OF NODES:", self.BANDWIDTH_OF_NODES )

        md = Model( 'MSP' )
        X, X_IN, X_OUT = {}, {}, {}
        for VL_index in range( NUMBER_OF_VL ):
            for previous_node in range( NUMBER_OF_NODES ):
                for following_node in range( NUMBER_OF_NODES ):
                    X[ VL_index, previous_node, following_node ] = md.addVar( lb=0, ub=len( DESTINATION[ VL_index ] ), vtype=GRB.INTEGER, name="X_" + str( VL_index ) + "_" + str( previous_node ) + "_" + str( following_node ) )

        for VL_index in range( NUMBER_OF_VL ):
            for node in range( NUMBER_OF_NODES ):
                X_IN[ VL_index, node ] = md.addVar( lb=0, ub=len( DESTINATION[ VL_index ] ), vtype=GRB.INTEGER, name="X_IN_" + str( VL_index ) + "_" + str( node ) )

        for VL_index in range( NUMBER_OF_VL ):
            for node in range( NUMBER_OF_NODES ):
                X_OUT[ VL_index, node ] = md.addVar( lb=0, ub=len( DESTINATION[ VL_index ] ), vtype=GRB.INTEGER, name="X_OUT_" + str( VL_index ) + "_" + str( node ) )

        Y = {}
        for VL_index in range( NUMBER_OF_VL ):
            for previous_node in range( NUMBER_OF_NODES ):
                for following_node in range( NUMBER_OF_NODES ):
                    Y[ VL_index, previous_node, following_node ] = md.addVar( vtype=GRB.BINARY, name="Y_" + str( VL_index ) + "_" + str( previous_node ) + "_" + str( following_node ) )

        PERCENT_OF_BANDWIDTH_USAGE = md.addVars( NUMBER_OF_NODES, NUMBER_OF_NODES, vtype=GRB.CONTINUOUS, name="PERCENT_OF_BANDWIDTH_USAGE" )  # 二维数组，记录每一条物理链路的带宽占用百分比
        PERCENT_OF_AVERAGE_BANDWIDDTH_USAGE = md.addVar( vtype=GRB.CONTINUOUS, name="PERCENT_OF_AVERAGE_BANDWIDDTH_USAGE" ) # 记录所有存在的物理链路的带宽占用百分比的平均数
        ABS_PERCENT_OF_DELTA_OF_BANDWIDTH_USGE = md.addVars( NUMBER_OF_NODES, NUMBER_OF_NODES, lb=-1, ub=1, vtype=GRB.CONTINUOUS, name="PERCENT_OF_DELTA_OF_BANDWIDTH_USGE" ) # 二维数组，记录所有存在的物理链路的带宽占用百分比与平均数之差
        VARIANCE = md.addVar( vtype=GRB.CONTINUOUS, name="VARIANCE" ) # 记录所有存在的物理链路的带宽占用百分比方差

        DELAY_OF_NODES = md.addVars( NUMBER_OF_VL, NUMBER_OF_NODES, vtype=GRB.CONTINUOUS, name="DELAY_OF_NODES" )

        BANDWIDTH_COST_OF_VL = md.addVars( NUMBER_OF_VL, vtype=GRB.CONTINUOUS, name="BANDWIDTH_COST_OF_VL" )
        TOTAL_BANDWIDTH_COST = md.addVar( vtype=GRB.CONTINUOUS, name="TOTAL_BANDWIDTH_COST" )

        """
        开始添加约束
        """

        """
        添加约束：约束X与Y之间的大小对应关系: 1, 当Y取0时，X必然也取0; 2, 当Y取1时，X必然取值大于0
        因此下述相关X与Y的取值的约束，只对Y进行约束即可
        """
        for VL_index in range(NUMBER_OF_VL):
            for previous_node in range( NUMBER_OF_NODES ):
                for following_node in range( NUMBER_OF_NODES ):
                    md.addConstr( Y[ VL_index, previous_node, following_node ] <= X[ VL_index, previous_node, following_node ] )
                    md.addConstr( self.UPPER_BOUND * Y[ VL_index, previous_node, following_node ] >= X[ VL_index, previous_node, following_node ] )

        # 添加约束：节点到节点本身没有环路
        for VL_index in range( NUMBER_OF_VL ):
            for node in range( NUMBER_OF_NODES ):
                md.addConstr( Y[ VL_index, node, node ] == 0 )

        # 添加约束：物理链路不存在时，对应的Y的取值必然也为0
        for VL_index in range( NUMBER_OF_VL ):
            for previous_node in range( NUMBER_OF_NODES ):
                for following_node in range( NUMBER_OF_NODES ):
                    md.addConstr( Y[ VL_index, previous_node, following_node ] <=  ADJACENT_MATRIX[ previous_node ][ following_node ] )

        # 添加约束：对任意一条虚拟链路VL，没有节点向源节点传输数据，即：没有节点路由至源节点
        for VL_index in range( NUMBER_OF_VL ):
            source_node = SOURCE[ VL_index ]
            for previous_node in range( NUMBER_OF_NODES ):
                md.addConstr( Y[ VL_index, previous_node, source_node ] == 0 )  # 没有节点向源节点传输数据

        # 添加约束：对任意一条虚拟链路的一个目的节点，有且仅有一个节点向目的节点路由
        for VL_index in range( NUMBER_OF_VL ):
            for destination_node in DESTINATION[ VL_index ]:
                md.addConstr( quicksum( Y[ VL_index, previous_node, destination_node ] for previous_node in range( NUMBER_OF_NODES ) ) == 1 )  # 只有一个节点向目的节点传输数据

        # 添加约束：对于任意一条虚拟链路的节点，除源节点以及目的节点外，所有节点有且最多有一个节点路由向它本身
        for VL_index in range( NUMBER_OF_VL ):
            for following_node in range( NUMBER_OF_NODES ):
                if following_node != SOURCE[ VL_index ] and following_node not in DESTINATION[ VL_index ]:
                    md.addConstr( quicksum( Y[ VL_index, previous_node, following_node ] for previous_node in range( NUMBER_OF_NODES ) ) <= 1 )

        # 添加约束：对于任意一条虚拟链路，进入某个节点的虚链路需要寻址的节点数 以及出该节点的虚链路需要寻址的目的数
        for VL_index in range(NUMBER_OF_VL):
            for node in range(NUMBER_OF_NODES):
                md.addConstr( X_IN[ VL_index, node ] == quicksum( X[ VL_index, previous_node, node ] for previous_node in range( NUMBER_OF_NODES ) ) )
                md.addConstr( X_OUT[ VL_index, node ] == quicksum( X[ VL_index, node, following_node ] for following_node in range( NUMBER_OF_NODES ) ) )

        for VL_index in range(NUMBER_OF_VL):
            for node in range(NUMBER_OF_NODES):
                if node == SOURCE[ VL_index ]:
                    md.addConstr( X_IN[ VL_index, node ] - X_OUT[ VL_index, node ] == -len( DESTINATION[ VL_index ] ) )
                elif node in DESTINATION[ VL_index ]:
                    md.addConstr( X_IN[ VL_index, node ] - X_OUT[ VL_index, node ] == 1 )
                else:
                    md.addConstr( X_IN[ VL_index, node ] == X_OUT[ VL_index, node ] )

        """
        TOTAL_MESSAGE_SIZE_TRANSMITTED_BY_PHYSICAL_PORTS = md.addVars( NUMBER_OF_NODES, NUMBER_OF_NODES, vtype=GRB.INTEGER, name="TOTAL_MESSAGE_SIZE_TRANSMITTED_BY_PHYSICAL_PORTS" ) # 二维数组：记录每一条物理链路传输的虚拟链路的MTU之和
        # 添加约束：每一条物理链路传输的虚拟链路的MTU之和等于所有经此虚拟链路传输的虚拟链路的MTU之和
        for previous_node in range( NUMBER_OF_NODES ):
            for following_node in range( NUMBER_OF_NODES ):
                md.addConstr( TOTAL_MESSAGE_SIZE_TRANSMITTED_BY_PHYSICAL_PORTS[ previous_node, following_node ] == quicksum( Y[ VL_index, previous_node, following_node ] * MTU[ VL_index ] for VL_index in range( NUMBER_OF_VL ) ) )
        # 添加约束：每一条物理链路必须（有足够带宽）将所有经此物理链路传输的虚拟链路的MTU之和在一个BAG内转发完毕
        for previous_node in range( NUMBER_OF_NODES ):
            for following_node in range( NUMBER_OF_NODES ):
                for VL_index in range( NUMBER_OF_VL ):
                    md.addConstr( BAG[ VL_index ] * BANDWIDTH_OF_NODES[ previous_node ] >= TOTAL_MESSAGE_SIZE_TRANSMITTED_BY_PHYSICAL_PORTS[ previous_node, following_node ] * Y[ VL_index, previous_node, following_node ] )
        """

        # 添加约束：任意一条物理链路传输的虚拟链路的带宽占用之和，不应当超过该条物理链路的带宽
        for previous_node in range( NUMBER_OF_NODES ):
            for following_node in range( NUMBER_OF_NODES ):
                md.addConstr( quicksum( Y[ VL_index, previous_node, following_node ] * BANDWIDTH_OF_VLs[ VL_index ] for VL_index in range( NUMBER_OF_VL ) ) <= self.BANDWIDTH_OF_NODES[ previous_node ] )

        for VL_index in range( NUMBER_OF_VL ):
            md.addConstr( DELAY_OF_NODES[ VL_index, SOURCE[ VL_index ] ] == 0 )
        for VL_index in range( NUMBER_OF_VL ):
            for following_node in range( NUMBER_OF_NODES ):
                md.addConstr( DELAY_OF_NODES[ VL_index, following_node ] == quicksum( ( DELAY_OF_NODES[ VL_index, previous_node ] + 2 * MTU[ VL_index ]/self.BANDWIDTH_OF_NODES[ previous_node ] ) * Y[ VL_index, previous_node, following_node ] for previous_node in range( NUMBER_OF_NODES ) ) )
        for VL_index in range( NUMBER_OF_VL ):
            for destination_index in range( len( DESTINATION[ VL_index ] ) ):
                destination = DESTINATION[ VL_index ][ destination_index ]
                md.addConstr( DELAY_OF_NODES[ VL_index, destination ] <= DELAY_BOUND_LEFT[ VL_index ][ destination_index ] )

        for previous_node in range( NUMBER_OF_NODES ):
            for following_node in range( NUMBER_OF_NODES ):
                md.addConstr( PERCENT_OF_BANDWIDTH_USAGE[ previous_node, following_node ] * self.BANDWIDTH_OF_NODES[ previous_node ] == quicksum( Y[ VL_index, previous_node, following_node ] * BANDWIDTH_OF_VLs[ VL_index ] for VL_index in range( NUMBER_OF_VL ) ) )
        md.addConstr( PERCENT_OF_AVERAGE_BANDWIDDTH_USAGE * NUMBER_OF_EXISTING_PHYSICAL_LINKS == quicksum( quicksum( PERCENT_OF_BANDWIDTH_USAGE[ previous_node, following_node ] for previous_node in range( NUMBER_OF_NODES ) ) for following_node in range( NUMBER_OF_NODES ) ) )
        for previous_node in range( NUMBER_OF_NODES ):
            for following_node in range( NUMBER_OF_NODES ):
                md.addConstr( ABS_PERCENT_OF_DELTA_OF_BANDWIDTH_USGE[ previous_node, following_node ] >= PERCENT_OF_BANDWIDTH_USAGE[ previous_node, following_node ] - PERCENT_OF_AVERAGE_BANDWIDDTH_USAGE )
                md.addConstr( ABS_PERCENT_OF_DELTA_OF_BANDWIDTH_USGE[ previous_node, following_node ] >= PERCENT_OF_AVERAGE_BANDWIDDTH_USAGE - PERCENT_OF_BANDWIDTH_USAGE[ previous_node, following_node ] )
        md.addConstr( VARIANCE == quicksum( quicksum( ABS_PERCENT_OF_DELTA_OF_BANDWIDTH_USGE[ previous_node, following_node ] for previous_node in range( NUMBER_OF_NODES ) ) for following_node in range( NUMBER_OF_NODES ) ) )

        # set objective function，目标函数
        md.setObjective( VARIANCE, GRB.MINIMIZE )

        """
        for VL_index in range( NUMBER_OF_VL ):
            md.addConstr( BANDWIDTH_COST_OF_VL[ VL_index ] == quicksum( quicksum( Y[ VL_index, previous_node, following_node ] * BANDWIDTH_OF_VLs[ VL_index ] for previous_node in range( NUMBER_OF_NODES ) ) for following_node in range( NUMBER_OF_NODES ) ) )

        # set objective function，目标函数
        md.addConstr( TOTAL_BANDWIDTH_COST == quicksum( BANDWIDTH_COST_OF_VL[ VL_index ] for VL_index in range( NUMBER_OF_VL ) ) )

        md.setObjective( TOTAL_BANDWIDTH_COST, GRB.MINIMIZE )
        """

        md.Params.NonConvex = 2
        if GAP != None:
            md.Params.MIPGap = GAP  # 设置求解混合整数规划的Gap为GAP
        if TIMELIMITED != None:
            md.Params.TimeLimit = TIMELIMITED  # 设置最长求解时间为 TIMELIMITED 秒
        md.optimize()

        X_FOR_RETURN, Y_FOR_RETURN = [], []
        for VL_index in range( NUMBER_OF_VL ):
            x_of_vl, y_of_vl = [], []
            for row_index in range( NUMBER_OF_NODES ):
                x_of_row, y_of_row = [], []
                for column_index in range( NUMBER_OF_NODES ):
                    if X[ VL_index, row_index, column_index ].x >= Hyper_Parameters.threshold_for_binary:
                        x_of_row.append(1)
                    else:
                        x_of_row.append(0)
                    if Y[ VL_index, row_index, column_index ].x >= Hyper_Parameters.threshold_for_binary:
                        y_of_row.append(1)
                    else:
                        y_of_row.append(0)
                x_of_vl.append( x_of_row )
                y_of_vl.append( y_of_row )
            X_FOR_RETURN.append( x_of_vl )
            Y_FOR_RETURN.append( y_of_vl )

        DELAY_OF_NODES_FOR_RETURN = []
        for VL_index in range( NUMBER_OF_VL ):
            delay_of_vl = []
            for node in DESTINATION[ VL_index ]:
                delay_of_vl.append( float( DELAY_OF_NODES[ VL_index, node ].x ) )
            DELAY_OF_NODES_FOR_RETURN.append( delay_of_vl )

        TOTAL_BANDWIDTH_COST_FOR_RETURN = TOTAL_BANDWIDTH_COST.x

        # 更新节点带宽
        # 验证物理端口传输虚拟链路的带宽是否超出物理端口的传输速率
        for previous_node in range( NUMBER_OF_NODES ):
            bandwidth_cost = 0
            for VL_index in range( NUMBER_OF_VL ):
                for following_node in range( NUMBER_OF_NODES ):
                    if Y_FOR_RETURN[ VL_index ][ previous_node ][ following_node ] == 1:
                        bandwidth_cost += ( MTU[ VL_index ] + self.DELTA ) / BAG[ VL_index ]
            self.BANDWIDTH_OF_NODES[ previous_node ] -= bandwidth_cost

        # 验证物理链路带宽占用百分比
        for previous_node in range( NUMBER_OF_NODES ):
            for following_node in range( NUMBER_OF_NODES ):
                if ADJACENT_MATRIX[previous_node][following_node] == 0 and PERCENT_OF_BANDWIDTH_USAGE[previous_node, following_node].x > 0:
                    print("ADJACENT_MATRIX[%d][%d]:" % (previous_node, following_node), ADJACENT_MATRIX[previous_node][following_node], "PERCENT_OF_DELTA_OF_BANDWIDTH_USGE[%d, %d]:" % (previous_node, following_node), PERCENT_OF_BANDWIDTH_USAGE[previous_node, following_node].x)
                if PERCENT_OF_BANDWIDTH_USAGE[previous_node, following_node].x > 1:
                    print("ADJACENT_MATRIX[%d][%d]:" % (previous_node, following_node), ADJACENT_MATRIX[previous_node][following_node], "PERCENT_OF_DELTA_OF_BANDWIDTH_USGE[%d, %d]:" % (previous_node, following_node), PERCENT_OF_BANDWIDTH_USAGE[previous_node, following_node].x)

        print( "VARIANCE:", VARIANCE.x )

        return X_FOR_RETURN, Y_FOR_RETURN, TOTAL_BANDWIDTH_COST_FOR_RETURN, DELAY_OF_NODES_FOR_RETURN, self.BANDWIDTH_OF_NODES