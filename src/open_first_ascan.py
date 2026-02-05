from ndtkit_api import NDTKitAScanInterface
from ndtkit_api.model.frame.NICartographyFrameAScan import NICartographyFrameAScan
from ndtkit_api.model.readers import NIReaderHelper
from ndtkit_api.model.NIEnumScanType import NIEnumScanType


"""
Some file format contains several acquisition files. This example shows how to open the first A-Scan frame in such file.
If the file doesn't contain several acquisition files, it will simply open the A-Scan frame.
"""

""" Parameters """
input_acquisition_path = "path/to/ascan"


def get_first_ascan_frame(file_path: str) -> NICartographyFrameAScan | None:
    """Helper function to get the first A-Scan frame from a file."""
    nodes = NIReaderHelper.getAvailableLeafNodes(file_path)

    if not nodes:
        return NDTKitAScanInterface.open_ascan(file_path)
    else:
        for node in nodes:
            if node.get_scan_type() == NIEnumScanType.ASCAN:
                return NDTKitAScanInterface.open_ascan(file_path, node.get_node_id())
    return None


if __name__ == "__main__":
    ascan = get_first_ascan_frame(input_acquisition_path)
    if ascan:
        print(f"Column number: {ascan.get_column_number()}")
        print(f"Row number: {ascan.get_row_number()}")
    else:
        print("No A-Scan found in the file.")
