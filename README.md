# NDTkit Python API Examples

![NDTkit Python API examples](https://img.shields.io/badge/NDTkit_API_examples-Python-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 💻 Overview

This repository provides **usage examples** for the Python API designed to interact with the **[NDTkit](https://www.testia.com/product/ndtkit-ut/)** software.

---

## 🚀 Getting Started

### Prerequisites

1.  **Python 3.11+**
2.  **NDTkit** installed and launched

### Installation

Clone this repository and install the necessary dependencies:

```bash
git clone https://github.com/cedric-bertrand-testia/ndtkit-python-api-examples.git
cd ndtkit-python-api-examples
pip install -r requirements.txt
```

### Usage Example

Here is a simple example showing how to apply a global gain to a C-Scan.

```python
from ndtkit_api import NDTKitCScanInterface
from ndtkit_api.model.frame.NICartographyFrameCScan import NICartographyFrameCScan
from ndtkit_api.model.NIEnumSpecialValue import NIEnumSpecialValue


def apply_gain(cscan: NICartographyFrameCScan, gain: float):
    data: list[list[float]] = cscan.get_data()
    data_gain = []
    for row in data:
        data_gain.append([value * gain if not NIEnumSpecialValue.is_special_value(value) else value for value in row])
    cscan.set_data(data_gain)
    cscan.get_palette().real_limits()


if __name__ == "__main__":
    input_cscan_path = "path/to/cscan"
    output_cscan_path = "output/path"

    cscan = NDTKitCScanInterface.open_cscan(input_cscan_path, True)
    apply_gain(cscan, 2)
    NDTKitCScanInterface.save_cscan(cscan, output_cscan_path)

```
