# Shared Street Conflict Assessment Toolkit

## Overview

This project is a GIS-based Python toolkit for assessing pedestrian-cyclist conflict scores on shared streets and simulating topology-based street redesign interventions.

The toolkit translates observed street conditions into a weighted conflict scoring system. It evaluates each street segment based on spatial and design attributes such as pedestrian width, cycling width, shared-space condition, hotspot proximity, ground marking, physical divider, vegetation, fences, and canopy constraints.

After calculating the baseline conflict score, the toolkit identifies different street conflict topologies and tests multiple redesign interventions. Each intervention updates selected GIS attributes, recalculates the post-intervention conflict score, and records the estimated implementation cost. The final output supports before-and-after comparison of street redesign scenarios.

## Project Background

Shared streets often involve overlapping pedestrian and cycling movements, unclear spatial boundaries, insufficient path width, or conflicts caused by barriers, greenery, entrances, bus stops, and other street-side conditions. These conflicts are usually difficult to evaluate through visual observation alone.

This project explores how GIS attribute data and rule-based scoring can support a more systematic assessment of shared-street conflicts and help planners compare possible street improvement strategies.

## Workflow

1. Prepare the GIS input database.
2. Normalize street-segment attributes.
3. Calculate the baseline conflict score.
4. Classify street segments into conflict topologies.
5. Apply topology-specific redesign interventions.
6. Recalculate post-intervention conflict scores.
7. Export final comparison tables for different street types.

## Conflict Score Indicators

The baseline conflict score is calculated using a weighted indicator system:

| Indicator                   | Description                                               |
| --------------------------- | --------------------------------------------------------- |
| Shared-space condition      | Whether pedestrian and cycling movement overlap           |
| Cycling width               | Available or estimated width for cycling movement         |
| Pedestrian width            | Available or estimated width for pedestrian movement      |
| Hotspot proximity           | Proximity to entrances and bus stops                      |
| Ground marking              | Quality of surface marking or lane visual separation      |
| Divider                     | Presence or absence of physical/spatial separation        |
| Vegetation                  | Type and intensity of verge or buffer vegetation          |
| Fence and canopy constraint | Presence of fences, canopy, or other physical constraints |

## Street Conflict Topologies

The toolkit classifies street segments into different topology types:

| Topology | Description                                                                 |
| -------- | --------------------------------------------------------------------------- |
| Topo A   | Shared-space condition with limited separation or missing secondary path    |
| Topo B   | Street segment with multiple movement spaces but insufficient width balance |
| Topo C   | Segment constrained by fences, canopy, or other physical barriers           |
| Topo D   | No-path condition requiring new pedestrian/cycling infrastructure           |

## Intervention Scenarios

The intervention scripts test whether a redesign method is spatially feasible based on available verge and buffer width. If feasible, the script updates selected attributes and recalculates the conflict score.

| Scenario | Main logic                                        |
| -------- | ------------------------------------------------- |
| A1       | Add basic ground marking                          |
| A2       | Apply stronger colored surface marking            |
| A3       | Add physical or spatial divider                   |
| A4       | Create dedicated cycling/shared-space improvement |
| B1       | Improve cycling width condition                   |
| B2       | Improve pedestrian width condition                |
| B3       | Rebalance pedestrian and cycling space            |
| C1       | Reduce fence/canopy-related constraint            |
| D1       | Add minimum shared path                           |
| D2       | Add marked shared path                            |
| D3       | Add separated and marked pedestrian/cycling path  |

## Repository Structure

```text
scripts/
├── 00_prepare_baseline_conflict_scores.py
├── A1_add_basic_lane_marking.py
├── A2_apply_colored_surface_marking.py
├── A3_add_physical_divider.py
├── A4_create_dedicated_cycle_space.py
├── B1_widen_cycle_space.py
├── B2_widen_pedestrian_space.py
├── B3_rebalance_pedestrian_cycle_space.py
├── C1_remove_barrier_or_canopy_conflict.py
├── D1_add_minimum_shared_path.py
├── D2_add_marked_shared_path.py
├── D3_add_separated_cycle_pedestrian_path.py
└── 99_export_conflict_score_outputs.py
```

## Outputs

The toolkit generates GIS output layers and attribute tables containing:

* Baseline conflict score
* Conflict topology classification
* Feasibility of each redesign intervention
* Post-intervention conflict score
* Estimated intervention cost
* Final before-and-after comparison table

## Tools and Environment

* Python
* ArcPy
* ArcGIS Pro
* File Geodatabase
* GIS attribute table processing
* Rule-based spatial analysis

## Relevance

This project demonstrates how urban design knowledge, GIS-based spatial analysis, and Python scripting can be combined to support evidence-based street redesign. It is relevant to smart city planning, active mobility, walkability and bikeability assessment, urban safety analysis, and spatial decision-support systems.
