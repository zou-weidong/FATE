#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#  Copyright 2019 The FATE Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import json
import os
import subprocess
import sys

# from load_file_functions import load_file

home_dir = os.path.split(os.path.realpath(__file__))[0]
config_path = home_dir + '/conf'
data_path = home_dir + '/../data'
load_file_program = home_dir + '/../load_file/load_file.py'

# data_set = 'breast'
data_set = 'default_credit'
# data_set = 'give_credit'

mode = 'fit'


# mode = 'transform'


def make_config_file(work_mode, job_id, role, guest_partyid, host_partyid):
    work_mode = int(work_mode)

    with open(config_path + '/{}_runtime_conf.json'.format(role), 'r', encoding='utf-8') as load_f:
        role_config = json.load(load_f)

    if role == 'guest':
        role_config['local']['party_id'] = guest_partyid
        data_suffix = 'b'
    else:
        role_config['local']['party_id'] = host_partyid
        data_suffix = 'a'

    role_config['role']['host'][0] = host_partyid
    role_config['role']['guest'][0] = guest_partyid
    role_config['WorkFlowParam']['work_mode'] = int(work_mode)

    role_config['FeatureBinningParam']['process_method'] = mode
    role_config['WorkFlowParam']['train_input_table'] = "{}_{}_{}".format(data_set, role, job_id)

    # guest_config_path = config_path + '/guest_runtime_conf.json_' + str(job_id)
    role_config_path = "{}/{}_runtime_conf.json_{}".format(
        config_path, role, job_id
    )

    with open(role_config_path, 'w', encoding='utf-8') as json_file:
        json.dump(role_config, json_file, ensure_ascii=False)

    with open(config_path + '/load_file.json', 'r', encoding='utf-8') as load_f:
        load_config = json.load(load_f)
    load_config['work_mode'] = work_mode

    # load_config['file'] = data_path + '/' + data_set + '_b.csv'
    load_config['file'] = "{}/{}_{}.csv".format(data_path, data_set, data_suffix)

    load_config['table_name'] = "{}_{}_{}".format(data_set, role, job_id)

    # load_file_role = config_path + '/load_file.json_guest_' + str(job_id)
    load_file_path = "{}/load_file.json_{}_{}".format(config_path, role, job_id)

    with open(load_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(load_config, json_file, ensure_ascii=False)

    return role_config_path, load_file_path


def load_file(load_file_path):
    load_process = subprocess.Popen(["python",
                                     load_file_program,
                                     "-c",
                                     load_file_path,
                                     ])
    # load_process.communicate()
    returncode = load_process.wait()
    print("Load file return code : {}".format(returncode))


if __name__ == '__main__':
    work_mode = sys.argv[1]
    jobid = sys.argv[2]
    role = sys.argv[3]
    guest_partyid = int(sys.argv[4])
    host_partyid = int(sys.argv[5])

    role_config_path, load_file_path = make_config_file(work_mode, jobid, role, guest_partyid, host_partyid)

    load_file(load_file_path)

    work_path = home_dir + '/../../workflow/hetero_binning_workflow/' \
                           'hetero_binning_{}_workflow.py'.format(role)

    subprocess.Popen(["python",
                      work_path,
                      "-c",
                      role_config_path,
                      "-j",
                      jobid
                      ])
