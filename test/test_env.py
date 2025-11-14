import numpy as np
import pytest

from env import FactoryEnv


def create_valid_factory_arguments():
    """
    4 nodes
    1 machine
    2 robots
    0 -> input node
    1 -> machine input
    2 -> machine output
    3 -> output node   
    dist = 1 between all nodes
    robot 0 has distance 0 to all nodes
    robot 1 has distance 1 to all nodes 
    machine: input_type=1, output_type=2
    """
    num_robots = 2
    num_nodes = 4
    num_machines = 1

    # simple distance matrix: all ones, shape (num_nodes, num_nodes)
    distances = np.ones((num_nodes, num_nodes), dtype=float)

    # each robot has a dict: node_index -> distance
    robot_initial_distances = [
        {i: 0.0 for i in range(num_nodes)},  # robot 0 has distance 0 to all nodes
        {i: 1.0 for i in range(num_nodes)},  # robot 1 at distance 1 to all nodes
    ]

    # input and output nodes
    input_nodes = [0]
    output_nodes = [3]

    # machines
    num_machines = 1
    machine_transitions = [
        {1: 2},  # machine 0: input node 1 -> output node 2
    ]

    return dict(
        num_robots=num_robots,
        robot_initial_distances=robot_initial_distances,
        num_nodes=num_nodes,
        distances=distances,
        input_nodes=input_nodes,
        output_nodes=output_nodes,
        num_machines=num_machines,
        machine_transitions=machine_transitions,
    )


def test_factory_env_constructor():
    # create valid factory env arguments
    args = create_valid_factory_arguments()
    # create factory env object
    env = FactoryEnv(**args)

    # check attributes
    assert env.num_robots == 2
    assert len(env.robot_initial_distances) == 2
    for robot_distances in env.robot_initial_distances:
        assert len(robot_distances) == env.num_nodes
    
    assert env.num_nodes == 4
    assert env.distances.shape == (env.num_nodes, env.num_nodes)
    assert env.input_nodes == [0]
    assert env.output_nodes == [3]

    # node_types: input node -> 0, machine input -> input_type, machine output -> output_type, output node -> 5
    assert env.node_types[0] == 0          # input node
    assert env.node_types[1] == 1          # machine input node
    assert env.node_types[2] == 2          # machine output node
    assert env.node_types[3] == 3          # output node
