# coding=utf-8
# Copyright (c) 2025 Jifeng Wu
# Licensed under the MIT License. See LICENSE file in the project root for full license information.
import sys

from detect_qt_binding import detect_qt_binding, QtBindings
from numpy import frombuffer, ndarray, uint8

if sys.byteorder != 'little':
    raise RuntimeError('This function only supports little-endian systems.')

QT_BINDING = detect_qt_binding()
if QT_BINDING == QtBindings.PyQt6:
    from PyQt6.QtGui import QImage

    Format_RGB32 = QImage.Format.Format_RGB32
    Format_ARGB32 = QImage.Format.Format_ARGB32


    def get_buffer(qimage):
        voidptr = qimage.constBits()
        voidptr.setsize(qimage.sizeInBytes())
        return voidptr
elif QT_BINDING == QtBindings.PySide6:
    from PySide6.QtGui import QImage

    Format_RGB32 = QImage.Format.Format_RGB32
    Format_ARGB32 = QImage.Format.Format_ARGB32


    def get_buffer(qimage):
        return qimage.constBits()
elif QT_BINDING == QtBindings.PyQt5:
    from PyQt5.QtGui import QImage

    Format_RGB32 = QImage.Format_RGB32
    Format_ARGB32 = QImage.Format_ARGB32


    def get_buffer(qimage):
        voidptr = qimage.constBits()
        voidptr.setsize(qimage.sizeInBytes())
        return voidptr
elif QT_BINDING == QtBindings.PySide2:
    from PySide2.QtGui import QImage

    Format_RGB32 = QImage.Format_RGB32
    Format_ARGB32 = QImage.Format_ARGB32


    def get_buffer(qimage):
        return qimage.constBits()
elif QT_BINDING == QtBindings.PyQt4:
    from PyQt4.QtGui import QImage

    Format_RGB32 = QImage.Format_RGB32
    Format_ARGB32 = QImage.Format_ARGB32


    def get_buffer(qimage):
        voidptr = qimage.constBits()
        voidptr.setsize(qimage.byteCount())
        return voidptr
elif QT_BINDING == QtBindings.PySide:
    from PySide.QtGui import QImage

    Format_RGB32 = QImage.Format_RGB32
    Format_ARGB32 = QImage.Format_ARGB32


    def get_buffer(qimage):
        return qimage.constBits()
else:
    raise ImportError(
        'We require one of PyQt6, PySide6, PyQt5, PySide2, PyQt4, or PySide. '
        'None of these packages were detected in your Python environment.'
    )


def qimage_to_hwc_bgrx_8888_ndarray_view(qimage):
    # type: (QImage) -> ndarray
    """
    Return a zero-copy HWC BGRX 8888 ndarray view of a QImage.
    NOTE: QImage must outlive the ndarray!
    """
    height = qimage.height()
    width = qimage.width()
    bytes_per_line = qimage.bytesPerLine()

    if qimage.format() not in (Format_RGB32, Format_ARGB32) or bytes_per_line != width * 4:
        raise ValueError('QImage must be in Format_RGB32 or Format_ARGB32 and tightly packed.')

    buffer = get_buffer(qimage)

    return frombuffer(buffer, dtype=uint8).reshape(height, width, -1)


def qimage_to_hwc_bgrx_8888_ndarray(qimage):
    """
    Return a copy of QImage data as HWC BGRX 8888 ndarray.
    """
    return qimage_to_hwc_bgrx_8888_ndarray_view(qimage).copy()


def hwc_bgrx_8888_ndarray_to_qimage_view(hwc_bgrx_8888_ndarray):
    # type: (ndarray) -> QImage
    """
    Return QImage wrapping the provided ndarray's memory (zero-copy).
    CAUTION: Do not modify or garbage-collect ndarray while QImage is alive!
    """
    height, width, channels = hwc_bgrx_8888_ndarray.shape
    if channels != 4 or hwc_bgrx_8888_ndarray.dtype != uint8 or not hwc_bgrx_8888_ndarray.flags['C_CONTIGUOUS']:
        raise ValueError('ndarray must be in HWC BGRX 8888 format and C contiguous.')

    bytes_per_line = width * 4
    # Will use Format_ARGB32 (works: Qt ignores the alpha for BGRX; it's just a matter of byte order)
    return QImage(hwc_bgrx_8888_ndarray.data, width, height, bytes_per_line, Format_ARGB32)


def hwc_bgrx_8888_ndarray_to_qimage(hwc_bgrx_8888_ndarray):
    # type: (ndarray) -> QImage
    """
    Return a detached QImage copy from numpy array.
    """
    return hwc_bgrx_8888_ndarray_to_qimage_view(hwc_bgrx_8888_ndarray).copy()
