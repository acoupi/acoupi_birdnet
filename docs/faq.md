# Acoupi-BirdNET FAQ

#### What is acoupi-birdnet
**acoupi-birdnet** is the implementation of the latest AI Bioacoustics Classifier [BirdNET-Lite](https://github.com/kahst/BirdNET-Lite) using acoupi Python toolkit. 

**acoupi-birdnet** uses the python API provided by the python package [birdnetlib](https://pypi.org/project/birdnetlib/) to access the BridNET-Lite and BirdNET-Analyzer models. 

#
#### What is BirdNET? 
**BirdNET** is a deep-learning model for sound bird recognition. The model was developed by the [K. Lisa Yang Center for Conservation Bioacoustics](https://www.birds.cornell.edu/ccb/) at the [Cornell Lab of Ornithology](https://www.birds.cornell.edu/home). 

[BirdNET-Lite](https://github.com/kahst/BirdNET-Lite) is the TF-Lite version of BirdNET model. 

#
#### Can the BirNET model classify any bird species? 
The BirdNET model is updated regularly. The V2.4 can recognized more than 6,000 species worldwide. The BirdNET model is used widely but as with any deep-learning model, the model has some biases and is prone to false detection. 


#
#### For who is acoupi-birdnet? 
acoupi-birdnet is itended for researchers, practioners, and individuals interested in recording and classifying birds species on devices. 

#
#### What is the diffence between acoupi-birdnet and BirdNET-Pi? 
....

# 
#### Can I configure acoupi-birdnet?

Yes. Users can customised the configuration parameters of acoupi-birdnet to suit their own needs. See [user_guide/configuration](/docs/user_guide/configuration.md) to learn more about the configuration options.

#
#### What do I need to use acoupi-birdnet?
To use acoupi-batdetect2 you will need the following hardware:
 - a Raspberry Pi 4
 - an SD Card (32GB or 64GB) with RaspbiOS-Arm64-Lite installed. 
 - a USB microphone such as the [AudioMoth](https://www.openacousticdevices.info/audiomoth) or a Lavalier microhpon. 

#
#### Where can I found more information about BirdNET? 

1. The [BirdNET-Analyzer GitHub repository](https://github.com/kahst/BirdNET-Analyzer) contains a lot of information about the model. 

2. The publication ... 