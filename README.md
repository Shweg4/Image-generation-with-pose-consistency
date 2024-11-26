# myolab-takehome-Shweg4
MyoLab take-home assignment: Image generation with pose consistency 

These are the steps you would have to follow to run the Controlnet model with openpose 

First create a new conda environment

    conda env create -f environment.yaml
    conda activate control

Stable Diffusion 1.5 + ControlNet (using human pose)

    python gradio_pose2image.py

Right now you need to input an image and then the Openpose will detect the pose for you.

![Groud truth/image](images/basketball_player.jpg)
<img src="images/basketball_player.jpg" alt="Groud truth/image" width="100" height="100">

![Detected pose/ Conditional image](images/conditional_image.png)

![A white female playing basketball in a court ](images/female.png)

