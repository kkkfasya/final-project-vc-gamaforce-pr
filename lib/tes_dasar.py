#!/usr/bin/env python3
from lib.drone import buat_drone

d = buat_drone()
try:
    d.takeoff(2.0)
    d.pindah(maju=3.0, kanan=3.0)
    d.info('posisi (%.2f, %.2f, %.2f) lidar %s' % (d.x, d.y, d.z, {k: round(v, 2) for k, v in d.lidar.items()}))
    d.putar(-90)
    d.pindah(maju=-3.0, kanan=3.0)
    d.putar(90)
    d.naik_ke(1.5)
    d.info('posisi (%.2f, %.2f, %.2f) kamera depan %s' % (d.x, d.y, d.z, None if d.gambar['front'] is None else d.gambar['front'].shape))
finally:
    d.mendarat()
