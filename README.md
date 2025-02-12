# acoupi_birdnet
An acoupi-compatible BirdNET model and program

> [!TIP]
> Read the latest [documentation](https://acoupi.github.io/acoupi_birdnet/)

#### Readme Content
- [What is acoupi_birdnet?](#what-is-acoupi_birdnet)
- [What is the difference between _acoupi_ and _acoupi_birdnet_](#what-is-the-difference-between-acoupi-and-acoupi_birdnet)
- [Requirements](#requirements)
- [Installation](#installation)
- [What is acoupi?](#what-is-acoupi)

## What is _acoupi_birdnet_?
*acoupi_birdnet* is an open-source Python package that implement the [BirdNET-Analyzer](https://github.com/kahst/BirdNET-Analyzer?tab=readme-ov-file) bioacoustic deep-learning model on edge devices like the [Raspberry Pi](https://www.raspberrypi.org/), using the [_acoupi_](https://acoupi.github.io/acoupi) framework. The BirdNET-Analyzer DL model has been developed by the [K. Lisa Yang Center for Conservation Bioacoustics](https://www.birds.cornell.edu/ccb/) at the [Cornell Lab of Ornithology](https://www.birds.cornell.edu/home) in collaboration with [Chemnitz University of Technology](https://www.tu-chemnitz.de/index.html.en) to detect and classify more than 6000 bird species. 

## What is the difference between _acoupi_ and _acoupi_birdnet_?

__acoupi_birdnet__ and [___acoupi___](https://acoupi.github.io/acoupi) are different. The __acoupi_birdnet__ program is built on top of the ___acoupi___ python package. Think of ___acoupi___ like a bag of LEGO pieces that you can assemble into multiple shapes and forms. __acoupi_birdnet__ would be the results of assembling some of these LEGO pieces into "birds"!

> [!TIP]
> **Get familiar with _acoupi_**
>
> *acoupi_birdnet* builds on and inherits features from _acoupi_. If you want to learn more the [_acoupi_](https://acoupi.github.io/acoupi) framework, we recommand starting with _acoupi's_ home documentation. 

## Requirements
_acoupi_ has been designed to run on single-board computer devices like the [Raspberry Pi](https://www.raspberrypi.org/) (RPi).
Users should be able to download and test _acoupi_ software on any Linux-based machines with Python version >=3.8,<3.12 installed.

- A Linux-based single board computer such as the Raspberry Pi 4B. 
- A SD Card with 64-bit Lite OS version installed.
- A USB microphone, such as an [AudioMoth USB Microphone](https://www.openacousticdevices.info/audiomoth) or a Lavalier.

> [!TIP] 
> **Recommended Hardware**
>
> The software has been extensively developed and tested with the RPi 4B. We advise users to select the RPi 4B or a device featuring similar specifications.

## Installation

To install *acoupi_birdnet* on your embedded device, you will need to first have _acoupi_ installed on your device. Follow these steps to install both _acoupi_ and _acoupi_birdnet_:


**Step 1:** Install _acoupi_ and its dependencies. 
```bash
curl -sSL https://github.com/acoupi/acoupi/raw/main/scripts/setup.sh | bash
```

**Step 2:** Install *acoupi_birdnet* and its dependencies

```bash
pip install acoupi_birdnet
```

**Step 3:** Configure the *acoupi_birdnet* program.

```bash
acoupi setup --program acoupi_birdnet.program
```

**Step 4**: Start the *acoupi_birdnet* program.

```bash
acoupi deployment start
```

> [!TIP] 
> To check what are the available commands for acoupi, enter `acoupi --help`.


## What is acoupi?

_acoupi_ is an open-source Python package that simplifies the use and implementation of bioacoustic classifiers on edge devices. 
It integrates and standardises the entire bioacoustic monitoring workflow, facilitating the creation of custom sensors, by handling audio recordings, processing, classifications, detections, communication, and data management.

> [!WARNING] 
> **Licenses and Usage**
>
>**_acoupi_birdnet_ can not be used for commercial purposes.** 
>
>  The *acoupi_birdnet* program inherits the BirdNET-Analyzer model license, published under the [__Creative Commons Attribution-NonCommercial 4.0 International__](https://github.com/kahst/BirdNET-Analyzer?tab=License-1-ov-file#readme). Please make sure to review this license to ensure your intended use complies with its terms.

> [!WARNING]
> **Model Output Reliabilit**
>
> Please note that *acoupi_birdnet* program is not responsible for the accuracy or reliability of predictions made by the BirdNET-Analyzer model. It is essential to understand the model's performance and limitations before using it in your project.
>
> For more details on the BirdNET model, refer to the publication [Kahl S., et al., (2021) _BirdNET: A deep learning solution for avian diversity monitoring_](https://doi.org/10.1016/j.ecoinf.2021.101236). To learn more about using the BirdNET scores and outputs from the model, refer to [Wood CM. and Kahl S., (2024) _Guidelines for appropriate use of BirdNET scores and other detector outputs_](https://connormwood.com/wp-content/uploads/2024/02/wood-kahl-2024-guidelines-for-birdnet-scores.pdf).

> [!IMPORTANT]
> We would love to hear your feedback about the documentation. We are always looking to hearing suggestions to improve readability and user's ease of navigation. Don't hesitate to reach out if you have comments!