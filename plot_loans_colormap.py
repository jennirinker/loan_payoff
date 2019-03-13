# -*- coding: utf-8 -*-
"""Overlay of total payments over loan breakdown
"""
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# load the data and massage it
loan_csv = 'loan_df.csv'
loan_df = pd.read_csv(loan_csv).set_index('index')
loan_df.index = pd.to_datetime(loan_df.index)
pay_csv = 'pay_df.csv'
pay_df = pd.read_csv(pay_csv).set_index('date')
pay_df.index = pd.to_datetime(pay_df.index)
loan_names = loan_df.columns[::2].map(lambda s: s.rstrip(' .P'))  # unique list of loans
short_names = {'sallie mae': 'SaMa',
               'nelnet - A': 'NeNe-A',
               'nelnet - B': 'NeNe-B',
               'nelnet - C': 'NeNe-C',
               'nelnet - D': 'NeNe-D',
               'AK advantage': 'AK Adv',
               'wells fargo - 1': 'WF-1',
               'wells fargo - 101': 'WF-101',
               'wells fargo - 102': 'WF-102',
               'wells fargo - 103': 'WF-103'}
interest = {'sallie mae': 6.8,
               'nelnet - A': 6.8,
               'nelnet - B': 6.8,
               'nelnet - C': 6.8,
               'nelnet - D': 6.8,
               'AK advantage': 7.3,
               'wells fargo - 1': 3.25,
               'wells fargo - 101': 7.74,
               'wells fargo - 102': 4.74,
               'wells fargo - 103': 4.74}
ordered_loans = ['AK advantage', 'wells fargo - 101', 'nelnet - C', 'nelnet - B',
                 'sallie mae', 'nelnet - D', 'nelnet - A', 'wells fargo - 102',
                 'wells fargo - 103', 'wells fargo - 1']  # payment order
grey_1 = '0.10'  # dark
grey_2 = '0.20'  # not so dark
grey_3 = '0.3'  # is this even grey anymore
ax_ht, ax_sep = 0.074, 0.08  # axes height and seperation for loans
yoffset, xoffset = 0.12, 0.11  # overall x and y offsets

# =================== INITIALIZE THE FIGURE ===================

fig = plt.figure(1, figsize=(10, 6))
plt.clf()

# =================== YEARS UNDER IT ALL ===================

ax = plt.axes([xoffset, yoffset - 0.01, 0.8, 0.86])
idx_years = [np.argmax(loan_df.index > str(year)) for year in range(2012, 2016)]
for iy, year in enumerate(idx_years):
    ax.plot([year, year], [0, 1],
            color=grey_3, linewidth=2.5)
    ax.text(year + 0.3, 0.995, f'{iy + 2012:.0f}',
            horizontalalignment='left', verticalalignment='top',
            fontsize=13, color=grey_2)
ax.set_xlim([0, loan_df.shape[0]])
ax.set_ylim([0, 1])
plt.axis('off')

# =================== LOANS BY AXIS ===================

for i_loan, loan_name in enumerate(ordered_loans[::-1]):
    ax_df = loan_df[[loan_name + s for s in [' .P', ' .I']]]
    ax = plt.axes([xoffset, yoffset + i_loan * ax_sep,
                   0.8, ax_ht])
    cmesh = ax.pcolormesh(range(loan_df.index.size + 1), range(3),
                          ax_df.values.T,
                          vmin=0, vmax=8500)
    plt.axis('off')
    ax.text(-0.07, 0.7, short_names[loan_name],
            horizontalalignment='center', verticalalignment='center',
            transform=ax.transAxes, fontsize=11, color=grey_2)
    ax.text(-0.07, 0.3, f'{interest[loan_name]}%',
            horizontalalignment='center', verticalalignment='center',
            transform=ax.transAxes, fontsize=10, color=grey_2)

    if i_loan == 2:
        ax.text(30, 0.5, 'Principal',
                horizontalalignment='left', verticalalignment='center',
                fontsize=12, color='w')
        ax.text(27, 1.5, 'Interest',
                horizontalalignment='left', verticalalignment='center',
                fontsize=12, color='w')

# =================== OVERALL ===================

ax = plt.axes([xoffset, yoffset, 0.8, (len(loan_names) - 1) * ax_sep + ax_ht])
ax.set_facecolor('none')
total_paid = pay_df.payment.values.sum()
plt.plot(np.cumsum(np.r_[0, pay_df.payment.values]),
         'w', linewidth=6.5, alpha=1)
plt.plot(np.cumsum(np.r_[0, pay_df.payment.values]),
         'darkred', linewidth=5, alpha=1)
ax.set_ylim([0, total_paid])
ax.set_xlim([0, pay_df.payment.values.size])
plt.yticks(np.linspace(0, total_paid, 11),
           labels=[f'${x/1000:.0f}k' for x in
                   np.linspace(0, total_paid, 11)])
ax.yaxis.tick_right()
ax.xaxis.set_visible(False)
[ax.spines[edge].set_visible(False) for edge in ['top', 'left', 'bottom', 'right']]

ax.tick_params(axis='y', which='major', pad=22)
for tick in ax.yaxis.get_major_ticks():
    tick.tick1line.set_markersize(0)
    tick.tick2line.set_markersize(0)
    tick.label2.set_verticalalignment('center')
    tick.label2.set_horizontalalignment('center')
    tick.label2.set_fontsize(14)
    tick.label2.set_color('darkred')

# =================== COLORBAR ===================

cbar_ax = plt.axes([0.3, 0.035, 0.4, 0.04])  # down center
cb = plt.colorbar(cmesh, cax=cbar_ax, orientation='horizontal')
cbar_ax.axis('off')
cbar_ax.text(-0.01, 0.5, '$0k',
             horizontalalignment='right', verticalalignment='center',
             transform=cbar_ax.transAxes, fontsize=11, color=grey_2)
cbar_ax.text(1.01, 0.5, '$8.5k',
             horizontalalignment='left', verticalalignment='center',
             transform=cbar_ax.transAxes, fontsize=11, color=grey_2)
cb.outline.set_visible(False)

# =================== SAVE THE BEAUTY ===================

fig.savefig(os.path.basename(__file__).replace('.py', '.png'), dpi=200)
