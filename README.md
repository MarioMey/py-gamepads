# py-gamepads 0.3
Connect several bluetooth gamepads (like the images) via Python.
<p>
<img src="https://user-images.githubusercontent.com/4954109/124144597-7e90c880-da62-11eb-9a19-f3bd5ef61551.png" alt="drawing" width="200"/>
<img src="https://user-images.githubusercontent.com/4954109/124145124-e9420400-da62-11eb-816d-0e94f513c754.png" alt="drawing" width="200"/>
</p>

### Usage

```
bt_gamepads.py [--c amount]

    --c: Amount of gamepads to connect. Default: 2
    
    While running:
    q: Quit
```
### Example
`python3.7 bt_gamepads.py --c 2`
### Description
It connects gamepads using `evdev` by taking data from `/dev/input/event*`. The code checks from 16 to 23 if there's any or some gamepads connected.

Gamepads could be turned on before or after running code and they can be turned off and on when code is running. This is possble because there is a thread that checks every second their state.

Because I use this exact python file with my project, it loads a personal `obs_api.py` file (that loads real OBS python API). If you run it, as it doesn't find it, it loads an alternative `obs_api_no_obs.py` file that doesn't load OBS API. See what's inside that file, change or remove what you want.

Code includes OSC functions to send OSC messages. It needs `pythonosc`.

## Modules:
- evdev: https://python-evdev.readthedocs.io
- pythonosc: https://python-osc.readthedocs.io
