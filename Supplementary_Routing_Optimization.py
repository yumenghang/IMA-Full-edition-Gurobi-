"""
经过验证，路由优化返回的路径中，存在路径不完全的情况
因此，需要针对路径不完全的目的地，单独寻找其传输路由
"""
from gurobipy import *

UPPER_BOUND = 100000
DELTA = 47

class supplementary_routing_optimize():
    def __init__( self, physical_ports_information, BANDWIDTH_OF_NODES ):
        self.physical_ports_information = physical_ports_information
        self.BANDWIDTH_OF_NODES = BANDWIDTH_OF_NODES

    def routing_optimize( self, ADJACENT_MATRIX, source, destination, mtu, bag, delay_bound_left, GAP, TIMELIMITED ):
        NUMBER_OF_NODES = len( ADJACENT_MATRIX )
        bandwidth_of_VL = ( mtu + DELTA ) / bag
        print( "BANDWIDTH OF NODES:", self.BANDWIDTH_OF_NODES )

        md = Model( 'MSP' )
        Y = md.addVars( NUMBER_OF_NODES, NUMBER_OF_NODES, lb=0, ub=1, vtype=GRB.INTEGER, name="Y" )
        Y_IN = md.addVars( NUMBER_OF_NODES, lb=0, ub=1, vtype=GRB.INTEGER, name="Y_IN" )
        Y_OUT = md.addVars( NUMBER_OF_NODES, lb=0, ub=1, vtype=GRB.INTEGER, name="Y_OUT" )

        DELAY_OF_NODES = md.addVars( NUMBER_OF_NODES, vtype=GRB.CONTINUOUS, name="DELAY_OF_NODES" )

        BANDWIDTH_COST_OF_VL = md.addVar( vtype=GRB.CONTINUOUS, name="BANDWIDTH_COST_OF_VL" )

        """
        开始添加约束
        """

        # 添加约束：节点到节点本身没有环路
        for node in range( NUMBER_OF_NODES ):
            md.addConstr( Y[ node, node ] == 0 )

        # 添加约束：物理链路不存在时，对应的Y的取值必然也为0
        for previous_node in range( NUMBER_OF_NODES ):
            for following_node in range( NUMBER_OF_NODES ):
                md.addConstr( Y[ previous_node, following_node ] <= ADJACENT_MATRIX[ previous_node ][ following_node ] )

        # 添加约束：对任意一条虚拟链路VL，没有节点向源节点传输数据，即：没有节点路由至源节点
        for previous_node in range( NUMBER_OF_NODES ):
            md.addConstr( Y[ previous_node, source ] == 0 )  # 没有节点向源节点传输数据

        # 添加约束：对任意一条虚拟链路的一个目的节点，有且仅有一个节点向目的节点路由
        md.addConstr( quicksum( Y[ previous_node, destination ] for previous_node in range( NUMBER_OF_NODES ) ) == 1 )  # 只有一个节点向目的节点传输数据

        # 添加约束：对于任意一条虚拟链路的节点，除源节点以及目的节点外，所有节点有且最多有一个节点路由向它本身
        for following_node in range( NUMBER_OF_NODES ):
            if following_node != source and following_node != destination:
                md.addConstr( quicksum( Y[ previous_node, following_node ] for previous_node in range( NUMBER_OF_NODES ) ) <= 1 )

        # 添加约束：对于任意一条虚拟链路，进入某个节点的虚链路需要寻址的节点数 以及出该节点的虚链路需要寻址的目的数
        for node in range(NUMBER_OF_NODES):
            md.addConstr( Y_IN[ node ] == quicksum( Y[ previous_node, node ] for previous_node in range( NUMBER_OF_NODES ) ) )
            md.addConstr( Y_OUT[ node ] == quicksum( Y[ node, following_node ] for following_node in range( NUMBER_OF_NODES ) ) )

        for node in range(NUMBER_OF_NODES):
            if node == source:
                md.addConstr( Y_IN[ node ] - Y_OUT[ node ] == -1 )
            elif node == destination:
                md.addConstr( Y_IN[ node ] - Y_OUT[ node ] == 1 )
            else:
                md.addConstr( Y_IN[ node ] == Y_OUT[ node ] )

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
        
        # 添加约束：任意一条物理链路传输的虚拟链路的带宽占用之和，不应当超过该条物理链路的带宽
        for previous_node in range( NUMBER_OF_NODES ):
            for following_node in range( NUMBER_OF_NODES ):
                md.addConstr( Y[ previous_node, following_node ] * bandwidth_of_VL <= self.BANDWIDTH_OF_NODES[ previous_node ] )

        md.addConstr( DELAY_OF_NODES[ source ] == 0 )
        for following_node in range( NUMBER_OF_NODES ):
            md.addConstr( DELAY_OF_NODES[ following_node ] == quicksum( ( DELAY_OF_NODES[ previous_node ] + 2 * mtu/bandwidth_of_VL ) * Y[ previous_node, following_node ] for previous_node in range( NUMBER_OF_NODES ) ) )
        md.addConstr( DELAY_OF_NODES[ destination ] <= delay_bound_left )
        """

        md.addConstr( BANDWIDTH_COST_OF_VL == quicksum( quicksum( Y[ previous_node, following_node ] * bandwidth_of_VL for previous_node in range( NUMBER_OF_NODES ) ) for following_node in range( NUMBER_OF_NODES ) ) )

        # set objective function，目标函数
        md.setObjective( BANDWIDTH_COST_OF_VL, GRB.MINIMIZE )

        md.setParam(GRB.Param.MIPGap, 0)
        md.Params.NonConvex = 2
        if GAP != None:
            md.Params.MIPGap = GAP  # 设置求解混合整数规划的Gap为GAP
        if TIMELIMITED != None:
            md.Params.TimeLimit = TIMELIMITED  # 设置最长求解时间为 TIMELIMITED 秒
        md.optimize()

        Y_FOR_RETURN = []
        for row_index in range( NUMBER_OF_NODES ):
            y_of_row = []
            for column_index in range( NUMBER_OF_NODES ):
                y_of_row.append( int( Y[ row_index, column_index ].x ) )
            Y_FOR_RETURN.append( y_of_row )

        delay_of_destination = DELAY_OF_NODES[ destination ].x

        BANDWIDTH_COST_FOR_RETURN = BANDWIDTH_COST_OF_VL.x

        # 更新节点带宽
        # 验证物理端口传输虚拟链路的带宽是否超出物理端口的传输速率
        for previous_node in range( NUMBER_OF_NODES ):
            for following_node in range( NUMBER_OF_NODES ):
                if Y_FOR_RETURN[ previous_node ][ following_node ] == 1:
                    bandwidth_cost = ( mtu + DELTA ) / bag
                    self.BANDWIDTH_OF_NODES[ previous_node ] -= bandwidth_cost

        return Y_FOR_RETURN, BANDWIDTH_COST_FOR_RETURN, delay_of_destination, self.BANDWIDTH_OF_NODES