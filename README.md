# Lips Cropping from a Video

## Description
This module is designed to detect and crop lips from a video. It utilizes a pre-trained model to accurately identify lips within the video frames and subsequently crops them.

## Usage
- python 3.9.13
- Download the `models` folder from [Google drive](https://drive.google.com/drive/folders/1kKSyMd8m5f-gG5CgEUfmS0XpNjnWAb-u?usp=sharing) and place it within the lips cropping directory.
  ```bash
  pip install -r requirements.txt
  ```
- pass the path to your video file in lip_cropping.py Execute the following command:
   
   ```bash
   python lip_cropping.py
    ```
   This will save results in outputs directory
## Flask Api
```bash
python lip_cropping_api.py
```
