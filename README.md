# myolab-takehome-Shweg4
MyoLab take-home assignment: Image generation with pose consistency 

These are the steps you would have to follow to run the Controlnet model with openpose 

First create a new conda environment

    conda env create -f environment.yaml
    conda activate control

Stable Diffusion 1.5 + ControlNet (using human pose)

    python gradio_pose2image.py

You need to input an image for the openpose to detetec the pose.

<div style="display: flex; justify-content: space-around; align-items: center;">

  <div style="text-align: center;">
    <h4>Ground Truth / Image</h4>
    <img src="images/basketball_player.jpg" alt="Ground truth/image" width="350" height="350">
  </div>

  <div style="text-align: center;">
    <h4>Detected Pose / Conditional Image</h4>
    <img src="images/conditional_image.png" alt="Detected pose/Conditional image" width="350" height="350">
  </div>

  <div style="text-align: center;">
    <h4>A White Female Playing Basketball in a Court</h4>
    <img src="images/female.png" alt="A white female playing basketball in a court" width="350" height="350">
  </div>

</div>
