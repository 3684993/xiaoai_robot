#!/usr/bin/env python

import sys
import numpy as np
from typing import Any

from ..teleoperator import Teleoperator
from ..utils import TeleopEvents
from .configuration_xiaoai_gamepad import XiaoaiGamePadConfig


class XiaoaiGamePadTeleop(Teleoperator):
    """
    Gamepad teleoperation for Xiaoai 4DOF robotic arm.
    Maps gamepad inputs directly to joint movements.
    """

    config_class = XiaoaiGamePadConfig
    name = "xiaoai_gamepad"

    def __init__(self, config: XiaoaiGamePadConfig):
        super().__init__(config)
        self.config = config
        self.robot_type = config.type
        self.gamepad = None
        
        # 关节状态
        self.joint_deltas = {
            "base_yaw": 0.0,
            "base_pitch": 0.0,
            "elbow_pitch": 0.0, 
            "wrist_pitch": 0.0
        }
        # 平滑滤波参数
        self.smoothing_factor = 0.3  # 平滑系数 (0.0-1.0)，越小越平滑
        self.filtered_deltas = self.joint_deltas.copy()

    @property
    def action_features(self) -> dict:
        return {
            "dtype": "float32",
            "shape": (4,),  # 4个关节
            "names": {
                "joints": ["base_yaw", "base_pitch", "elbow_pitch", "wrist_pitch"]
            },
        }

    @property
    def feedback_features(self) -> dict:
        return {}

    def connect(self) -> None:
        # 使用与官方相同的游戏手柄选择逻辑
        if sys.platform == "darwin":
            from .gamepad_utils import GamepadControllerHID as Gamepad
        else:
            from .gamepad_utils import GamepadController as Gamepad

        # 创建游戏手柄控制器，使用关节步长作为控制参数
        self.gamepad = Gamepad(
            x_step_size=self.config.joint_step_size,
            y_step_size=self.config.joint_step_size, 
            z_step_size=self.config.joint_step_size,
            wrist_step_size=self.config.joint_step_size,
            deadzone=self.config.deadzone
        )
        self.gamepad.start()
        
        print("Xiaoai Gamepad Controls:")
        print("  Left Stick: base_yaw (left/right), base_pitch (up/down)")
        print("  Right Stick: elbow_pitch (left/right), wrist_pitch (up/down)")
        print("  Y/Triangle: End episode with SUCCESS")
        print("  A/Cross: End episode with FAILURE") 
        print("  X/Square: Rerecord episode")
        print("  RB: Intervention mode")
        print("  RT/LT: Gripper control (if enabled)")

    def get_action(self) -> dict[str, Any]:
        if self.gamepad is None:
            return {joint: 0.0 for joint in self.joint_deltas.keys()}

        # 更新游戏手柄状态
        self.gamepad.update()

        # 获取原始的 delta 值（来自游戏手柄）
        delta_x, delta_y, delta_z,delta_wrist = self.gamepad.get_deltas()

        # 将游戏手柄输入映射到关节
        # 左摇杆：base_yaw (左右), base_pitch (上下)
        #self.joint_deltas["base_yaw"] = delta_y  # 左摇杆左右 -> base_yaw
        #self.joint_deltas["base_pitch"] = delta_x  # 左摇杆上下 -> base_pitch
        
        # 右摇杆：elbow_pitch (左右), wrist_pitch (上下)  
        #self.joint_deltas["elbow_pitch"] = delta_z  # 右摇杆上下 -> elbow_pitch
        # 注意：这里可能需要根据实际手柄映射调整
        #
        #self.joint_deltas["wrist_pitch"] = delta_wrist

        # 应用平滑滤波
        self.joint_deltas["base_yaw"] = self._apply_smoothing("base_yaw", delta_y)
        self.joint_deltas["base_pitch"] = self._apply_smoothing("base_pitch", delta_x)
        self.joint_deltas["elbow_pitch"] = self._apply_smoothing("elbow_pitch", delta_z)
        self.joint_deltas["wrist_pitch"] = self._apply_smoothing("wrist_pitch", delta_wrist)
        

        return {f"{joint}.pos": delta for joint, delta in self.joint_deltas.items()}
    
    def _apply_smoothing(self, joint_name: str, new_delta: float) -> float:
        """应用指数平滑滤波"""
        filtered = (self.smoothing_factor * new_delta + 
                   (1 - self.smoothing_factor) * self.filtered_deltas[joint_name])
        self.filtered_deltas[joint_name] = filtered
        return filtered * self.config.joint_step_size

    def get_teleop_events(self) -> dict[str, Any]:
        """获取遥操作事件（干预、终止等）"""
        if self.gamepad is None:
            return {
                TeleopEvents.IS_INTERVENTION: False,
                TeleopEvents.TERMINATE_EPISODE: False,
                TeleopEvents.SUCCESS: False,
                TeleopEvents.RERECORD_EPISODE: False,
            }

        # 更新游戏手柄状态
        self.gamepad.update()

        # 检查干预状态
        is_intervention = self.gamepad.should_intervene()

        # 获取 episode 结束状态
        episode_end_status = self.gamepad.get_episode_end_status()
        terminate_episode = episode_end_status in [
            TeleopEvents.RERECORD_EPISODE,
            TeleopEvents.FAILURE,
        ]
        success = episode_end_status == TeleopEvents.SUCCESS
        rerecord_episode = episode_end_status == TeleopEvents.RERECORD_EPISODE

        return {
            TeleopEvents.IS_INTERVENTION: is_intervention,
            TeleopEvents.TERMINATE_EPISODE: terminate_episode,
            TeleopEvents.SUCCESS: success,
            TeleopEvents.RERECORD_EPISODE: rerecord_episode,
        }

    def disconnect(self) -> None:
        """断开游戏手柄连接"""
        if self.gamepad is not None:
            self.gamepad.stop()
            self.gamepad = None

    def is_connected(self) -> bool:
        """检查游戏手柄是否连接"""
        return self.gamepad is not None and self.gamepad.running

    def calibrate(self) -> None:
        """校准游戏手柄"""
        pass

    def is_calibrated(self) -> bool:
        """检查是否已校准"""
        return True

    def configure(self) -> None:
        """配置游戏手柄"""
        pass

    def send_feedback(self, feedback: dict) -> None:
        """发送反馈到游戏手柄"""
        pass