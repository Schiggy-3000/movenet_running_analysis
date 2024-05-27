<a name="readme-top"></a>

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

Tensorflow built several model for [pose estimation](https://www.tensorflow.org/lite/examples/pose_estimation/overview) based on computer vision techniques that detect human figures in images and videos, so that one could determine, for example, where someone's elbow shows up in an image. The pose estimation models takes a processed camera image as input and outputs information about keypoints. The keypoints detected are as following:

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

This project builds on top of this pretrained model, using its infered keypoints for running analysis in athletes.  

<p align="right">(<a href="#readme-top">back to top</a>)</p>



## Example

Following an example of some parameters that are extracted by the movenet_running_analysis scripts.

![ANNOTATED_jes_woods_nike_coach](https://github.com/Schiggy-3000/movenet_running_analysis/raw/main/Processed_data/Gifs/ANNOTATED_jes_woods_nike_coach_1.gif)

- **VD (relative to leg length)** is the maximum vertical distance the center of mass has traveled.
- **Left knee angle** is the angle formed by ankle, knee and hip of the left leg.
- **Right knee angle** is the angle formed by ankle, knee and hip of the right leg.
- **Knee angle min.** is the minimum angle formed by the ankle, knee and hip of either leg.
- **Total steps** is a counter of the steps taken.
- **Cadence** measures steps per minute.
- **Leading ankle to CoM max. (relative to leg length)** the maximum distance an ankle came in front of the center of mass (CoM).
- **Trailing ankle max. (relative to leg length)** the maximum distance an ankle traveled behind the center of mass (CoM).

There are plenty more metrics that can be toggled, depending on the analysis one aims to do.

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