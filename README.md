# Real-ESRGAN GIMP plugin



### Installation

1. Clone repo into your plugin folder

    ```bash
    git clone https://github.com/xinntao/Real-ESRGAN.git
    cd Real-ESRGAN
    ```

2. Install dependent packages

    ```bash
    # Install basicsr - https://github.com/xinntao/BasicSR
    # We use BasicSR for both training and inference
    pip install basicsr
    # facexlib and gfpgan are for face enhancement
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

## :zap: Quick Inference

### Inference general images

Download pre-trained models: [RealESRGAN_x4plus.pth](https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth)

```bash
wget https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth -P experiments/pretrained_models
```

Inference!

```bash
python inference_realesrgan.py -n RealESRGAN_x4plus -i inputs --face_enhance
```

Results are in the `results` folder

### Inference anime images

<p align="center">
  <img src="https://raw.githubusercontent.com/xinntao/public-figures/master/Real-ESRGAN/cmp_realesrgan_anime_1.png">
</p>

Pre-trained models: [RealESRGAN_x4plus_anime_6B](https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth)<br>
 More details and comparisons with [waifu2x](https://github.com/nihui/waifu2x-ncnn-vulkan) are in [**anime_model.md**](docs/anime_model.md)

```bash
# download model
wget https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth -P experiments/pretrained_models
# inference
python inference_realesrgan.py -n RealESRGAN_x4plus_anime_6B -i inputs
```

Results are in the `results` folder

### Usage of python script

1. You can use X4 model for **arbitrary output size** with the argument `outscale`. The program will further perform cheap resize operation after the Real-ESRGAN output.

```console
Usage: python inference_realesrgan.py -n RealESRGAN_x4plus -i infile -o outfile [options]...

A common command: python inference_realesrgan.py -n RealESRGAN_x4plus -i infile --outscale 3.5 --half --face_enhance

  -h                   show this help
  -i --input           Input image or folder. Default: inputs
  -o --output          Output folder. Default: results
  -n --model_name      Model name. Default: RealESRGAN_x4plus
  -s, --outscale       The final upsampling scale of the image. Default: 4
  --suffix             Suffix of the restored image. Default: out
  -t, --tile           Tile size, 0 for no tile during testing. Default: 0
  --face_enhance       Whether to use GFPGAN to enhance face. Default: False
  --half               Whether to use half precision during inference. Default: False
  --ext                Image extension. Options: auto | jpg | png, auto means using the same extension as inputs. Default: auto
```


## :european_castle: Model Zoo

Please see [docs/model_zoo.md](docs/model_zoo.md)

## :computer: Training and Finetuning on your own dataset

A detailed guide can be found in [Training.md](Training.md).

## BibTeX

    @InProceedings{wang2021realesrgan,
        author    = {Xintao Wang and Liangbin Xie and Chao Dong and Ying Shan},
        title     = {Real-ESRGAN: Training Real-World Blind Super-Resolution with Pure Synthetic Data},
        booktitle = {International Conference on Computer Vision Workshops (ICCVW)},
        date      = {2021}
    }

## :e-mail: Contact

If you have any question, please email `xintao.wang@outlook.com` or `xintaowang@tencent.com`.

## :hugs: Acknowledgement

Thanks for all the contributors.

- [AK391](https://github.com/AK391): Integrate RealESRGAN to [Huggingface Spaces](https://huggingface.co/spaces) with [Gradio](https://github.com/gradio-app/gradio). See [Gradio Web Demo](https://huggingface.co/spaces/akhaliq/Real-ESRGAN).
- [Asiimoviet](https://github.com/Asiimoviet): Translate the README.md to Chinese (中文).
- [2ji3150](https://github.com/2ji3150): Thanks for the [detailed and valuable feedbacks/suggestions](https://github.com/xinntao/Real-ESRGAN/issues/131).
