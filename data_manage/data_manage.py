# -*- coding: utf-8 -*-
# @author: Yuhao Wang
# @email: wangyuhao@shanshu.ai
# @date: 2021/08/12

from entity import Berth
from entity import Vessel


class DataManager(object):

    def __init__(self, file):
        length_berth, self.time_horizon, \
            num_crane, self.num_vessel = [int(x) for x in next(file).split()]

        self.berth = Berth(length_berth, num_crane)
        self.vessel_dict = {}

        i = 0
        for lines in file:
            current_line = lines.split()
            self.vessel_dict.update({i: Vessel(current_line)})
            i += 1
