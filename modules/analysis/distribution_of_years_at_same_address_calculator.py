import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import FuncFormatter

from modules.shared.common.paths import PANEL_DATA_OUTPUT_PATH
from modules.shared.models.panel_data_entry import PanelDataEntry
from modules.repository.src.constants.panel_data_table import (
    PANEL_DATA_TABLE_NAME,
    PANEL_DATA_TABLE_COLUMNS_NAMES,
)
from modules.repository.src.utility.get_table_entries import get_table_entries

db = PANEL_DATA_OUTPUT_PATH / "db" / "STABLE - PANEL - Oct 22 - 221440.db"

entries = get_table_entries(
    db, PANEL_DATA_TABLE_NAME
)  # , " WHERE year = 1900 OR year = 1899")

panel_data_entries: list[PanelDataEntry] = []
for row in entries:
    entry_data = dict(zip(PANEL_DATA_TABLE_COLUMNS_NAMES, row))
    entry = PanelDataEntry(**entry_data)
    panel_data_entries.append(entry)

zwischen_result = dict()
for entry in panel_data_entries:
    key = f"{entry.original_names}-{entry.address}"
    if key not in zwischen_result:
        zwischen_result[key] = 1
    else:
        zwischen_result[key] += 1

s = sorted(zwischen_result.items(), key=lambda x: x[1], reverse=True)

result = dict()
for e in s:
    nr_of_years_found = e[1]
    persons_count = 0
    if nr_of_years_found not in result:
        result[nr_of_years_found] = 1
    else:
        result[nr_of_years_found] += 1

print(f"Für 1 Jahr: {result[1]}")
result.pop(1)

print(f"Für 2 Jahre: {result[2]}")
result.pop(2)

print(f"Für 3 Jahre: {result[3]}")
result.pop(3)

x = list(result.keys())
y = list(result.values())

# Create the plot
plt.figure(figsize=(10, 5))
plt.bar(x, y, color="skyblue")

plt.xlabel("Jahren an gleicher Adresse")
plt.ylabel("Anzahl Personen")
plt.title("Wie viele Personen waren an x Jahren an derselben Adresse?")

# Set Y-axis limits for better granularity
plt.ylim(0, max(y) * 1.1)  # Adding some padding above the max value

# Set more granular Y-axis ticks
y_ticks = np.arange(0, max(y) + 2000, 2000)  # Adjust the step size as needed
plt.yticks(y_ticks)


# Function to format y-axis labels with commas
def format_func(value, tick_number):
    return f"{int(value):,}"


# Use FuncFormatter to apply the formatting function
plt.gca().yaxis.set_major_formatter(FuncFormatter(format_func))

# Show the plot
plt.xticks(x)  # Ensure all keys are marked on the X-axis
plt.grid(axis="y")  # Add gridlines for better readability
plt.show()
