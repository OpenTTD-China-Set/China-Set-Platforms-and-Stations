# Vox Readme

This folder contains all voxel models used to create the sprites. You could use any preferred to open `.vox` files. In our project, we used MagicaVoxel, which is availble on its official website.

## Vox types

All files that ends with `mirrored` means that they are mirrored model, and the script will not generate a separate `.pnml` file for them.

|Prefix|Meaning|
|---|---|
|pl1|**pl**atform **1** (symmetric)|
|pl2|**pl**atform **2** (asymmetric)|
|pl3|**pl**atform **3** (symmetric, no double sided version)|
|pl4|**pl**atform **4** (asymmetric, no double sided version)|
|bul|station **bu**i**l**ding|
|ful|**ful**l platform|
|wa1|**wa**ypoint **1** (symmetric)|
|wa2|**wa**ypoint **2** (asymmetric)|
|wa3|**wa**ypoint **3** (symmetric double sided)|

A standard voxel model file's name should have these componets:
```
plm_high_brown_something.vox
|   |    |     |
type|    |     style subtype, could be extended
    subtype
         style
```

## Voxel standards

|Type|height limit|remarks|
|---|---|---|
|high platforms|16vx||
|low platforms|12vx||

## Credits

Voxel models are created by NACHN, Dongfeng<sub>4</sub>3110 and WenSim
