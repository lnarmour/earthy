#!/usr/local/bin/python

import sys
import os
import numpy as np
from functools import reduce
from matplotlib import pyplot as plt
from scipy import stats

class Metric():

    def __init__(self, m_id, name, description, max_val):
        self.id = int(m_id) # id
        self.name = name
        self.description = description
        self.max_val = float(max_val) if max_val else None

    def __str__(self):
        return '[{}] : {} ({})'.format(self.id, self.description, self.name)


def init_ini(filename='data.ini'):
    defs = {}
    with open(filename, 'r') as f:
        ini = [l.strip('\n') for l in f.readlines()]

    for m_id,l in enumerate(ini):
        description, name, max_val = l.split(':')
        defs[name] = Metric(m_id, name, description, max_val)

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


def main():
    metric_defs = init_ini('data.ini')
    metric_index = {metric_defs[k].id: k for k in metric_defs}
    if os.getenv('VERBOSE'):
        for m in metric_defs:
            print(metric_defs[m])

    data = load_data('data_numeric.csv')
    do_pearson_corr(data, metric_defs, metric_index)
    plot_distributions(data, metric_defs, metric_index)
    plot_pairs(data, metric_defs, metric_index)


def plot_distributions(data, metric_defs, metric_index, P=7):
    os.makedirs("plots", exist_ok=True)

    for i in range(P):
        print('working on distribution {}[{}] pdf'.format(metric_index[i], i))
        metric = data[:, i][data[:, i] >= 0] # ignore values of -1
        metric = prune_outliers(metric)
        hist, bin_edges = np.histogram(metric)

        #print(data[:, i])
        #print(hist)
        #print(bin_edges)

        fig, ax = plt.subplots()

        pad = (bin_edges[1] - bin_edges[0]) / 2
        width = (max(bin_edges[:-1]) - min(bin_edges)) / plt.rcParams['hist.bins']
        plt.bar(bin_edges[:-1], hist, width=width, color='#0504aa', alpha=0.7)
        plt.xlim(min(bin_edges)-pad, max(bin_edges[:-1])+pad)
        plt.grid(axis='y', alpha=0.75)
        plt.xlabel('Value', fontsize=24)
        plt.xticks(fontsize=24)
        plt.yticks(fontsize=24)
        plt.ylabel('Frequency', fontsize=24)
        #plt.title(metric_defs[metric_index[i]].description, fontsize=14)
        fig.tight_layout()
        plt.savefig('plots/distrib_{}_{}.pdf'.format(i, metric_index[i]))
        plt.clf()



def plot_pairs(data, metric_defs, metric_index, P=7):
    print('working on correlations all pdf')
    fig, axs = plt.subplots(P, P, sharex='col', sharey='row')
    fig.set_figheight(8)
    fig.set_figwidth(8)
    #fig.tight_layout(pad=1.8)

    for i in range(P):
        m1 = metric_index[i]
        axs[i, 0].set_ylabel(m1)
        for j in range(P):
            if j>i:
                axs[i, j].set_visible(False)
                #axs[i, j].text(0.5, 0.5, 'matplotlib', horizontalalignment='center',
                #               verticalalignment='center', transform=axs[i, j].transAxes)
                continue

            m2 = metric_index[j]
            # subplot for each combo
            keys1 = [metric_defs[k].id for k in metric_defs if m1 == k]
            keys2 = [metric_defs[k].id for k in metric_defs if m2 == k]

            L = np.add.reduce(data[:,min(keys1):max(keys1)+1], axis=1)
            R = np.add.reduce(data[:,min(keys2):max(keys2)+1], axis=1)

            H, V = prune_pair(L, R)
            h_max, h_min = np.max(H, axis=0), np.min(H, axis=0)
            v_max, v_min = np.max(V, axis=0), np.min(V, axis=0)
            #H, V = H / h_max, V / v_max

            axs[i, j].scatter(H, V, marker='.')
            #axs[i, j].plot([0,1], [0,1], 'k--', alpha=0.5)

            h_range = h_max - h_min
            v_range = v_max - v_min
            axs[i, j].set_xlim(np.min(H)-0.1*h_range, np.max(H)+0.1*h_range)
            axs[i, j].set_ylim(np.min(V)-0.1*v_range, np.max(V)+0.1*v_range)
            #axs[i, j].set_aspect('equal', adjustable='box')

    for j in range(P):
        m2 = metric_index[j]
        axs[-1, j].set_xlabel(m2)
        #axs[-1, j].tick_params(axis='x', labelrotation=45)

    plt.savefig('plots/all.pdf')


def prune_outliers(data, m=2):
    # filter values greater than m std-devs from the mean
    # assumes that data is 1D
    if len(data.shape) > 1:
        raise Exception('data must be 1D but is {}'.format(data.shape))
    return data[abs(data - np.mean(data)) < m * np.std(data)]


def prune_pair(l, r, m=2):
    data = np.array([l, r]).transpose()
    # filter pairs where either val is greater than m std-devs from the mean
    c = abs(data - np.mean(data, axis=0)) < m * np.std(data, axis=0)
    ret = data[np.logical_and.reduce(c, axis=1), :]
    return ret[:,1], ret[:,0]


def do_pearson_corr(data, metric_defs, metric_index, P=7):
    print('working on pearson correlation coefficients')
    def_pad = max([len(metric_index[i]) for i in range(P)])

    for i in range(P):
        print('{:{}} |  '.format(metric_index[i], def_pad), end='')
        for j in range(0, i+1):
            L, R = prune_pair(data[:,i], data[:,j])
            pc = stats.pearsonr(L, R)[0]
            pad = '' if pc < 0 else ' '
            print('{}{:.4f}  '.format(pad, pc), end='')
        print()

    print('{:{}}  {}'.format('', def_pad, '-' * (def_pad + P*9)))
    print('{:{}}     '.format('', def_pad), end='')
    for i in range(P):
        print('{:{}}  '.format(metric_index[i], 7), end='')
    print()





if __name__ == '__main__':
  main()

