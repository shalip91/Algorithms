from client_packer import ClientPacker
from client_shipper import ClientShipper
from orders.orders_file_generator import OrderFileGenerator
from pathlib import Path
from util import show_opt_schedule

"""****************************************************************************
*******************************************************************************
in this file, i will show the result for "sum" cost function with only small
variations to the 'ai' parameter

with opposed to the last 2 tests, where the prime shipments were first at the 
schedule but were not necessarily in ascending order with regard to the 
cost function. 
here we can see the there is a compatibility with cost function's values.
*******************************************************************************
****************************************************************************"""


ORDER_NUM = 15
MAX_INVENTORY_SIZE = 8
MAX_DISTANCE = 10
MAX_WEIGHT = 10
MAX_VALUE = 10
AI_MIN = 0.85
AI_MAX = 0.9
SHIP_INVENTORY_WEIGHT_RATIO = 0.15
WREG_MAX_INVENTORY_WEIGHT_RATIO = 0.3
REG_V_MAX_VALUE = MAX_VALUE * 0.7
COST_FUNCTION_TYPE = ["sum", "max", "identity", "len"]

def generate_input(filename):
    generator = OrderFileGenerator(order_num=ORDER_NUM,
                                   max_inventory_size=MAX_INVENTORY_SIZE,
                                   max_distance=MAX_DISTANCE,
                                   max_weight=MAX_WEIGHT,
                                   max_value=MAX_VALUE,
                                   ai_min=AI_MIN,
                                   ai_max=AI_MAX)
    generator.generate_json(filename)


if __name__ == '__main__':

    generate_input(f"input_files/{Path(__file__).stem}.json")

    packer = ClientPacker(filename=f"input_files/{Path(__file__).stem}.json",
                          ship_size=round(MAX_INVENTORY_SIZE * MAX_WEIGHT * SHIP_INVENTORY_WEIGHT_RATIO),
                          reg_w_max_size=round(MAX_INVENTORY_SIZE * MAX_WEIGHT * WREG_MAX_INVENTORY_WEIGHT_RATIO),
                          reg_v_max_value=REG_V_MAX_VALUE)


    shipper = ClientShipper(shipments=packer.calculate_shipments(),
                            q_diff_factor=0.75,
                            cost_function_type="sum")


    show_opt_schedule(tasks=shipper.schedule, cost_function_type="sum")

