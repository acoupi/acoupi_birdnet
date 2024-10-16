# acoupi_birdnet

## What is acoupi_birdnet?

*acoupi_birdnet* is an open-source Python package that implement the [BirdNET-Analyzer](https://github.com/kahst/BirdNET-Analyzer?tab=readme-ov-file) bioacoustics deep-learning model on edge devices like the [Raspberry Pi](https://www.raspberrypi.org/), using the [_acoupi_](https://acoupi.github.io/acoupi) framework. The BirdNET-Analyzer DL model has been developed by the [K. Lisa Yang Center for Conservation Bioacoustics](https://www.birds.cornell.edu/ccb/) at the [Cornell Lab of Ornithology](https://www.birds.cornell.edu/home) in collaboration with [Chemnitz University of Technology](https://www.tu-chemnitz.de/index.html.en) to detect and classify more than 6000 bird species. 

!!! Warning "What is the difference between _acoupi_ and *acoupi_birdnet*?"

    __acoupi_birdnet__ and [___acoupi___](https://acoupi.github.io/acoupi) are different. The __acoupi_birdnet__ program is built on top of the ___acoupi___ python package. Think of ___acoupi___ like a bag of LEGO pieces that you can assemble into multiple shapes and forms. __acoupi_birdnet__ would be the results of assembling some of these LEGO pieces into "birds"!

??? Tip "Get familiar with _acoupi_"

    *acoupi_birdnet* builds on and inherits features from _acoupi_. If you want to learn more the [_acoupi_](https://acoupi.github.io/acoupi) framework, we recommand starting with _acoupi's_ home documentation. 

## Requirements

*acoupi_birdnet* is designed to run on single-board computers like the Raspberry Pi.
It can be installed and tested on any Linux-based machines with Python version >=3.8,<3.12.

- A Linux-based single-board computer such as the Raspberry Pi 4B.
- A SD Card with the 64-bit Lite OS version installed.
- An ultrasonic USB Microphone, such as an [AudioMoth USB Microphone](https://www.openacousticdevices.info/audiomoth) or an Ultramic 192K/250K.


??? tip "Recommended Hardware"

    The software has been extensively developed and tested with the RPi 4B.
    We advise users to select the RPi 4B or a device featuring similar specifications.

## Installation

To install *acoupi_birdnet* on your embedded device, you will need to first have _acoupi_ installed on your device. Follow these steps to install both _acoupi_ and acoupi_birdnet:

!!! Example "Step1: Install _acoupi_ and its dependencies"

    ```bash
    curl -sSL https://github.com/acoupi/acoupi/raw/main/scripts/setup.sh | bash
    ```

!!! Example "Step2: Install *acoupi_birdnet* and its dependencies"

    ```bash
    pip install acoupi_birdnet
    ```

!!! Example "Step 3: Configure the *acoupi_birdnet* program."

    ```bash
    acoupi setup --program acoupi_birdnet.program
    ```

!!! Example "Step 4: Start the *acoupi_birdnet* program."

    ```bash
    acoupi deployment start
    ```

??? tip "Using *acoupi_birdnet* from the command line"

    To check what are the available commands for _acoupi_birdnet_, enter `acoupi --help`. For more details about each of the commands, refer to the _acoupi_ [CLI documentation](https://acoupi.github.io/acoupi/reference/cli/) for further info.

## What is acoupi? 🚀

_acoupi_ is an open-source Python package that simplifies the use and implementation of bioacoustic classifiers on edge devices. 
It integrates and standardises the entire bioacoustic monitoring workflow, facilitating the creation of custom sensors, by handling audio recordings, processing, classifications, detections, communication, and data management.

!!! warning "Licenses and Usage"

    **_acoupi_birdnet_ can not be used for commercial purposes.**

    The *acoupi_birdnet* program inherits the BirdNET-Analyzer model license, published under the [__Creative Commons Attribution-NonCommercial 4.0 International__](https://github.com/kahst/BirdNET-Analyzer?tab=License-1-ov-file#readme). Please make sure to review this license to ensure your intended use complies with its terms.

!!! warning "Model Output Reliability"

    Please note that *acoupi_birdnet* program is not responsible for the accuracy or reliability of predictions made by the BirdNET-Analyzer model. It is essential to understand the model's performance and limitations before using it in your project.

    For more details on the BirdNET model, refer to the publication [Kahl S., et al., (2021) _BirdNET: A deep learning solution for avian diversity monitoring_](https://doi.org/10.1016/j.ecoinf.2021.101236). To learn more about using the BirdNET scores and outputs from the model, refer to [Wood CM. and Kahl S., (2024) _Guidelines for appropriate use of BirdNET scores and other detector outputs_](https://connormwood.com/wp-content/uploads/2024/02/wood-kahl-2024-guidelines-for-birdnet-scores.pdf) 

!!! Tip "Available _acoupi_ programs!"

    _acoupi_ offers various programs that can be configured to meet your needs. These programs can be used to simply record audio, send messages, or even detect and classify birds species. Check out the full list of available [_acoupi_ programs](https://acoupi.github.io/acoupi/explanation/programs/#pre-built_programs) to learn more. 


## Next steps 📖

Get to know _acoupi_ better by exploring this documentation.

<table>
    <tr>
        <td>
            <a href="tutorials">Tutorials</a>
            <p>Step-by-step information on how to install, configure and deploy <i>acoupi_birdnet</i> for new users.</p>
        </td>
    </tr>
    <tr>
        <td>
            <a href="explanation">Explanation</a>
            <p>Learn more about the building blocks constituing <i>acoupi_birdnet</i> program.</p>
        </td>
    </tr>
    <tr>
        <td>
            <a href="reference">Reference</a>
            <p>Technical information refering to <i>acoupi_birdnet</i> code.</p>
        </td>
    </tr>
</table>

!!! tip "Important"

    We would love to hear your feedback about the documentation. We are always looking to hearing suggestions to improve readability and user's ease of navigation. Don't hesitate to reach out if you have comments!

*[AI]: Artificial Intelligence
*[CLI]: Command Line Interface
*[DL]: Deep Learning
*[RPi]: Raspberry Pi
