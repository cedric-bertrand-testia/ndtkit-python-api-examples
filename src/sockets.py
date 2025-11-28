"""
This example demonstrates how to control the application by sending raw command messages over a socket connection.

This approach is particularly useful in two scenarios:
1. **Interoperability**: It proves that the API is language-agnostic. You can control the Java application from *any* programming language that supports sockets (C#, C++, MATLAB, etc.), not just Python.
2. **Access to Full Java API**: It allows you to invoke *any* Java method found in the project's Javadoc, even if that specific function has not yet been exposed or wrapped in the official high-level Python library. By specifying the class and method names dynamically, you bypass the limitations of the standard wrapper.
"""

from ndtkit_api.ndtkit_socket_connection import call_api_method
from typing import List, Dict, Any

""" Parameters"""
INPUT_CSCAN_PATH = "path/to/cscan"
DEFECT_THRESHOLD = 12


def reset_environment():
    """Closes all currently open frames in the application."""
    call_api_method("agi.ndtkit.api", "NDTKitCartographyFrameInterface", "closeAllFrames", [])


def load_cscan(file_path: str) -> str:
    """
    Opens a C-Scan file and returns its UUID.
    """
    parameters = [
        {
            "type": "java.lang.String",
            "value": file_path,
        }
    ]
    result = call_api_method("agi.ndtkit.api", "NDTKitCScanInterface", "openCScan", parameters)
    # Assuming result is a list of frames, we return the UUID of the first one
    return result[0]["uuid"]


def get_cscan_data(cscan_uuid: str) -> List[List[float]]:
    """Retrieves the raw data matrix from the C-Scan."""
    parameters = [
        {
            "type": "agi.ndtkit.api.model.frame.NICartographyFrameCScan",
            "value": cscan_uuid,
        }
    ]
    return call_api_method("agi.ndtkit.api.model.frame", "NICartographyFrameCScan", "getData", parameters)  # type: ignore


def compute_binary_mask(data: List[List[float]], threshold: float) -> List[List[bool]]:
    """
    Processes the raw data locally to create a boolean matrix 
    where True indicates a value above the threshold.
    """
    boolean_matrix = []
    for row in data:
        boolean_matrix.append([value > threshold for value in row])
    return boolean_matrix


def apply_defects(cscan_uuid: str, boolean_matrix: List[List[bool]]) -> List[Dict[str, Any]]:
    """
    Sends the computed binary mask back to the API to generate defect objects.
    """
    parameters = [
        {
            "type": "boolean[][]",
            "value": str(boolean_matrix),
        },
        {
            "type": "agi.ndtkit.api.model.frame.NICartographyFrameCScan",
            "value": cscan_uuid,
        },
        {
            "type": "agi.ndtkit.api.model.NIEnumDefectShapeType",
            "value": "RECTANGLE_FITTING",
        }
    ]
    return call_api_method("agi.ndtkit.api", "NDTKitDefectDetectionInterface", "applyDefects", parameters)  # type: ignore


if __name__ == "__main__":

    # 1. Cleanup
    reset_environment()

    # 2. Load Data
    uuid = load_cscan(INPUT_CSCAN_PATH)

    # 3. Get Data
    raw_data = get_cscan_data(uuid)

    # 4. Process Data (Local Logic)
    mask = compute_binary_mask(raw_data, DEFECT_THRESHOLD)

    # 5. Apply Results
    defects = apply_defects(uuid, mask)

    print(f"{len(defects)} defects have been found")
