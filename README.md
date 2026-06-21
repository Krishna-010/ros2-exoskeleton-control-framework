# ROS2 Modular Lower-Limb Exoskeleton Control & Analysis Framework
> A modular ROS2 software framework demonstrating the complete control and analysis pipeline for a bilateral lower-limb exoskeleton.
A modular ROS2 framework for simulating and analyzing bilateral lower-limb exoskeleton control using synthetic gait data. The framework processes joint kinematics, joint kinetics, and ground reaction forces to estimate gait phase, compute assistive torques, generate motor commands, estimate power consumption, and visualize system behavior using standard ROS2 tools.

## Table of Contents

- Overview
- System Architecture
- Software Pipeline
- Features
- Background
- Project Structure
- ROS Topics
- Custom Messages
- Installation
- Running the Project
- Visualization
- Sample Data
- Future Improvements
- License

## Overview

This project implements a modular ROS2 pipeline for simulating the control architecture of a bilateral lower-limb exoskeleton. Rather than combining all functionality into a single node, the system is divided into independent ROS2 nodes that communicate through topics, making the framework easy to understand, extend, and debug.

The framework reproduces a typical exoskeleton control pipeline:

- Playback of synthetic biomechanical gait data
- Ground reaction force (GRF) based gait phase detection
- Assistive torque computation
- Motor torque conversion using drivetrain gear ratios
- Mechanical and electrical power estimation
- Battery current and runtime estimation
- Real-time visualization using RViz2 and ROS visualization tools

Although the current implementation uses synthetic gait data for demonstration purposes, the modular architecture allows the CSV playback node to be replaced with live sensors in future hardware implementations.

## System Architecture

The framework follows a modular publish-subscribe architecture in ROS2. Each node performs a single responsibility and communicates with other nodes through ROS topics.

```text
                CSV Playback Node
                       │
      ┌────────────────┼────────────────┐
      │                │                │
      ▼                ▼                ▼
 Joint Angles    Joint Moments   Joint Velocities
                       │
                       ▼
                Ground Reaction Force
                       │
                       ▼
               Gait Phase Detection
                       │
                       ▼
             Assistive Torque Controller
                       │
                       ▼
             Motor Command Conversion
                       │
                       ▼
        Power & Battery Monitoring
                       │
                       ▼
             RViz2 Visualization

```
This modular architecture allows each subsystem to be independently developed, tested, and replaced without affecting the rest of the framework.
> Each node follows the single-responsibility principle, allowing individual components to be developed, tested, and replaced independently.

## Software Pipeline

The current implementation processes data through the following sequence:

1. CSV Playback
2. Joint Angle, Joint Moment, Joint Velocity, and GRF publication
3. Gait Phase Detection
4. Assistive Torque Computation
5. Motor Torque Conversion
6. Mechanical and Electrical Power Estimation
7. Battery Current and Runtime Estimation
8. RViz2 Visualization

## Features

### Control

- Bilateral lower-limb processing
- Gait phase detection using GRF
- Hip and ankle assistive torque computation
- Motor torque conversion
- Configurable gear ratios
- Torque saturation

### Analysis

- Mechanical power estimation
- Electrical power estimation
- Battery current estimation
- Runtime estimation

### Software

- Modular ROS2 node architecture
- Custom ROS2 message definitions
- ROS2 launch file support
- Parameter-based configuration
- RViz2 visualization
- rqt_graph compatibility
- rqt_plot compatibility

## Visualization

### ROS Graph

The figure below shows the modular ROS2 node and topic architecture used by the framework.

![ROS Graph](images/rqt_graph.png)

---

### Live Topic Plot

The following plot demonstrates the relationship between joint moment, assistive torque, and motor torque during gait.

![rqt_plot](images/rqt_plot.png)

---

### RViz Visualization

RViz2 is used to visualize assistive torque as ROS visualization markers.

![RViz](images/rviz_marker.png)

## Background

This framework was developed as an extension of my M.S. Robotics capstone project at the Georgia Institute of Technology. The original capstone focused on the feasibility study and design of an integrated bilateral hip–ankle exoskeleton. This ROS2 framework translates that work into a modular software architecture for control, analysis, and visualization, following the design principles used in real robotic systems.