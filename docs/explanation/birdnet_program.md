# BirdNet Program

The BirdNET Program has been designed to record, detect and classify, as well as manage and send messages of UK bat calls. The program extends the `DetectionProgram` and `MessagingProgram` from the _acoupi_ package by adding the BirdNET model and integrating users' custom configuration schema.

### Key Elements

#### BirdNET_ConfigSchema

Defines the configuration for the BirdNET program, including the audio recording, model setup, file management, messaging, and summariser settings.

### Program Tasks 
#### Recording
Records audio from a microphone and saves the audio files
in a temporary directory until they have been processed by the `detection` 
and `management` tasks. Based on the `SavingFilters` configuration, recordings 
will either saved or deleted.

#### Detection
Runs the BirdNET model on the audio recordings, processes
the detections, and can use a custom `ModelOutputCleaner` to filter out unwanted detections (e.g., low-confidence score). The filtered detections are saved in a `metadata.db` file. 

#### Management
Performs periodically file management operations, such as moving recording to permanent storage, or deleting unnecessary ones.

#### Messaging
Send messages stored in the message store using a configured protocol (HTTP or MQTT). 

#### Summary
Periodically creates summaries of the detections. 

### Customisation Options

#### Model Config
Set the `detection_threshold` to clean out the output of the 
BatDetect2 model. Detections with a confidence score below this threshold 
will be excluded from the store and from the message content.

#### Saving Config
Define where recordings are stored, the naming format, and 
the minimum confidence score for saving recordings. Recordings with confidence 
scores below the `saving_threshold` will not be saved. The `saving_threshold` 
can be set lower than the `detection_threshold` to save recordings with uncertain detections. Recordings with detections above the `detection_threshold` will be 
saved in the `true_dir` directory, while recordings with detections below 
the `detection_threshold` but above the `saving_threshold` will be saved in 
the `false_dir` directory. 

#### SavingFilters Config 
Define additional saving filters for saving recordings. 

- A timeinterval interval fitler that saves recordings whthin a specific time window, set by the `starttime` and `endtime` parameters. 
- A frequency filter that saves recordings for a specific duration (in minutes) at defined interval (in minutes), set by the `frequency_duration` and `frequency_interval` parameters.
- A before dawn/dusk filter to save recording for a defined duration (in minutes) before dawn and dusk, set by the `before_dawndusk_duration`.
- An after dawn/dusk filter to save recording for a defined duration (in minutes) after dawn and dusk, set by the `after_dawndusk_duration`.

#### SummariserConfig
Define the interval for summarising detections. 
By default, the summariser calculates the minimum, maximum, and average 
confidence scores of the total number of detections for each time interval. 
If the `low_band_threshold`, `mid_band_threshold`, and `high_band_threshold` are 
set to values greater than 0.0, it also summarises the number of detections in 
each band (low, mid, high).