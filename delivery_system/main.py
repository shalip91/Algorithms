from client_packer import ClientPacker


if __name__ == '__main__':
    packer = ClientPacker(filename='orders.json',
                          ship_size=12,
                          reg_w_max_size=10,
                          reg_v_max_value=5)

    for order in packer.orders:
        print(order)

    print("after calculating")
    packer.calculate_shipments()
