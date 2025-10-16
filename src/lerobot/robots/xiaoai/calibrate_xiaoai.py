from .config_xiaoai_follower import XiaoaiFollowerConfig
from .xiaoai_follower import XiaoaiFollower  # 你的自定义类文件

def main():
    config = XiaoaiFollowerConfig(
        port="/dev/ttyACM0",
        id="xiaoai_1",
        use_degrees=True
    )
    robot = XiaoaiFollower(config)
    robot.connect(calibrate=True)

if __name__ == "__main__":
    main()
