# -*- coding: utf-8 -*-
# @author: Yuhao Wang
# @email: wangyuhao@shanshu.ai
# @date: 2021/08/12

class Vessel(object):

    def __init__(self, f_line):
        self.size = int(f_line[0])
        self.arrival_time = int(f_line[1])
        self.due_time = int(f_line[2]) + 1
        self.weight_location = int(f_line[3])
        self.weight_waiting = int(f_line[4])
        self.weight_due = int(f_line[5])
        self.preferred_location = int(f_line[6]) - 1
        self.min_crane = int(f_line[7])
        self.max_crane = int(f_line[8])

        self.processing_time = {}
        i = 0
        for cranes in range(self.min_crane, self.max_crane + 1):
            self.processing_time.update({cranes: int(f_line[9 + i])})
            i += 1

        self.num_crane_used = None
        self.final_processing_time = None
        self.best_position_x = None
        self.best_position_y = None

    def set_num_crane(self, num_crane_used):
        self.num_crane_used = num_crane_used

    def set_final_processing_time(self, final_time):
        self.final_processing_time = final_time

    def set_best_position(self, x, y):
        self.best_position_x = x
        self.best_position_y = y