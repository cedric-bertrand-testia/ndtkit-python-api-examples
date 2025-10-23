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
