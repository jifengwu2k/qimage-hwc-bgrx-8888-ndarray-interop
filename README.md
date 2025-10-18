# `qimage-hwc-bgrx-8888-ndarray-interop`

Zero-copy conversion between Qt QImage (in `Format_RGB32`/`Format_ARGB32`) and NumPy ndarray (in HWC BGRX 8888 format).

## Features

- Zero-copy: Memory is shared between objects - no pointless data copying!
- Cross-binding: Supports PyQt6, PyQt5, PyQt4, PySide6, PySide2, or PySide.
- Safety: Explicit checks for packing and format - no surprises.

## Installation

Install your preferred Qt binding, then run:

```bash
pip install qimage-hwc-bgrx-8888-ndarray-interop
```

## Usage

```python
# coding=utf-8
from qimage_hwc_bgrx_8888_ndarray_interop import (
    qimage_to_hwc_bgrx_8888_ndarray_view,
    qimage_to_hwc_bgrx_8888_ndarray,
    hwc_bgrx_8888_ndarray_to_qimage_view,
    hwc_bgrx_8888_ndarray_to_qimage,
)

# Convert a QImage to numpy.ndarray (zero-copy view):
arr_view = qimage_to_hwc_bgrx_8888_ndarray_view(qimage)

# Convert a QImage to a copy of image data:
arr = qimage_to_hwc_bgrx_8888_ndarray(qimage)

# Convert a contiguous (H, W, 4) uint8 ndarray back to a QImage (zero-copy view):
qimg_view = hwc_bgrx_8888_ndarray_to_qimage_view(arr)

# Convert ndarray to a QImage (copies data):
qimg_copy = hwc_bgrx_8888_ndarray_to_qimage(arr)
```

## Safety & Caveats

- Endianness: Only little-endian systems are supported (typical modern computers).
    - On unsupported (big-endian) systems, `RuntimeError` is raised at import time.
- Tightly packed images only: QImage must have `bytesPerLine == width * 4` for zero-copy view.
- **Memory lifetime matters:**
    - Do **not** let the QImage or ndarray be garbage collected while the other exists and references its buffer.
    - If in doubt, use the `copy()` variants.

## Contributing

Contributions are welcome! Please submit pull requests or open issues on the GitHub repository.

## License

This project is licensed under the [MIT License](LICENSE).