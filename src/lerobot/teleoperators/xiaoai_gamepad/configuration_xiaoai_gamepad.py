#!/usr/bin/env python

from dataclasses import dataclass
from ..config import TeleoperatorConfig

@TeleoperatorConfig.register_subclass("xiaoai_gamepad")
@dataclass
class XiaoaiGamePadConfig(TeleoperatorConfig):
    type: str = "xiaoai_gamepad"
    
    # 游戏手柄设备路径
    gamepad_device: str = "/dev/input/js0"
    
    # 控制参数
    joint_step_size: float = 5.0  # 关节步长（度）
    deadzone: float = 0.1         # 摇杆死区
    
    # 是否使用夹爪
    use_gripper: bool = False
    
    # 关节映射配置
    joint_mapping: dict = None
    
    def __post_init__(self):
        if self.joint_mapping is None:
            self.joint_mapping = {
                "axes": {
                    0: "base_yaw",      # 左摇杆左右 -> 基座旋转
                    1: "base_pitch",    # 左摇杆上下 -> 基座俯仰  
                    3: "elbow_pitch",   # 右摇杆左右 -> 肘部俯仰
                    4: "wrist_pitch"    # 右摇杆上下 -> 腕部俯仰
                }
            }