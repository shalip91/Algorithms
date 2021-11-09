from client_packer import ClientPacker
from client_shipper import ClientShipper
from orders.orders_file_generator import OrderFileGenerator
from pathlib import Path
from util import show_opt_schedule

"""****************************************************************************
*******************************************************************************
in this file, i will show the result for "sum" cost function:

the same as with small batch file !
we can see that every cost function plot a different schedule.
the difference is at the position between the 'v-reg' them selfs and the prime.
-   the 'w-reg' keeps his position as a barrier between the 'v-regs' and the 'primes'
*******************************************************************************
****************************************************************************"""


ORDER_NUM = 40
MAX_INVENTORY_SIZE = 8
MAX_DISTANCE = 10
MAX_WEIGHT = 10
MAX_VALUE = 100
AI_MIN = 0.1
AI_MAX = 1
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
    packer.calculate_shipments()

    shipper = ClientShipper(shipments=packer.shipments,
                            q_diff_factor=0.75,
                            cost_function_type="sum")

    show_opt_schedule(tasks=shipper.schedule, cost_function_type="sum")

