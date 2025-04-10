import sys
import pandas as pd
import numpy as np
import xgboost
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import argparse
import warnings
from sklearn.metrics import roc_curve, auc
warnings.filterwarnings('ignore')

import PyIO
import PyPluMA
class BoxWhiskerPlugin:
 def input(self, inputfile):
  self.parameters = PyIO.readParameters(inputfile)
 def run(self):
     pass
 def output(self, outputfile):
  genus = self.parameters["genus"]
  #biasedOutput.to_csv('biasedOutput.tsv', sep='\t', index=False)
  biasedOutput = pd.read_csv(PyPluMA.prefix()+"/"+self.parameters["stats"], sep='\t', header=0)

  # Use biasedOutput dataframe to make a simple box and whisker plot
  # Set data in the biasedOutput dataframe to numeric
  biasedOutput = biasedOutput.apply(pd.to_numeric)

  # Create the figure and two subplots (axes) with shared x-axes
  fig, (ax, ax2) = plt.subplots(2, 1, sharex=True, figsize=(10, 8))
  fig.subplots_adjust(hspace=0.1)  # Adjust space between axes

  # Plotting the data - vertical box plots
  ax.boxplot([biasedOutput[genus], biasedOutput['Other']], labels=[genus, 'Other'])
  ax2.boxplot([biasedOutput[genus], biasedOutput['Other']], labels=[genus, 'Other'])

  # Define upper and lower range for the y-axis on both plots to zoom into different data ranges
  ax.set_ylim(480, 530)  # Set this range to capture outlier or higher value ranges
  ax2.set_ylim(0, 45)    # Set this range to capture most of the data

  # Hide the spines between ax and ax2
  ax.spines['bottom'].set_visible(False)
  ax2.spines['top'].set_visible(False)
  ax.xaxis.tick_top()
  ax.tick_params(labeltop=False)  # Don't put tick labels at the top
  ax2.xaxis.tick_bottom()

  # Diagonal lines to indicate the break in the plot
  d = .015  # Diagonal line length
  kwargs = dict(transform=ax.transAxes, color='k', clip_on=False)
  ax.plot((-d, +d), (-d, +d), **kwargs)        # Top-left diagonal
  ax.plot((1 - d, 1 + d), (-d, +d), **kwargs)  # Top-right diagonal

  kwargs.update(transform=ax2.transAxes)  # Switch to the bottom axes
  ax2.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # Bottom-left diagonal
  ax2.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # Bottom-right diagonal

  # Add a main title to the figure
  fig.suptitle('Box and Whisker Plot of Caenorhabditis and Other Origin\nCounts with 10 Replicates', fontsize=16)

  # Show the plot
  plt.show()
  plt.savefig(outputfile, dpi=1200, bbox_inches='tight')
  plt.close()


