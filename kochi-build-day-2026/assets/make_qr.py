# Usage: python make_qr.py "<url>" out.png
import sys, qrcode
img = qrcode.make(sys.argv[1], box_size=14, border=3)
img.save(sys.argv[2]); print("saved", sys.argv[2])
