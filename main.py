# -*- coding: utf-8 -*-
# @author: Yuhao Wang
# @email: wangyuhao@shanshu.ai
# @date: 2021/08/12

from data_manage import DataManager
from model import ModelManager


with open('DATA/GenMB-10m/instance_Gen_Meisel2009_10m_20_1.dat') as f:
    data_manager = DataManager(f)

model_manager = ModelManager(data_manager)
model_manager.build()

result_analyst = model_manager.solve()
result_analyst.show()
