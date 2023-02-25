# -*- coding: utf-8 -*-
import os

from tactile_learning.utils.utils_learning import save_json_obj
from cri.transforms import transform_pose


def setup_control_params(reality, task, save_dir=None):

    if task == 'surface_3d' and reality == 'sim':
        control_params = {
            'ep_len': 500,
            'pid_params': {
                'kp': [1, 1, 0.5, 0.5, 0.5, 1],                 
                'ki': [0, 0, 0.3, 0.1, 0.1, 0],                
                'ei_clip': [[0, 0, 0, -30, -30, 0], [0, 0, 5, 30, 30, 0]],        
                'error': 'lambda y, r: transform_pose(r, y)'  # SE(3) error
            },
            'ref_pose': [0, -1, 3, 0, 0, 0]              
        }

    elif task == 'edge_2d' and reality == 'sim':
        control_params = {
            'ep_len': 100,#60,
            'pid_params': {
                'kp': [0.5, 1, 0, 0, 0, 0.5],                 
                'ki': [0.3, 0, 0, 0, 0, 0.1],                
                'ei_clip': [[-5, 0, 0, 0, 0, -45], [5, 0, 0, 0, 0,  45]],          
                'error': 'lambda y, r: transform_pose(r, y)'  # SE(3) error
            },
            'ref_pose': [0, 1, 0, 0, 0, 0]              
        }

    elif task == 'edge_3d' and reality == 'sim':
        control_params = {
            'ep_len': 400,
            'pid_params': {
                'kp': [0.5, 1, 0.5, 0, 0, 0.5],                 
                'ki': [0.3, 0, 0.3, 0, 0, 0.1],                
                'ei_clip': [[0, -5, 0, 0, 0, -45], [0, 5, 5, 0, 0, 45]],
                'error': 'lambda y, r: transform_pose(r, y)'  # SE(3) error
            },
            'ref_pose': [0, 1, 3, 0, 0, 0]             
        }

    elif task == 'edge_5d' and reality == 'sim':
        control_params = {
            'ep_len': 250,
            'pid_params': {
                'kp': [1, 0.5, 0.5, 0.5, 0.5, 0.5],                
                'ki': [0, 0.3, 0.3, 0.1, 0.1, 0.1],
                'ei_clip': [[0, -5, 0, -30, -30, -45], [0, 5, 5, 30, 30, 45]],
                'error': 'lambda y, r: transform_pose(r, y)'  # SE(3) error
            },
            'ref_pose': [1, 0, 3, 0, 0, 0]              
        }

    elif task == 'edge_2d' and reality == 'real':
        control_params = {
            'ep_len': 150,
            'pid_params': {
                'kp': [0.5, 1, 0, 0, 0, 0.5],                
                'ki': [0.3, 0, 0, 0, 0, 0.1],
                'ei_clip': [[-5, 0, 0, 0, 0, -45], [-5, 0, 0, 0, 0, 45]],
                'error': 'lambda y, r: transform_pose(r, y)'  # SE(3) error
            },
            'ref_pose': [0, 3, 0, 0, 0, 15]
        }

    if save_dir:
        save_json_obj(control_params, os.path.join(save_dir, 'control_params'))

    # convert error into function handle if exists
    if 'error' in control_params['pid_params']:
        control_params['pid_params']['error'] = eval(control_params['pid_params']['error'])

    return control_params


def setup_env_params(reality, task, stimulus, save_dir=None):

    if reality == 'real':
        env_params = {
            'work_frame': [285, 0, -93, 0, 0, 0], # square, circle
            'linear_speed': 10, 
            'angular_speed': 10,
            'tcp_pose': [0, 0, 0, 0, 0, 0],
            'model_type': 'posenet_cnn'
        }

    elif reality == 'sim':
        env_params = {
            'stim_name': stimulus,
            'stim_pose': [600, 0, 0, 0, 0, 0],
            'show_gui': True, 
            'show_tactile': True, 
            'quick_mode': False,
            'model_type': 'simple_cnn'
        }

        if stimulus == 'saddle':
            env_params['work_frame'] = [600, -65, 55-3, -180, 0, 0]

        elif stimulus == 'bowl':
            env_params['work_frame'] = [600, 0, 25, -180, 0, 0]
            env_params['stim_pose'] = [600, 0, 60, 90, 0, 0]
            env_params['stim_scale'] = 0.3

        elif task[:-3] == 'edge':
            env_params['work_frame'] = [650,   0, 40-3, -180, 0, 0]

        elif task[:-3] == 'surface':
            env_params['work_frame'] = [610, -55, 40-3, -180, 0, 0]

        if save_dir:
            save_json_obj(env_params, os.path.join(save_dir, 'env_params'))

    return env_params


def setup_servo_control(reality, task, stimulus, save_dir=None):
    control_params = setup_control_params(reality, task, save_dir)
    env_params = setup_env_params(reality, task, stimulus, save_dir)

    return env_params, control_params


if __name__ == '__main__':
    pass
