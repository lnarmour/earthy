#!/usr/local/bin/python

import sys
import os
import numpy as np
from functools import reduce
from matplotlib import pyplot as plt
from scipy import stats

class Metric():

  def __init__(self, m_id, name, description):
    self.id = int(m_id) # id
    self.name = name
    self.description = description

  def __str__(self):
    return '[{}] : {} ({})'.format(self.id, self.description, self.name)


def init_ini(filename='data.ini'):
  defs = {}
  with open(filename, 'r') as f:
    ini = [l.strip('\n') for l in f.readlines()]

  for m_id,l in enumerate(ini):
    description, name = l.split(':')
    defs[name] = Metric(m_id, name, description)

  return defs


def load_data(filename='data.csv'):
  apps = []
  with open(filename, 'r') as f:
    data = [l.strip('\n') for l in f.readlines()]
  
  for app_line in data[1:]:
    vector = [float(v) for v in app_line.split(',')[1:] if v]
    apps.append(vector)

  apps = np.array(apps)
  return apps


def main(script_name, metric_1=None, metric_2=None):

  metric_defs = init_ini('data.ini')
  metric_index = {metric_defs[k].id: k for k in metric_defs}
  if os.getenv('VERBOSE'):
    for m in metric_defs:
      print(metric_defs[m])

  data = load_data('data.csv')

  P = 8
  fig, axs = plt.subplots(P, P, sharex='col', sharey='row')
  fig.set_figheight(8)
  fig.set_figwidth(8)

  for i in range(P):
    m1 = metric_index[i]
    axs[i, 0].set_ylabel(m1)
    for j in range(P):
      if j>i:
        axs[i, j].set_visible(False)
        axs[i, j].set_visible(False)
        continue

      m2 = metric_index[j]
      # subplot for each combo
      keys1 = [metric_defs[k].id for k in metric_defs if m1 == k]
      keys2 = [metric_defs[k].id for k in metric_defs if m2 == k]

      H = np.add.reduce(data[:,min(keys1):max(keys1)+1], axis=1)
      V = np.add.reduce(data[:,min(keys2):max(keys2)+1], axis=1)

      axs[i, j].scatter(H, V, marker='.')
      axs[i, j].plot([0,1], [0,1], 'k--', alpha=0.5)

      axs[i, j].set_xlim(-0.02, 1.02)
      axs[i, j].set_ylim(-0.02, 1.02)
      axs[i, j].set_aspect('equal', adjustable='box')

  for j in range(P):
    m2 = metric_index[j]
    axs[-1, j].set_xlabel(m2)

  plt.savefig('all.png')


def do_pearson_corr():
  metric_defs = init_ini('data.ini')
  metric_index = {metric_defs[k].id: k for k in metric_defs}
  if os.getenv('VERBOSE'):
    for m in metric_defs:
      print(metric_defs[m])

  data = load_data('data.csv')

  P = 8

  def_pad = max([len(metric_index[i]) for i in range(8)])

  for i in range(P):
    print('{:{}} |  '.format(metric_index[i], def_pad), end='')
    for j in range(0, i+1):
      pc = stats.pearsonr(data[:,i], data[:,j])[0]
      pad = '' if pc < 0 else ' '
      print('{}{:.4f}  '.format(pad, pc), end='')
    print()

  print('{:{}}  {}'.format('', def_pad, '-' * (def_pad + P*9)))
  print('{:{}}     '.format('', def_pad), end='')
  for i in range(P):
    print('{:{}}  '.format(metric_index[i], 7), end='')
  print()











if __name__ == '__main__':
  args = sys.argv
  do_pearson_corr()
  #main(*args)

