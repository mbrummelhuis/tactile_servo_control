"""
python launch_collect_data.py -r sim -s tactip -t edge_2d
"""
import os

from tactile_data.tactile_servo_control import BASE_DATA_PATH
from tactile_data.collect_data.collect_data import collect_data
from tactile_data.collect_data.process_data import process_data, split_data
from tactile_data.collect_data.setup_embodiment import setup_embodiment
from tactile_data.collect_data.setup_targets import setup_targets
from tactile_data.utils import make_dir

from tactile_servo_control.collect_data.setup_collect_data import setup_collect_data
from tactile_servo_control.utils.parse_args import parse_args


def launch(args, data_params):

    for args.task in args.tasks:
        for data_dir_name, num_poses in data_params.items():

            data_dir_name = '_'.join(filter(None, [data_dir_name, *args.data_version]))
            output_dir = '_'.join([args.robot, args.sensor])

            # setup save dir
            save_dir = os.path.join(BASE_DATA_PATH, output_dir, args.task, data_dir_name)
            image_dir = os.path.join(save_dir, "images")
            make_dir(save_dir)
            make_dir(image_dir)

            # setup parameters
            collect_params, env_params, sensor_params = setup_collect_data(
                args.robot,
                args.sensor,
                args.task,
                save_dir
            )

            # setup embodiment
            robot, sensor = setup_embodiment(
                env_params,
                sensor_params
            )

            # setup targets to collect
            target_df = setup_targets(
                collect_params,
                num_poses,
                save_dir
            )

            # collect
            collect_data(
                robot,
                sensor,
                target_df,
                image_dir,
                collect_params
            )


def process(args, data_params, process_params, split=None):

    output_dir = '_'.join([args.robot, args.sensor])
    dir_names = ['_'.join(filter(None, [dir, *args.data_version])) for dir in data_params]

    for args.task in args.tasks:
            path = os.path.join(BASE_DATA_PATH, output_dir, args.task)

            dir_names = split_data(path, dir_names, split)
            process_data(path, dir_names, process_params)


if __name__ == "__main__":

    args = parse_args(
        robot='sim',
        sensor='tactip',
        tasks=['edge_2d'],
        data_version=['temp']
    )

    data_params = {
        'data': 500,
        # 'train': 4000,
        # 'val': 1000,
    }

    process_params = {
        # "thresh": [61, 5],
        # "circle_mask_radius": 140, # 140 ABB tactip # 210 CR midi 
        "bbox": (12, 12, 240, 240)  # sim (12, 12, 240, 240) # CR midi (5, 10, 425, 430) # MG400 mini (10, 10, 310, 310) # ABB tactip (25, 25, 305, 305)
    }

    launch(args, data_params)
    process(args, data_params, process_params, split=0.8)
