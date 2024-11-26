# myolab-takehome-Shweg4
MyoLab take-home assignment: Image generation with pose consistency 

These are the steps you would have to follow to run the Controlnet model with openpose 

First create a new conda environment

    conda env create -f environment.yaml
    conda activate control

Stable Diffusion 1.5 + ControlNet (using human pose)

    python gradio_pose2image.py

Right now you need to input an image and then the Openpose will detect the pose for you.

<img src="images/basketball_player.jpg" alt="Groud truth/image" width="350" height="350">

<img src="images/conditional_image.png" alt="Detected pose/Conditional image" width="350" height="350">

<img src="images/female.png" alt="A white female playing basketball in a court" width="350" height="350">


