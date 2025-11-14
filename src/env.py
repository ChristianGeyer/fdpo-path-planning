import numpy as np

# src/fdpo/env.py

import numpy as np

class Machine:
    """
    attributes:
        size: number of input-output channels
        machine_type: tuple (input_type, output_type)
        transitions: dict mapping input nodes to output nodes
    """
    def __init__(self, machine_type: tuple[int, int], transitions: dict[int, int]):
        self.size = len(transitions)
        self.machine_type = machine_type  # (input_type, output_type)
        self.transitions = transitions    # mapping from input nodes to output nodes
    
class FactoryEnv:

    """
    structural attributes:

        num_robots: number of robots in the factory
        robot_initial_distances: list of dicts with initial distances from each robot to each node of the factory

        num_nodes: number of nodes in the factory
        distances: distance matrix (num_nodes, num_nodes) between nodes

        input_nodes: list of input nodes
        output_nodes: list of output nodes

        num_machines: number of machines in the factory
        machine_transitions: list of dicts mapping input nodes to output nodes for each machine

        machines: list of machine objects -> compute from the above
        node_types: dict mapping nodes to types -> compute from the above
        actions: dict mapping (box_type, node_type) to list of valid target nodes -> compute from the above

    dynamic attributes:

        robots: list of robot objects
        boxes: list of box objects
    """
    def __init__(self, num_robots: int, robot_initial_distances: list[dict[int, float]],
                num_nodes: int, distances: np.ndarray,
                input_nodes: list[int], output_nodes: list[int],
                num_machines: int, machine_transitions: list[dict[int, int]]):
        self.num_robots = num_robots
        self.robot_initial_distances = robot_initial_distances
       
        self.num_nodes = num_nodes
        self.distances = distances
        
        self.input_nodes = input_nodes
        self.output_nodes = output_nodes

        self.num_machines = num_machines
        
        # create list of machine-objects
        self.machines = []
        for i in range(num_machines):
            machine = Machine((2*i+1, 2*i+2), machine_transitions[i])
            self.machines.append(machine)

        # create dict of node_types
        self.node_types = {}
        # input nodes
        for node in input_nodes:
            self.node_types[node] = 0  # input node type
        # machine nodes
        for i in range(num_machines):
            machine = self.machines[i]
            input_type, output_type = machine.machine_type
            for input_node, output_node in machine.transitions.items():
                self.node_types[input_node] = input_type
                self.node_types[output_node] = output_type
        # output nodes
        for node in output_nodes:
            self.node_types[node] = 2*num_machines + 1  # output node type

        # validate inputs
        #self._validate_init_inputs()

    """
    def _validate_init_inputs(self):
        # check robot_initial_distances length
        assert len(self.robot_initial_distances) == self.num_robots, "robot_initial_distances length does not match num_robots"

        # check node_types length
        assert len(self.node_types) == self.num_nodes, "node_types length does not match num_nodes"

        # check distances shape
        assert self.distances.shape == (self.num_nodes, self.num_nodes), "distances shape does not match (num_nodes, num_nodes)"

        # check that machine nodes, input nodes and output nodes are not conflicting
        total_nodes = []
        for in_node in self.input_nodes: # input nodes
            total_nodes.append(in_node)
        for out_node in self.output_nodes: # output nodes
            total_nodes.append(out_node)
        for machine in self.machines: # machine nodes
            for in_node, out_node in machine.transitions.items():
                total_nodes.append(in_node)
                total_nodes.append(out_node)
        # each node should be unique
        assert len(total_nodes) == len(set(total_nodes)), "Conflicting node definitions found."
        # all nodes should be represented
        assert len(total_nodes) == self.num_nodes, "Some nodes are not represented."
       
        # check output node type
        assert all(self.node_types[node] == 2*self.num_machines + 1 for node in self.output_nodes), "Output nodes do not have correct type."
        """