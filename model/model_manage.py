# -*- coding: utf-8 -*-
# @author: Yuhao Wang
# @email: wangyuhao@shanshu.ai
# @date: 2021/08/12

import coptpy as copt
from itertools import product
from .result_analyst import ResultAnalyst


class ModelManager(object):

    def __init__(self, data):

        self.data = data
        self.vessel_index = range(self.data.num_vessel)
        self.double_vessel_index = list(product(self.vessel_index,
                                                self.vessel_index))
        for i in self.vessel_index:
            self.double_vessel_index.remove((i, i))
        self.vessel_hold_index = list()
        for i in self.vessel_index:
            for j in range(len(self.data.vessel_dict[i].processing_time)):
                self.vessel_hold_index.append((i,
                                               j + self.data.vessel_dict[i].
                                               min_crane))
        self.env = None
        self.model = None
        # Decision variables
        self.u = None
        self.b = None
        self.c = None
        self.z = None
        self.tard = None
        self.d = None
        self.sigma = None
        self.delta = None
        self.alpha = None

    def build(self):
        self.env = copt.Envr()
        self.model = self.env.createModel("BACASP")

        self.u = self.model.addVars(self.vessel_index, lb=0,
                                    vtype=copt.COPT.CONTINUOUS)
        self.b = self.model.addVars(self.vessel_index, lb=0,
                                    vtype=copt.COPT.CONTINUOUS)
        self.c = self.model.addVars(self.vessel_index, lb=0,
                                    vtype=copt.COPT.CONTINUOUS)
        self.z = self.model.addVars(self.vessel_index, lb=0,
                                    vtype=copt.COPT.INTEGER)
        self.tard = self.model.addVars(self.vessel_index, lb=0,
                                       vtype=copt.COPT.INTEGER)
        self.d = self.model.addVars(self.vessel_index,
                                    vtype=copt.COPT.INTEGER)
        self.sigma = self.model.addVars(self.double_vessel_index,
                                        vtype=copt.COPT.BINARY)
        self.delta = self.model.addVars(self.double_vessel_index,
                                        vtype=copt.COPT.BINARY)
        self.alpha = self.model.addVars(self.vessel_hold_index,
                                        vtype=copt.COPT.BINARY)

        self.model.setObjective(sum(
            (self.data.vessel_dict[i].weight_waiting
             * (self.u[i] - self.data.vessel_dict[i].arrival_time))
            + (self.data.vessel_dict[i].weight_due * self.tard[i])
            + (self.data.vessel_dict[i].weight_location * self.d[i])
            for i in self.vessel_index), sense=copt.COPT.MINIMIZE)

        for (i, j) in self.double_vessel_index:
            self.model.addConstr(
                self.u[j] >= self.u[i]
                + sum(self.alpha[i, q] * self.data.vessel_dict[i].
                      processing_time[q]
                      for q in range(self.data.vessel_dict[i].min_crane,
                                     self.data.vessel_dict[i].max_crane + 1))
                + ((self.sigma[i, j] - self.delta[i, j] - 1)
                   * self.data.time_horizon)
            )
            self.model.addConstr(
                self.b[j] >= self.b[i] + self.data.vessel_dict[i].size
                + ((self.delta[i, j] - self.sigma[i, j] - 1)
                   * self.data.berth.length_berth)
            )
            self.model.addConstr(
                self.z[j] >= self.z[i]
                + sum(self.alpha[i, q] * q
                      for q in range(self.data.vessel_dict[i].min_crane,
                                     self.data.vessel_dict[i].max_crane + 1))
                + ((self.delta[i, j] - 1)
                   * self.data.berth.num_crane)
            )
            self.model.addConstr(
                self.sigma[i, j] + self.sigma[j, i]
                + self.delta[i, j] + self.delta[j, i] == 1
            )

        for i in self.vessel_index:
            self.model.addConstr(
                sum(self.alpha[i, q] * self.data.vessel_dict[i].
                    processing_time[q]
                    for q in range(self.data.vessel_dict[i].min_crane,
                                   self.data.vessel_dict[i].max_crane + 1))
                + self.u[i] == self.c[i]
            )
            self.model.addConstr(
                self.u[i] >= self.data.vessel_dict[i].arrival_time
            )
            self.model.addConstr(
                sum(self.alpha[i, q]
                    for q in range(self.data.vessel_dict[i].min_crane,
                                   self.data.vessel_dict[i].max_crane + 1))
                == 1
            )
            self.model.addConstr(
                self.data.berth.length_berth - self.data.vessel_dict[i].size
                >= self.b[i]
            )
            self.model.addConstr(
                self.z[i] >=
                sum(self.alpha[i, q] * q
                    for q in range(self.data.vessel_dict[i].min_crane,
                                   self.data.vessel_dict[i].max_crane + 1))
            )
            self.model.addConstr(
                self.z[i] <= self.data.berth.num_crane
            )
            self.model.addConstr(
                self.d[i] >= self.b[i] - self.data.vessel_dict[i].
                preferred_location
            )
            self.model.addConstr(
                self.d[i] >= -self.b[i] + self.data.vessel_dict[i].
                preferred_location
            )
            self.model.addConstr(
                self.tard[i] >= self.c[i] - self.data.vessel_dict[i].due_time
            )

    def solve(self):
        self.model.solve()

        for i in self.vessel_index:
            self.data.vessel_dict[i].set_num_crane(
                sum(self.alpha[i, q].x * q
                    for q in range(self.data.vessel_dict[i].min_crane,
                                   self.data.vessel_dict[i].max_crane + 1))
            )

            self.data.vessel_dict[i].set_final_processing_time(
                self.c[i].x - self.u[i].x
            )
            self.data.vessel_dict[i].set_best_position(
                self.u[i].x, self.b[i].x
            )

        result_analyst = ResultAnalyst(self)

        return result_analyst