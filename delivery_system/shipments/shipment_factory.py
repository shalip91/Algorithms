import math
from abc import ABC, abstractmethod
from .knapsack_algoritms.knapsack_nVSv import *
from .knapsack_algoritms.knapsack_nVSw import *
from .shipment import Shipment

"""****************************************************************************
*******************************************************************************
in this file, i am implementing the Factory Design Pattern
for each case of calculation, i am suggesting a variation of knapsack solver:

-   for the "w-reg" i am using the O(Wn) Dynamic-Programming version that consider
    the "W" as constant of the system therefore the the complexity reduces to O(n). 
    
-   for the "v-reg" i am using the O(n^2V) Dynamic-Programming version that consider
    the "V" as constant of the system therefore the the complexity reduces to O(n). 
    
-   for the "prime" i am using the O(n^2V*) Dynamic-Programming approximation. 
*******************************************************************************
****************************************************************************"""

class Creator(ABC):
    @abstractmethod
    def create(self):
        pass

class WRegShipment(Creator):
    """ create a shipment base of the
        O(Wn) Dynamic-Programming knapsack """
    @staticmethod
    def create(order, order_limits):
        # call the knapsack solver
        _, taken_idxs = knapsack_nVSw(elements_W=order.get_items_weight(),
                                      elements_V=order.get_items_value(),
                                      sack_size=order_limits['reg_w_max_size'])
        # create the new inventory according to solver result
        new_inventory = [item for i, item in enumerate(order.inventory) if i in taken_idxs]
        return Shipment(order.client_name, order.distance, order.type,
                        order.ai, new_inventory)


class VRegShipment(Creator):
    """ create a shipment base of the
        O(n^2V) Dynamic-Programming knapsack """
    @staticmethod
    def create(order, order_limits):
        # remove all the expensive items
        order.inventory = list(filter(
            lambda item: item.value <= order_limits['reg_v_max_value'], order.inventory))

        if len(order.inventory) == 0:
            return None
        # call the knapsack solver
        _, taken_idxs = knapsack_nVSv(elements_W=order.get_items_weight(),
                                      elements_V=order.get_items_value(),
                                      sack_size=order_limits['ship_size'])
        # create the new inventory according to solver result
        new_inventory = [item for i, item in enumerate(order.inventory) if i in taken_idxs]
        return Shipment(order.client_name, order.distance, order.type,
                        order.ai, new_inventory)


class PrimeShipment(Creator):
    """ create a shipment base of the
        O(n^2V*) Dynamic-Programming knapsack approximation"""
    @staticmethod
    def create(order, order_limits):
        elements_v = order.get_items_value()
        # calculate "b" - the factor of each element's value
        b = (order.ai / (2*len(elements_v))) * max(elements_v)
        # update the value to be val/b only if b > 1, otherwise the problem will get worse
        if b > 1:
            elements_v = [round(v/b) for v in elements_v]
        # call the knapsack solver
        _, taken_idxs = knapsack_nVSv(elements_W=order.get_items_weight(),
                                      elements_V=elements_v,
                                      sack_size=order_limits['ship_size'])
        # create the new inventory according to solver result
        new_inventory = [item for i, item in enumerate(order.inventory) if i in taken_idxs]
        return Shipment(order.client_name, order.distance, order.type,
                        order.ai, new_inventory)


class ShipmentFactory:
    creatorsMap = {"w-reg": WRegShipment(), "v-reg": VRegShipment(), "prime": PrimeShipment()}
    @staticmethod
    def create(order, order_limits):
        """this will take the corresponding creator and will apply the Ctor"""
        return ShipmentFactory.creatorsMap[order.type].create(order, order_limits)
