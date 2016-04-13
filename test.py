#!/usr/bin/env python

"""
Hopefully clear instructions on how to deal with UBlox M8
- On my machine, the serial driver mounts it on /dev/cu.usbmodem1421
- Use 115200 baudrate
- Send CFG-PRT { portID = 3, reserved1 = 0, txReady = 0, reserved2 = 0, inProtoMask = 1, outProtoMask = 1, reserved3 = 0, reserved4 = 0 }
  This configures the USB interface with UBX input and output.
- Send CFG-MSG messages for all message types you care about.
  These will be triples (message class, message id, rate) where
  classes and ids are defined here https://www.u-blox.com/sites/default/files/products/documents/u-blox8-M8_ReceiverDescrProtSpec_(UBX-13003221)_Public.pdf
  And rates are, I think, messages emitted per measurement cycle? So 1?
"""

from ublox_m8 import UbloxM8Python

def handle(data, ts, id):
  print "MSG", ts, id, data

port = '/dev/cu.usbmodem1421'
baud = 115200

# message classes
CLASS_NAV = 0x01
CLASS_RXM = 0x02
CLASS_INF = 0x04
CLASS_ACK = 0x05
CLASS_CFG = 0x06
CLASS_MON = 0x0A
CLASS_AID = 0x0B
CLASS_TIM = 0x0D
CLASS_ESF = 0x10

# ACK messages
MSG_ACK_NACK = 0x00
MSG_ACK_ACK = 0x01

# NAV messages
MSG_NAV_POSECEF   = 0x1
MSG_NAV_POSLLH    = 0x2
MSG_NAV_STATUS    = 0x3
MSG_NAV_DOP       = 0x4
MSG_NAV_SOL       = 0x6
MSG_NAV_POSUTM    = 0x8
MSG_NAV_VELNED    = 0x12
MSG_NAV_VELECEF   = 0x11
MSG_NAV_TIMEGPS   = 0x20
MSG_NAV_TIMEUTC   = 0x21
MSG_NAV_CLOCK     = 0x22
MSG_NAV_SVINFO    = 0x30
MSG_NAV_AOPSTATUS = 0x60
MSG_NAV_DGPS      = 0x31
MSG_NAV_DOP       = 0x04
MSG_NAV_EKFSTATUS = 0x40
MSG_NAV_SBAS      = 0x32
MSG_NAV_SOL       = 0x06

# RXM messages
MSG_RXM_RAW    = 0x10
MSG_RXM_SFRB   = 0x11
MSG_RXM_SVSI   = 0x20
MSG_RXM_EPH    = 0x31
MSG_RXM_ALM    = 0x30
MSG_RXM_PMREQ  = 0x41

# AID messages
MSG_AID_ALM    = 0x30
MSG_AID_EPH    = 0x31
MSG_AID_ALPSRV = 0x32
MSG_AID_AOP    = 0x33
MSG_AID_DATA   = 0x10
MSG_AID_ALP    = 0x50
MSG_AID_DATA   = 0x10
MSG_AID_HUI    = 0x02
MSG_AID_INI    = 0x01
MSG_AID_REQ    = 0x00

# CFG messages
MSG_CFG_PRT = 0x00
MSG_CFG_ANT = 0x13
MSG_CFG_DAT = 0x06
MSG_CFG_EKF = 0x12
MSG_CFG_ESFGWT = 0x29
MSG_CFG_CFG = 0x09
MSG_CFG_USB = 0x1b
MSG_CFG_RATE = 0x08
MSG_CFG_SET_RATE = 0x01
MSG_CFG_NAV5 = 0x24
MSG_CFG_FXN = 0x0E
MSG_CFG_INF = 0x02
MSG_CFG_ITFM = 0x39
MSG_CFG_MSG = 0x01
MSG_CFG_NAVX5 = 0x23
MSG_CFG_NMEA = 0x17
MSG_CFG_NVS = 0x22
MSG_CFG_PM2 = 0x3B
MSG_CFG_PM = 0x32
MSG_CFG_RINV = 0x34
MSG_CFG_RST = 0x04
MSG_CFG_RXM = 0x11
MSG_CFG_SBAS = 0x16
MSG_CFG_TMODE2 = 0x3D
MSG_CFG_TMODE = 0x1D
MSG_CFG_TPS = 0x31
MSG_CFG_TP = 0x07

# ESF messages
MSG_ESF_MEAS   = 0x02
MSG_ESF_STATUS = 0x10

# INF messages
MSG_INF_DEBUG  = 0x04
MSG_INF_ERROR  = 0x00
MSG_INF_NOTICE = 0x02
MSG_INF_TEST   = 0x03
MSG_INF_WARNING= 0x01

# MON messages
MSG_MON_SCHD  = 0x01
MSG_MON_HW    = 0x09
MSG_MON_HW2   = 0x0B
MSG_MON_IO    = 0x02
MSG_MON_MSGPP = 0x06
MSG_MON_RXBUF = 0x07
MSG_MON_RXR   = 0x21
MSG_MON_TXBUF = 0x08
MSG_MON_VER   = 0x04

# TIM messages
MSG_TIM_TP   = 0x01
MSG_TIM_TM2  = 0x03
MSG_TIM_SVIN = 0x04
MSG_TIM_VRFY = 0x06

rates = [
  (CLASS_NAV, MSG_NAV_POSECEF, 1),
  (CLASS_NAV, MSG_NAV_POSLLH, 1),
  (CLASS_NAV, MSG_NAV_SVINFO, 1),
  (CLASS_NAV, MSG_NAV_VELECEF, 1),
  (CLASS_NAV, MSG_NAV_VELNED, 1),
  (CLASS_RXM, MSG_RXM_RAW, 1),
  (CLASS_RXM, MSG_RXM_SFRB, 1)
]

# Create wrapper and set callbacks
ub = UbloxM8Python(port)
ub.python_set_nav_posecef_callback(handle)
ub.python_set_nav_posllh_callback(handle)
ub.python_set_nav_svinfo_callback(handle)
ub.python_set_nav_velecef_callback(handle)
ub.python_set_nav_velned_callback(handle)
ub.python_set_rxm_rawx_callback(handle)
ub.python_set_rxm_sfrbx_callback(handle)

try:
  # Connect, which sets CFG-PRT to be USB with UBX in/out
  assert ub.Connect(port, baud)
  for (klass, id, rate) in rates:
    # Register for various messages
    assert ub.SetCfgMsgRate(klass, id, rate)
  raw_input('Press enter to stop')
finally:
  ub.Disconnect()
