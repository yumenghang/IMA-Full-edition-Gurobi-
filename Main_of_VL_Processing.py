import VL_Configuration_of_VL_Processing

class MAIN_OF_VL_PROCESSING():
    def __init__(self, topology_type):
        self.topology_type = topology_type

    def main(self):
        VL_CONFIGURATION_OF_VL_PROCESSING = VL_Configuration_of_VL_Processing.VL_CONFIGURATION_OF_VL_PROCESSING()
        if self.topology_type == "ARINC664":
            VL_CONFIGURATION_OF_VL_PROCESSING.vl_configuration_of_vl_processing_of_arinc664()
        else:
            VL_CONFIGURATION_OF_VL_PROCESSING.vl_configuration_of_vl_processing_of_afdx()