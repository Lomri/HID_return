# Requires pywinusb
#
# This can be used to:
# - get your connected HID devices
# - listen for a selected HID device
#
# USAGE:
# find_devices() returns a list of HID devices
# autodetect(optional_keyword) tries to autodetect a game controller for you. might not work, and -
# you can use your own keyword to search for it as well.
# assign() to start listening for a device
# sample_handler() gets then triggered from inputs and returns the keypresses
# call close_device() if you wish to stop listening for the device

import pywinusb.hid as hid

hid_filter = hid.HidDeviceFilter()
all_devices = hid_filter.get_devices()
device = None


def find_devices():
    hidlist = []
    if all_devices:  # Found some HID devices
        for i in 0, (len(all_devices) - 1):
            hidlist.append(all_devices[i])
        return hidlist
    # Returns: List of connected HID Devices with one Device in each index starting from [0]
    # Purpose: To get a list of all connected HID Devices


def autodetect(searchable="defaultvariable"):
    #  You can input a string variable to be searched in autodetection. Not required.
    list_1 = []

    for i in 0, ((len(all_devices)) - 1):  # iterate through all HID Devices
        if (str("ig_") or  # This is a string present in xinput (xbox etc.) controllers
                str.lower(searchable) or  # Case-sensitiveness
                str(searchable)) in str(all_devices[i]):

            iterable = str(all_devices[i])
            controller_vid = ''
            for v in range(16, 22):  # We know from experience a vID is listed in this spot
                # Grab the vendor id of the device
                controller_vid += str(iterable[v])
            list_1.append(controller_vid)  # put the vID in a list

    if list_1:
        return list_1
    else:
        return False

    # Returns: A list of device id's -
    # that are probably those of a gamepad's. If autodetection fails, returns False
    # Purpose: Works with 0 or more HID devices. Easily returns vID's for devices that are interesting.
    # Note: you can't use the list item directly to open the device, since the list item is a string
    # while the device id needs to be converted to int in base 16 (in python use int(controller_vid, 16)


def sample_handler(data):
    return data
    # Returns: A list of integers when a button is pressed or released on a controller
    # sample list: [0, 128, 128, 127, 127, 128, 128, 127, 127, 0, 128, 0, 0, 0, 0]
    # buttons in my controller (Logitech F710, should be same as xbox controller):
    # [0] = None
    # [1] = left stick x (left = decreases to min 0, right = increases to max 255, 128 by default)
    # [2] = same as [1]
    # [3] = left stick y (up = decreases to min 0, down = increases to max 255, 127 by default)
    # [4] = same as [3]
    # [5] = right stick x (left = decreases to min 0, right = increases to max 255, 128 by default)
    # [6] = same as [5]
    # [7] = right stick y (up = decreases to min 0, down = increases to max 255, 127 by default)
    # [8] = same as [7]
    # [9] = Unknown, something to do with Triggers, seems to set itself to 128 somewhat randomly
    # [10] = BOTH Triggers (R down pressed = 0, increases linearly to 128 max when released,
    # L released = 128, increases when down pressed to 255 max)
    # [11] = Multifunction as follows:
    # A: 1
    # B: 2
    # X: 4
    # Y: 8
    # Left Bumper (LB): 16
    # Right Bumper (RB): 32
    # Select / Back: 64
    # Start: 128
    # [12] =
    # Left stick press: 1
    # Right stick press: 2
    # D Up: 4
    # D Right: 12
    # D Down: 20
    # D Left: 28
    # [13] = None
    # [14] = None
    #
    # Purpose: function can be interrupted and a separate program can then listen to it -
    # function gets called always when there is a button press when the device is opened with assign function


def assign(vid):
    try:
        vid = int(vid, 16)  # Conversion required
        hid_filter = hid.HidDeviceFilter(vendor_id=vid)
        device = hid_filter.get_devices()[0]
        device.open()
        device.set_raw_data_handler(sample_handler)  # sample_handler function is now listening
        return True

    except NameError as e:
        return False  # no device was assigned

    # Returns: True if the device was assigned, False if not
    # Purpose: To assign and open a device to be listened to -
    # Use sample_handler function to get key presses after opening
    # Use close_device function to close the device if you wish to continue with your program & stop listening
    # You can also use built-in device.is_plugged() to run a while loop, for example


def close_device():
    if device:
        device.close()
        return True
    else:
        return False

    # Returns: True if the device was closed, False if it was not even assigned
    # Purpose: To quit from listening the device. This can be used if you wish to continue your program -
    # but end the listening
    # AFAIK this doesn't break anything if you never close the device, it closes when the program exits.
