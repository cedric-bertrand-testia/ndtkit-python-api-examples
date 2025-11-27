from ndtkit_api import NDTKitCScanInterface
from ndtkit_api.model.frame.NICartographyFrameCScan import NICartographyFrameCScan
from ndtkit_api.model.NIEnumSpecialValue import NIEnumSpecialValue

""" Parameters """
input_cscan_path = "path/to/cscan"
output_cscan_path = "output/path"


def apply_gain(cscan: NICartographyFrameCScan, gain: float):
    """
    Applies a specified gain factor to the C-Scan amplitude data.
    Special values (NoE, MASK, NaN,) are preserved and not multiplied by the gain.

    :param cscan: The NICartographyFrameCScan object to modify.
    :param gain: The multiplication factor (gain) to apply to the amplitude values.
    """
    # Retrieve the C-Scan's amplitude data (typically a 2D list of floats).
    data: list[list[float]] = cscan.get_data()
    data_gain = []

    # Iterate through each row (scan line) in the data.
    for row in data:
        # Apply the gain to each value, but only if it's not a special value.
        data_gain.append([value * gain if not NIEnumSpecialValue.is_special_value(value) else value for value in row])

    # Update the C-Scan object with the new gain-adjusted data.
    cscan.set_data(data_gain)

    # Recalculate the palette limits based on the new data range.
    cscan.get_palette().real_limits()


if __name__ == "__main__":
    # Open the C-Scan file using the interface (the 'True' might indicate read/write mode or synchronization).
    cscan = NDTKitCScanInterface.open_cscan(input_cscan_path, True)

    # Execute the gain application function with a gain factor of 2.
    apply_gain(cscan, 2)

    # Save the modified C-Scan data to the specified output path.
    NDTKitCScanInterface.save_cscan(cscan, output_cscan_path)
