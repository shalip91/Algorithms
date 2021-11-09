from client_packer import ClientPacker
from client_shipper import ClientShipper
from util import *


"""****************************************************************************
*******************************************************************************
in this file, i will show the result for the 4th assignment:
"Plot both shipments and schedules, plus scheduling objective function values."

in the last line i am plotting the Gantt Chart of the Schedule.
we can see that the see a good result of the primes at first and the regular line
as last.

something interesting happening with the "cost values" of each shipment.
the regulars are sorted by the increasing "cost values", but the primes are not.
*******************************************************************************
****************************************************************************"""


if __name__ == '__main__':

    packer = ClientPacker(filename='input_files/orders.json',
                          ship_size=12,
                          reg_w_max_size=10,
                          reg_v_max_value=5)

    title_print("orders before calculating the shipments")
    for o in packer.orders: print(o)

    title_print("orders after calculating the shipments")
    for s in packer.calculate_shipments(): print(s)

    shipper = ClientShipper(shipments=packer.shipments,
                            q_diff_factor=0.75,
                            cost_function_type="sum")

    title_print("precedence graph")
    print(shipper.prec_graph)

    title_print("ploting and printing the schedule")
    for i, shipment in enumerate(shipper.schedule):
        print(f"No.{i+1}:\t{shipment}")

    show_opt_schedule(tasks=shipper.schedule, cost_function_type="sum")
