# Source Code Folder Readme

This folder contains the nml source code used in CNSP.

This is an example:
```js
// this file includes explaination for each part of the station definition

// spirte layout for the station, defines the ground and building sprites
// for each station tile there should be two spritelayouts, one for x and another for y
spritelayout teststation_x {
    ground {
        sprite: GROUNDSPRITE_RAIL_X; //this is the ground sprite, using GROUNDSPRITE_RAIL_X will make it use the rail sprite and allowing trains to pass through
    }
    building {
        sprite: spriteset_old_high_x; // this is the building sprite, it uses the spriteset below
    }
}

spritelayout teststation_y {
    ground {
        sprite: GROUNDSPRITE_RAIL_Y; // same as above but for y
    }
    building {
        sprite: spriteset_old_high_y;
    }
}

// spriteset for the station, defines the sprites for the station
// for each station tile there should be two spritesets, one for x and another for y
spriteset (spriteset_old_high_x) {
    template_empty()
}
alternative_sprites (spriteset_old_high_x, ZOOM_LEVEL_IN_4X, BIT_DEPTH_32BPP) {
    template_standard_x("BasicPlatformHighToLow_4x")
}
spriteset (spriteset_old_high_y) {
    template_empty()
}
alternative_sprites (spriteset_old_high_y, ZOOM_LEVEL_IN_4X, BIT_DEPTH_32BPP) {
    template_standard_y("BasicPlatformHighToLow_4x")
}

// station definition
// this is the actual station definition, it defines the station name, class, and graphics
item (FEAT_STATIONS, stn_old_high) {
    property {
        class:"CNS1";
        classname: string(STR_CLS_CNP);
        name: string(STR_NAME_OLD_HIGH);
        //draw_pylon_tiles: 0;
		//hide_wire_tiles: 0xFF;
		//non_traversable_tiles: 0xFF;
    }
    graphics {
        // station callbacks
        sprite_layouts: [teststation_x, teststation_y]; // used graphics for station, follows [x, y] format
        spriteset_old_high_x; // default spriteset for station
    }
}

```