<a name="readme-top"></a>


<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Schiggy-3000/movenet_running_analysis">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Movenet Running Analysis</h3>

  <p align="center">
    A running analysis tool based on tensorfolwos movenet thunder!
    <br />
    <a href="https://github.com/Schiggy-3000/movenet_running_analysis"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/Schiggy-3000/movenet_running_analysis/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/Schiggy-3000/movenet_running_analysis/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
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

Tensorflow built a model for pose estimation based on computer vision techniques that detect human figures in images and videos, so that one could determine, for example, where someone's elbow shows up in an image. The pose estimation models takes a processed camera image as input and outputs information about keypoints. The keypoints detected are indexed by a part ID:

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

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Installation

Clone and apply this running analysis tool on your own device.

1. Clone the repo
   ```GitHub CLI
   gh repo clone Schiggy-3000/movenet_running_analysis
   ```
2. Build a virtual environment.
   ```sh
   cd \path\to\your\project
   python -m venv myvenv
   .\myvenv\Scripts\activate
   pip install -r requirements.txt
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-url]: https://github.com/Schiggy-3000/movenet_running_analysis/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Schiggy-3000/movenet_running_analysis.svg?style=for-the-badge
[forks-url]: https://github.com/Schiggy-3000/movenet_running_analysis/network/members
[stars-shield]: https://img.shields.io/github/stars/Schiggy-3000/movenet_running_analysis.svg?style=for-the-badge
[stars-url]: https://github.com/Schiggy-3000/movenet_running_analysis/stargazers
[issues-shield]: https://img.shields.io/github/issues/Schiggy-3000/movenet_running_analysis.svg?style=for-the-badge
[issues-url]: https://github.com/Schiggy-3000/movenet_running_analysis/issues
[license-shield]: https://img.shields.io/github/license/Schiggy-3000/movenet_running_analysis.svg?style=for-the-badge
[license-url]: https://github.com/Schiggy-3000/movenet_running_analysis/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/gabriel-meier-33bba8109
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 