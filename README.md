# myolab-takehome-Shweg4
MyoLab take-home assignment: Image generation with pose consistency 

These are the steps you would have to follow to run the Controlnet model with openpose 

First create a new conda environment

    conda env create -f environment.yaml
    conda activate control

Stable Diffusion 1.5 + ControlNet (using human pose)

    python gradio_pose2image.py

Apparently, this model deserves a better UI to directly manipulate pose skeleton. However, again, Gradio is somewhat difficult to customize. Right now you need to input an image and then the Openpose will detect the pose for you.

Prompt: "Chief in the kitchen"
![p](github_page/p11.png)

Prompt: "An astronaut on the moon"
![p](github_page/p12.png)
