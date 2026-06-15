import ctypes

# Windows volume key codes
VK_VOLUME_MUTE = 0xAD
VK_VOLUME_DOWN = 0xAE
VK_VOLUME_UP = 0xAF


def _press_key(key):
    ctypes.windll.user32.keybd_event(key, 0, 0, 0)
    ctypes.windll.user32.keybd_event(key, 0, 2, 0)


def set_volume(percent):
    percent = max(0, min(100, int(percent)))

    # reset by lowering volume a lot
    for _ in range(50):
        _press_key(VK_VOLUME_DOWN)

    # raise to target
    steps = int(percent / 2)

    for _ in range(steps):
        _press_key(VK_VOLUME_UP)


def volume_max():
    set_volume(100)


def volume_mute():
    _press_key(VK_VOLUME_MUTE)


def volume_unmute():
    _press_key(VK_VOLUME_MUTE)


def get_volume():
    # Windows does NOT expose simple API here via this method
    return -1