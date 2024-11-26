# myolab-takehome-Shweg4
MyoLab take-home assignment: Image generation with pose consistency 

These are the steps you would have to follow to run the Controlnet model with openpose 

First create a new conda environment

    conda env create -f environment.yaml
    conda activate control

Stable Diffusion 1.5 + ControlNet (using human pose)

    python gradio_pose2image.py

Right now you need to input an image and then the Openpose will detect the pose for you.

![Groud truth/image](images/0.png)

![Detected pose/ Conditional image](images/1.png)

![A white female playing basketball in a court ](images/2.png)

