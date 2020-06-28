#!/usr/bin/env python3

import sys
import pyotp
import qrcode

import base64
import otpauth_migration_pb2

with open(sys.argv[1], 'rb') as f:
    data = f.read()
    data = base64.b64decode(data)

    read = otpauth_migration_pb2.MigrationPayload()
    read.ParseFromString(data)
    for otp_parameters in read.otp_parameters:
        otp_parameters.secret = base64.b32encode(otp_parameters.secret)
        print(otp_parameters)

        totp = pyotp.totp.TOTP(otp_parameters.secret).provisioning_uri(otp_parameters.name, otp_parameters.issuer)
        url = str(totp).replace('%3D', '')
        qr = qrcode.QRCode()
        qr.add_data(url)
        qr.print_ascii(invert=True)
        print(url)
        print("=================================================================================")
