# myolab-takehome-Shweg4
MyoLab take-home assignment: Image generation with pose consistency 

These are the steps you would have to follow to run the Controlnet model with openpose 

First create a new conda environment

    conda env create -f environment.yaml
    conda activate control

Stable Diffusion 1.5 + ControlNet (using human pose)

    python gradio_pose2image.py

You need to input an image for the openpose to detetec the pose.

<table>
  <tr>
    <th>Ground Truth / Image</th>
    <th>Detected Pose / Conditional Image</th>
    <th>A White Female Playing Basketball in a Court</th>
  </tr>
  <tr>
    <td>
      <img src="images/basketball_player.jpg" alt="Ground truth/image" width="300">
    </td>
    <td>
      <img src="images/condition_image.png" alt="Detected pose/Conditional image" width="300">
    </td>
    <td>
      <img src="images/female.png" alt="A white female playing basketball in a court" width="300">
    </td>
  </tr>
</table>
