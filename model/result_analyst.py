# -*- coding: utf-8 -*-
# @author: Yuhao Wang
# @email: wangyuhao@shanshu.ai
# @date: 2021/08/13

import matplotlib.pyplot as plt
import matplotlib.patches as mpatch


class ResultAnalyst(object):

    def __init__(self, model_manager):

        self.best_obj = model_manager.model.getObjective()
        self.vessel_dict = model_manager.data.vessel_dict
        self.time_horizon = model_manager.data.time_horizon
        self.berth = model_manager.data.berth

        self.fig = None
        self.ax = None

    def show(self):
        self.fig, self.ax = plt.subplots(figsize=(10, 10))

        for i in range(len(self.vessel_dict)):
            rectangle = mpatch.Rectangle((self.vessel_dict[i].best_position_x,
                                          self.vessel_dict[i].best_position_y),
                                         self.vessel_dict[
                                             i].final_processing_time,
                                         self.vessel_dict[i].size,
                                         color='k', fill=True, alpha=0.2)
            self.ax.add_patch(rectangle)
            self.ax.annotate(
                str(i + 1), (self.vessel_dict[i].best_position_x
                             + self.vessel_dict[i].final_processing_time / 2,
                             self.vessel_dict[i].best_position_y
                             + self.vessel_dict[i].size / 2),
                color='k', weight='bold', fontsize='8',
                ha='center', va='center'
            )
            self.ax.annotate(
                "#Q:"+str(self.vessel_dict[i].num_crane_used),
                (self.vessel_dict[i].best_position_x
                 + self.vessel_dict[i].final_processing_time / 2,
                 self.vessel_dict[i].best_position_y
                 + self.vessel_dict[i].size / 2
                 - 1),
                color='k', weight='bold', fontsize='8',
                ha='center', va='center'
            )

        self.ax.set_xlim((0, self.time_horizon))
        self.ax.set_ylim((0, self.berth.length_berth))
        self.ax.set_aspect('equal')
        self.ax.set_ylabel('Berth location')
        self.ax.set_xlabel('Time')
        self.ax.set_title(
            'BAP optimal solution w/ total # of cranes ' + str(self.berth.num_crane))
        self.fig.show()
