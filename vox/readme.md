# Vox Readme

This folder contains all voxel models used to create the sprites. You could use any preferred to open `.vox` files. In our project, we used MagicaVoxel, which is availble on its official website.

## Vox types

All files that ends with `mirrored` means that they are mirrored model, and the script will not generate a separate `.pnml` file for them.

|Prefix|Meaning|
|---|---|
|plt|station **pl**a**t**form|
|plm|station **pl**atform **m**irrored|
|pls|station **pl**atform **s**ingle sided|
|psm|station **p**latform **s**ingle sided **m**irrored|
|bul|station **bu**i**l**ding|
|bum|station **bu**ilding **m**irrored|
|ful|**ful**l platform|

A standard voxel model file's name should have these componets:
```
plm_high_brown_something_mirrored.vox
|   |    |     |         |
type|    |     |         mirrored mark, necessary for some
    subtype    |         platform types e.g. plm and bul
         style |
               style subtype, could be extended
```

## Credits

|Filename|Author|Remarks|
|---|---|---|
|stn_high_old|WenSim|
|stn_high_to_low_old|WenSim
|stn_high_to_stairs|WenSim
|stn_low_old|WenSim
|stn_low_to_none_old|WenSim
|stn_stairs_old|WenSim
|stn_stairs_to_low_old|WenSim