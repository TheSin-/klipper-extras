# Unconditional Stop - M0
Adds `M0` to klipper

This is the same as `PAUSE` but doesn't use the macros, incase you want base PAUSE to replace something like `M112`.  Though the same rules of `PAUSE` apply and the certain commands need to finish before it'll run.

# Install
ssh into your klipper system
```
get clone https://github.com/TheSin-/klipper-extras.git thesin-klipper-extras
ln -s thesin-klipper-extras/unconditional_stop/unconditional_stop.py ~/klipper/klippy/extras/
sudo service klipper restart
```

# Config
add a section in the config to enable

```
[unconditional_stop]
```

# Update manager
Add this to moonraker.conf
```
[update_manager thesin-klipper-extras]
type: git_repo
path: ~/thesin-klipper-extras
origin: https://github.com/TheSin-/klipper-extras.git
managed_services: klipper
```
