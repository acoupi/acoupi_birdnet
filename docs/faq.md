# FAQ

## What is *acoupi-birdnet*?
**acoupi-birdnet** is the implementation of the latest AI Bioacoustics Classifier [BirdNET-Analyzer](https://github.com/kahst/BirdNET-Analyzer) using acoupi Python toolkit. 

## What is BirdNET-Analyzer? 
**BirdNET-Analyzer** is a deep-learning model to detect and classify birds vocalizations. The model has been developed by the [K. Lisa Yang Center for Conservation Bioacoustics](https://www.birds.cornell.edu/ccb/) at the [Cornell Lab of Ornithology](https://www.birds.cornell.edu/home) in collaboration with [Chemnitz University of Technology](https://www.tu-chemnitz.de/index.html.en).

## What is birdnetlib?
**acoupi-birdnet** uses the python API provided by the python package [birdnetlib](https://pypi.org/project/birdnetlib/) to access the  BirdNET-Analyzer model. 

## Can the BirNET model classify any bird species? 
The BirdNET model is updated regularly. The V2.4 can recognized more than 6,000 species worldwide. The BirdNET model is used widely but as with any deep-learning model, the model can predict false-positives and false-negatives. 

## For who is *acoupi-birdnet*? 
*acoupi-birdnet* is itended for researchers, practioners, and individuals interested in recording and classifying birds species on devices. 

## What is the diffence between acoupi-birdnet and BirdNET-Pi? 
....

## Can I configure *acoupi-birdnet*?

Yes. Users can customised the configuration parameters of *acoupi-birdnet* to suit their own needs. See [tutorials/configuration](tutorials/configuration.md) to learn more about the configuration options.

## What are the requirements to use *acoupi-birdnet*?
To use *acoupi-birdnet* you will need the following hardware:

 - a Raspberry Pi 4
 - an SD Card (32GB or 64GB) with RaspbiOS-Arm64-Lite installed. 
 - a USB microphone such as the [AudioMoth](https://www.openacousticdevices.info/audiomoth) or a Lavalier microhpon. 

## Where can I found more information about BirdNET? 

1. The [BirdNET-Analyzer GitHub repository](https://github.com/kahst/BirdNET-Analyzer) contains a lot of information about the model. 

2. The publication ["BirdNET: A deep learning solution for avian diversity monitoring"](https://doi.org/10.1016/j.ecoinf.2021.101236) (Kahl S., et al., 2021) is also a great resource to learn more about the architecture of the model. 

3. The research article ["Guidelines for appropriate use of BirdNET scores and other detector outputs"](https://connormwood.com/wp-content/uploads/2024/02/wood-kahl-2024-guidelines-for-birdnet-scores.pdf)  (Wood C.M and Kahl S., 2024) provides insightful information about how to understand and treat the detections scores from the model.