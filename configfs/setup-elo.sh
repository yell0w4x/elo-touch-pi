#!/usr/bin/env bash

# Elotouch configfs setup file
# 2020 (c) Gk Ltd.

TARGET_DIR="${1:-/sys/kernel/config/usb_gadget/}"

if [ ! -d "${TARGET_DIR}" ]; then
    logger "Can't setup elotouch the directory ${TARGET_DIR} doesn't exist"
    exit 1
fi 

ELOTOUCH_DIR=elotouch
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

cd "${TARGET_DIR}"
mkdir "${ELOTOUCH_DIR}"
cd "${ELOTOUCH_DIR}"

# -----------------------------------------------------------------------------
# device descriptor
# -----------------------------------------------------------------------------
echo 0x0110 > bcdUSB
echo 0 > bDeviceClass
echo 0 > bDeviceSubClass
echo 0 > bDeviceProtocol
echo 8 > bMaxPacketSize0
echo 0x04e7 > idVendor 
echo 0x0020 > idProduct 
echo 0x0201 > bcdDevice 

# device string descriptors
mkdir -p strings/0x409
echo "Elo TouchSystems 2700 IntelliTouch(r) USB Touchmonitor Interface" > strings/0x409/manufacturer 
echo "Elo TouchSystems, Inc." > strings/0x409/product 
echo "20L26392" > strings/0x409/serialnumber

# -----------------------------------------------------------------------------
# configuration descriptor
# -----------------------------------------------------------------------------
mkdir -p configs/conf.1
echo 0xe0 > configs/conf.1/bmAttributes
echo 0 > configs/conf.1/MaxPower

# configuration string descriptor
mkdir -p configs/conf.1/strings/0x409
echo "Model 2700" > configs/conf.1/strings/0x409/configuration

# -----------------------------------------------------------------------------
# interface descriptor
# -----------------------------------------------------------------------------
mkdir -p functions/hid.usb0
echo 0 > functions/hid.usb0/protocol
echo 0 > functions/hid.usb0/subclass
echo 8 > functions/hid.usb0/report_length
cat "${SCRIPT_DIR}/hid-report-descriptor.bin" > functions/hid.usb0/report_desc

# interface string descriptor
#mkdir -p functions/hid.usb0/strings/0x409
#echo "SmartSet Protocol" > functions/hid.usb0/strings/0x409/function

# assign function to configuration
ln -s functions/hid.usb0 configs/conf.1
# replace the name '20980000.usb' with one found under /sys/class/udc/ in your target system
echo 20980000.usb > UDC
