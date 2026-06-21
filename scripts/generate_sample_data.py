import math
import csv
from pathlib import Path

output_path = Path("sample_data/sample_walk.csv")
output_path.parent.mkdir(parents=True, exist_ok=True)

dt = 0.1
num_rows = 50
stride_period = 1.2
omega = 2 * math.pi / stride_period

headers = [
    "time",
    "hip_flexion_l", "knee_angle_l", "ankle_angle_l",
    "hip_flexion_r", "knee_angle_r", "ankle_angle_r",
    "hip_flexion_l_moment", "knee_angle_l_moment", "ankle_angle_l_moment",
    "hip_flexion_r_moment", "knee_angle_r_moment", "ankle_angle_r_moment",
    "hip_flexion_l_velocity", "knee_angle_l_velocity", "ankle_angle_l_velocity",
    "hip_flexion_r_velocity", "knee_angle_r_velocity", "ankle_angle_r_velocity",
    "left_foot_grf_si_norm", "right_foot_grf_si_norm",
]

def half_sine_grf(phase):
    value = math.sin(phase)
    return max(0.0, value) * 15.0

rows = []

for i in range(num_rows):
    t = i * dt

    left_phase = omega * t
    right_phase = left_phase + math.pi

    row = {
        "time": round(t, 3),

        "hip_flexion_l": 10.0 * math.sin(left_phase),
        "knee_angle_l": 25.0 + 15.0 * math.sin(left_phase + 0.5),
        "ankle_angle_l": -5.0 + 8.0 * math.sin(left_phase - 0.4),

        "hip_flexion_r": 10.0 * math.sin(right_phase),
        "knee_angle_r": 25.0 + 15.0 * math.sin(right_phase + 0.5),
        "ankle_angle_r": -5.0 + 8.0 * math.sin(right_phase - 0.4),

        # Synthetic normalized moments, roughly Nm/kg
        "hip_flexion_l_moment": 0.6 * math.sin(left_phase + 0.2),
        "knee_angle_l_moment": 0.4 * math.sin(left_phase + 0.7),
        "ankle_angle_l_moment": 0.8 * math.sin(left_phase - 0.5),

        "hip_flexion_r_moment": 0.6 * math.sin(right_phase + 0.2),
        "knee_angle_r_moment": 0.4 * math.sin(right_phase + 0.7),
        "ankle_angle_r_moment": 0.8 * math.sin(right_phase - 0.5),

        # Synthetic angular velocities
        "hip_flexion_l_velocity": 10.0 * omega * math.cos(left_phase),
        "knee_angle_l_velocity": 15.0 * omega * math.cos(left_phase + 0.5),
        "ankle_angle_l_velocity": 8.0 * omega * math.cos(left_phase - 0.4),

        "hip_flexion_r_velocity": 10.0 * omega * math.cos(right_phase),
        "knee_angle_r_velocity": 15.0 * omega * math.cos(right_phase + 0.5),
        "ankle_angle_r_velocity": 8.0 * omega * math.cos(right_phase - 0.4),

        "left_foot_grf_si_norm": half_sine_grf(left_phase),
        "right_foot_grf_si_norm": half_sine_grf(right_phase),
    }

    rows.append(row)

with output_path.open("w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()

    for row in rows:
        writer.writerow({
            key: round(value, 5) for key, value in row.items()
        })

print(f"Generated {output_path}")