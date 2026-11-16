#!/usr/bin/env python3
import manuver as m

TINGGI_MAZE = 1.3
BATAS_TINGGI_DINDING = 1.96
TINGGI_BAWAH_BALOK = 1.0
JARAK_DINDING = 0.43
JARAK_SEKAT = 0.70


def pintu_maze(d):
    d.info('R0: cari pintu maze')
    d.naik_ke(TINGGI_MAZE)
    m.geser_sampai(d, lambda d: d.lidar['front'] < 8.0, kanan=1.5, jarak_maks=25.0)
    m.geser_sampai(d, lambda d: d.lidar['front'] > 5.0, kanan=0.5, jarak_maks=4.0)
    d.pindah(kanan=0.4, kecepatan=0.4, toleransi=0.06)


def zigzag(d):
    d.info('R1: sekat zig-zag')
    m.susur(d, lambda d: d.lidar['front'] < JARAK_SEKAT + 0.02, tinggi=TINGGI_MAZE, sisi='right', jarak=JARAK_DINDING)
    m.geser_jaga_depan(d, -1, JARAK_SEKAT, lambda d: d.lidar['front'] > 3.0)
    m.geser_sampai(d, lambda d: d.lidar['left'] < JARAK_DINDING + 0.3, kanan=-0.3, jarak_maks=1.5)
    m.geser_sampai(d, lambda d: d.lidar['left'] < JARAK_DINDING + 0.04, kanan=-0.12, jarak_maks=0.6)
    m.susur(d, lambda d: d.lidar['front'] < 1.0, tinggi=TINGGI_MAZE, sisi='left', jarak=JARAK_DINDING)


def sekat_rendah(d):
    d.info('R2: sekat rendah')
    tinggi = m.naik_sampai_depan_kosong(d, 0.3, BATAS_TINGGI_DINDING)
    d.info('Lompat sekat di ketinggian %.2f m' % tinggi)
    m.susur(d, m.lewat('down', 0.6, 1.0), tinggi=tinggi, sisi='left', jarak=JARAK_DINDING, kecepatan=0.4)
    d.pindah(maju=0.3, kecepatan=0.4)


def pilar(d):
    d.info('R3: lingkaran ungu, pilar + balok')
    if m.maju_sampai_lingkaran(d, 'ungu', jarak_maks=2.5):
        m.sejajarkan_bawah(d, 'ungu')
    d.naik_ke(TINGGI_BAWAH_BALOK)
    m.geser_sampai(d, lambda d: d.lidar['left'] < 0.57, kanan=-0.3, jarak_maks=1.5)
    m.susur(d, m.lewat('right', 1.5, 1.5), tinggi=TINGGI_BAWAH_BALOK)


def terowongan(d):
    d.info('R4: terowongan')
    tinggi_bukaan = m.tengah_bukaan_tegak(d)
    lebar = m.tengah_bukaan(d)
    tinggi = d.z
    d.info('Mulut pipa: lebar %.2f m, tinggi %.2f m, masuk di ketinggian %.2f m' % (lebar, tinggi_bukaan, tinggi))
    m.susur(d, lambda d: d.lidar['front'] < 0.6, tinggi=tinggi, tengah_vertikal=True)
    tinggi = m.naik_sampai_depan_kosong(d, 0.6, 4.0)
    d.info('Naik ke lantai atas di ketinggian %.2f m' % tinggi)
    m.susur(d, m.lewat('down', 1.5, 2.0), tinggi=tinggi, kecepatan=0.6)
    d.pindah(maju=0.7, kecepatan=0.6)


def jalur_kanan(d):
    pintu_maze(d)
    zigzag(d)
    sekat_rendah(d)
    pilar(d)
    terowongan(d)


if __name__ == '__main__':
    from drone import buat_drone
    d = buat_drone()
    try:
        d.takeoff(TINGGI_MAZE)
        jalur_kanan(d)
        d.info('Jalur kanan selesai')
    finally:
        d.mendarat()
