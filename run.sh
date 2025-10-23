sudo rm -rf ../lerobot_datasets/lelamp_4dof
sudo chmod 666 /dev/ttyACM*
python -m lerobot.scripts.lerobot_record \
  --robot.type=xiaoai \
  --robot.port=/dev/ttyACM0 \
  --robot.id="xiaoai" \
  --robot.use_degrees=true \
  --robot.cameras='{"top_cam": {"type": "opencv", "index_or_path": "/dev/video2", "width": 320, "height": 240, "fps": 30}}' \
  --dataset.repo_id="hi3684993/lelamp_4dof_dataset" \
  --dataset.root="/home/sa/lerobot_datasets/lelamp_4dof" \
  --dataset.push_to_hub=false \
  --dataset.num_episodes=2 \
  --dataset.fps=30 \
  --dataset.episode_time_s=60 \
  --dataset.video=true \
  --dataset.single_task=false \
  --display_data=true \
  --teleop.type=xiaoai_leader \
  --teleop.port=/dev/ttyACM1 \
  --teleop.id="xiaoai_leader" \
  --teleop.use_degrees=true
#python -m lerobot.scripts.lerobot_calibrate --teleop.type=xiaoai_leader --teleop.port=/dev/ttyACM1 --teleop.calibration_dir="/home/sa/.cache/huggingface/lerobot/calibration/teleoperators/xiaoai_leader" --teleop.id=xiaoai_leader
#python -m lerobot.scripts.lerobot_calibrate --robot.type=xiaoai --robot.port=/dev/ttyACM0 --robot.calibration_dir="/home/sa/.cache/huggingface/lerobot/calibration/robots/xiaoai" --robot.id=xiaoai
