from client_packer import ClientPacker
from client_shipper import ClientShipper


if __name__ == '__main__':

    packer = ClientPacker(filename='orders.json',
                          ship_size=12,
                          reg_w_max_size=10,
                          reg_v_max_value=5)
    print("*****************************************\n"
          "orders before calculating the shipments:\n"
          "****************************************")
    for o in packer.orders: print(o)

    print("\n\n*****************************************\n"
          "orders after calculating the shipments:\n"
          "****************************************")
    for s in packer.calculate_shipments(): print(s)

    shipper = ClientShipper(shipments=packer.shipments,
                            q_diff_factor=0.75,
                            cost_function_type="identity")

    print("\n\n*****************************************\n"
          "           precedence graph\n"
          "****************************************")
    print(shipper.prec_graph)

    print("\n\n*****************************************\n"
          "                 schedule\n"
          "****************************************")
    for vertex in shipper.schedule:
        print(f"name:{vertex.key}")
