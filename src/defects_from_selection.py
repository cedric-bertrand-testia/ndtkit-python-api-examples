from ndtkit_api import NDTKitCScanInterface, NDTKitDefectDetectionInterface, NDTKitROIInterface, NDTKitCartographyFrameInterface
from ndtkit_api.model.roi.NIRoiSelection import NIRoiSelection
from ndtkit_api.model.NIEnumSpecialValue import NIEnumSpecialValue
from ndtkit_api.model.flaw.NIEnumDefectCharacteristics import NIEnumDefectCharacteristics
from ndtkit_api.model.flaw.Flaw import Flaw


""" Parameters"""
input_cscan_path = "path/to/cscan"
defect_threshold = 12

"""
This example demonstrates how to detect defects in a C-Scan based on a simple thresholding method.
A boolean matrix is created where each cell indicates whether a defect is present based on the threshold.
The matrix is then used to detect the defects in the C-Scan.
"""

if __name__ == "__main__":
    cscan = NDTKitCScanInterface.open_cscan(input_cscan_path, True)
    data = cscan.get_data()
    nan_value = float(NIEnumSpecialValue.NAN.get_value())
    for row in range(len(data)):
        for col in range(len(data[0])):
            data[row][col] = data[row][col] if NIEnumSpecialValue.is_special_value(data[row][col]) or data[row][col] < defect_threshold else nan_value
    cscan.set_data(data)
    selection: NIRoiSelection = NDTKitROIInterface.add_rectangular_selection(cscan, 20, 15, 10, 10)
    NDTKitDefectDetectionInterface.apply_defect_detection(None, cscan)
    flaws: list[Flaw] = NDTKitDefectDetectionInterface.get_all_defects(cscan)
    for flaw in flaws:
        flaw.set_comment("Detected with Python API")
        NDTKitDefectDetectionInterface.change_defect_value(cscan, flaw, NIEnumDefectCharacteristics.NOTE, "threshold = " + str(defect_threshold))
