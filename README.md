## Context

Develop a path planning strategy for (a/many) robot(s) to compete at the robot@factory competition. The competition rules can be found  at [Oficial competition rules 2024](https://github.com/P33a/RobotAtFactory/blob/main/RobotAtFactory_4_0_2024_Rules.pdf).

In the factory, boxes of different colors (R-red, G-green, B-blue) will be placed at the **input warehouse**. The goal is to convert all box colors to B, and place the B-boxes in the **output warehouse**. R-boxes must be transported to **machineA's inputs**, where they will be transformed from R to G and placed at the **machineA's outputs**. G-boxes must be transported to **machineB's inputs**, where they will be transformed from G to B and placed at the **machineB's outputs**.

Three robots will be placed in the factory and transport boxes simultaneously.

## Goal

Train an agent using the reinforcement learning approach to optimize robot decisions in the path-planning problem.

## Current Development Stage

1) Initial project structure created to start developping...
* docs/: files with relevant information about the project
* scripts/: files with relevant implementations that use the project packages
* src/: project packages
* test/: tests for project packages

2) Implemented weighted Graph logic:
* nodes
* adjacency list with neighbors and weights
* dijkstra's shortest distances and paths
* tests

## Next steps

Implement Graph2d logic:
* Node2d
  * nodes with x, y, theta
* Spline2d  
  * connect two Node2d objects with a parameterized curve
  * compute constant velocity parameterization
  * compute arc-length
  * compute expected traverse time based on curvature and max acceleration on curves (slower velocity on high curvature segments)
* Graph2d
  * list of Node2d nodes
  * list of Spline2d edges
  * Graph object with node-ids and weights