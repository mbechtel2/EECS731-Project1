################################################################################
#
# File: project1
# Author: Michael Bechtel
# Date: September 7, 2020
# Class: EECS 731
# Description: Combine datasets on U.S state populations, urbanization 
#              indexes and vehicle accidents and attempt to determine if there
#              is any correlation between the 3 statistics.
# 
################################################################################

# Imports
import pandas as pd
import matplotlib.pyplot as plt

# Read state population dataset
#   Get population estimates from 2012 (remove other unused datapoints)
#   Rename column headers
#   Scale state population sizes down by a factor of 1 million
state_populations = pd.read_csv("../data/raw/nst-est2019-alldata.csv")
state_populations = state_populations.loc[5:55,("NAME","POPESTIMATE2012")]
state_populations = state_populations.rename(columns={"NAME":"state", "POPESTIMATE2012":"population"})
state_populations.loc[:,"population"] /= 1000000

# Read state urbanization index dataset
#   Remove unused datapoints
state_urbanizations = pd.read_csv("../data/raw/urbanization-state.csv")
state_urbanizations = state_urbanizations.drop([2,12,37,42])

# Read state vehicular accidents dataset
#   Only keep total accidents (remove other unused datapoints)
#   Rename column headers
state_accidents = pd.read_csv("../data/raw/bad-drivers.csv")
state_accidents = state_accidents.loc[:,("State", "Number of drivers involved in fatal collisions per billion miles")]
state_accidents = state_accidents.rename(columns={"State":"state", "Number of drivers involved in fatal collisions per billion miles":"accidents"})

# Create merged dataset for population vs accidents
#   Sort dataset by population
population_vs_accidents = pd.merge(state_populations, state_accidents, on="state")
population_vs_accidents = population_vs_accidents.sort_values(by="population")
population_vs_accidents.to_csv("../data/processed/population_vs_accidents.csv")

# Create merged dataset for urbanization index vs accidents
#   Sort dataset by urbanization index
urbanindex_vs_accidents = pd.merge(state_urbanizations, state_accidents, on="state")
urbanindex_vs_accidents = urbanindex_vs_accidents.sort_values(by="urbanindex")
urbanindex_vs_accidents.to_csv("../data/processed/urbanindex_vs_accidents.csv")

# Plot accidents vs state population
graph_range = range(51)
_,graphs = plt.subplots(1,2)
graphs[0].plot(graph_range, 'population', data=population_vs_accidents)
graphs[0].plot(graph_range, 'accidents', data=population_vs_accidents)
graphs[0].set_ylim([0,25])
graphs[0].legend()

# Plot accidents vs state urbanization index
graphs[1].plot(graph_range, 'urbanindex', data=urbanindex_vs_accidents)
graphs[1].plot(graph_range, 'accidents', data=urbanindex_vs_accidents)
graphs[1].set_ylim([0,25])
graphs[1].legend()

# Save and display both graphs
plt.savefig("../visualizations/accident_correlations.png", bbox_inches='tight')
plt.show()