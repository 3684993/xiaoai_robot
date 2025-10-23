#!/usr/bin/env python

# Copyright 2025 The HuggingFace Inc. team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from dataclasses import dataclass, field

from lerobot.cameras import CameraConfig
from lerobot.cameras.opencv.configuration_opencv import OpenCVCameraConfig

from lerobot.robots import RobotConfig


@RobotConfig.register_subclass("xiaoai")
@dataclass
class XiaoaiFollowerConfig(RobotConfig):
    # Port to connect to the arm
    port: str

    disable_torque_on_disconnect: bool = True

    # `max_relative_target` limits the magnitude of the relative positional target vector for safety purposes.
    # Set this to a positive scalar to have the same value for all motors, or a list that is the same length as
    # the number of motors in your follower arms.
    max_relative_target: int | None = None

    # cameras
    #cameras: dict[str, CameraConfig] = field(
    #    default_factory=lambda: {
    #    "main": OpenCVCameraConfig(
    #        camera_index=0,  # 使用你找到的摄像头索引
    #        width=640,
    #        height=480,
    #        fps=25,
    #    )
    #})
    #cameras: dict[str, CameraConfig] = field(default_factory=dict)
    cameras: dict[str, CameraConfig] = field(
        default_factory=lambda: {
            "main": OpenCVCameraConfig(
                index_or_path="/dev/video4",
                fps=30,
                width=640,
                height=480
            ),
        }
    )

    # Set to `True` for backward compatibility with previous policies/dataset
    use_degrees: bool = False
