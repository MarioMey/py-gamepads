# py-gamepads 0.2
Connect several bluetooth gamepads (like the images) via Python.
<p>
<img src="https://user-images.githubusercontent.com/4954109/124144597-7e90c880-da62-11eb-9a19-f3bd5ef61551.png" alt="drawing" width="200"/>
<img src="https://user-images.githubusercontent.com/4954109/124145124-e9420400-da62-11eb-816d-0e94f513c754.png" alt="drawing" width="200"/>
</p>

### Usage

```
bt_gamepads.py [--gp1 input1] [--gp2 input2]

    --gp1: Number of input event in `/dev/input/event*` of gamepad 1. Default: 16.
    --gp2: Number of input event in `/dev/input/event*` of gamepad 2. Default: 20.
```
### Example
`python3.7 bt_gamepads.py --gp1 16 --gp2 20`
### Description
It connects gamepads using `evdev` by taking data from `/dev/input/event*`. My defaults events for my two gamepads are 16 and 20. But, by turning them on and off, sometimes, they goes to 17 and 21. So, code check once a second if device in event16 (as default or set by its command line) is turned on. If so, it connects to it and start receiving data and print it. If it is not connected, it tries at event16+1 (event17). The same for event20 (and event21).

Gamepads could be turned on before or after running code and they can be turned off and on when code is running. This is possble because there is a thread that checks every second their state.

Because I use this exact python file with my project, it loads a personal `obs_api.py` file (that loads real OBS python API). If you run it, as it doesn't find it, it loads an alternative `obs_api_no_obs.py` file that doesn't load OBS API. See what's inside that file, change or remove what you want.

Code includes OSC functions to send OSC messages. It needs `pythonosc`.

## Modules:
- evdev: https://python-evdev.readthedocs.io
- pythonosc: https://python-osc.readthedocs.io



