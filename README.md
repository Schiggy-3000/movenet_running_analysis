<a name="readme-top"></a>


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Schiggy-3000/movenet_running_analysis">
    <img src="/Miscellaneous/tensor_flow_logo.png" alt="Logo" style="width: 200px; height: auto;">
  </a>

  <h3 align="center">Movenet Running Analysis</h3>

  <p align="center">
    A running analysis tool based on tensorflow's movenet thunder model!
    <br />
    <a href="https://www.tensorflow.org/hub/tutorials/movenet">TensorFlow MoveNet</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#example">Example</a></li>
    <li><a href="#installation">Installation</a></li>
  </ol>
</details>



## About The Project

Tensorflow built several model for [pose estimation](https://www.tensorflow.org/lite/examples/pose_estimation/overview) based on computer vision techniques that detect human figures in images and videos, so that one could determine, for example, where someone's elbow shows up in an image. The pose estimation models takes a processed camera image as input and outputs information about keypoints. The keypoints detected are indexed by a part ID:

* nose: 0
* left_eye: 1
* right_eye: 2
* left_ear: 3
* right_ear: 4
* left_shoulder: 5
* right_shoulder: 6
* left_elbow: 7
* right_elbow: 8
* left_wrist: 9
* right_wrist: 10
* left_hip: 11
* right_hip: 12
* left_knee: 13
* right_knee: 14
* left_ankle: 15
* right_ankle: 16

This project builds on top of this pretrained model, using its infered keypoints for analysing running techniques in athletes.  

<p align="right">(<a href="#readme-top">back to top</a>)</p>



## Example

Following an example of some parameters that are extracted by the movenet_running_analysis scripts.

![ANNOTATED_jes_woods_nike_coach](https://github.com/Schiggy-3000/movenet_running_analysis/raw/main/Processed_data/Gifs/ANNOTATED_jes_woods_nike_coach.gif)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



## Installation

Clone and apply this running analysis tool on your own device.

1. Clone the repo
   ```GitHub CLI
   gh repo clone Schiggy-3000/movenet_running_analysis
   ```
2. Navigate to project
   ```sh
   cd \path\to\movenet_running_analysis
   ```
3. Build virtual environment
   ```sh
   python -m venv myvenv
   ```
4. Activate virtual environment
   ```sh
   .\myvenv\Scripts\activate
   ```
5. Install dependencies
   ```sh
   pip install -r requirements.txt
   ```
6. Execute main.py
   ```sh
   python.exe .\main.py
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>