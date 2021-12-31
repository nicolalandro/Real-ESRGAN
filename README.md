# Real-ESRGAN GIMP plugin



## Installation

1. Clone repo into your GIMP plugin folder (We need GIMP 2.99.* or greater)

    ```bash
    # cd into GIMP folder
    git clone https://github.com/xinntao/Real-ESRGAN.git
    cd Real-ESRGAN
    ```

2. Install dependent packages

    ```bash
    cd Real-ESRGAN
    flatpak run --command=bash org.gimp.GIMP//beta

    pip install basicsr
    pip install facexlib
    pip install gfpgan
    pip install -r requirements.txt
    ```

3. Download pretrained models

    ```bash
    cd Real-ESRGAN
    # reality
    wget https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth -P experiments/pretrained_models
    # anime
    wget https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth -P experiments/pretrained_models
    ```
## Usage
* open GIMP
* click on Filters>Real ESRGan
* click OK on the dialog
* wait
* it will create the 4x file
