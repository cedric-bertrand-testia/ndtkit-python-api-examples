from ndtkit_api import NDTKitCScanInterface, NDTKitDefectDetectionInterface
from ndtkit_api.model.NIEnumSpecialValue import NIEnumSpecialValue
from ndtkit_api.model.NIEnumDefectShapeType import NIEnumDefectShapeType
from ndtkit_api.model.flaw.NIEnumDefectCharacteristics import NIEnumDefectCharacteristics

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
    defects_matrix = [[False for _ in range(len(data[0]))] for _ in range(len(data))]
    for row in range(len(data)):
        for col in range(len(data[0])):
            value = data[row][col]
            defects_matrix[row][col] = not NIEnumSpecialValue.is_special_value(value) and value > defect_threshold
    flaws = NDTKitDefectDetectionInterface.apply_defects_from_matrix(defects_matrix, cscan, NIEnumDefectShapeType.RECTANGLE_FITTING)
    for flaw in flaws:
        flaw.set_comment("Detected with Python API")
        NDTKitDefectDetectionInterface.change_defect_value(cscan, flaw, NIEnumDefectCharacteristics.NOTE, "threshold = " + str(defect_threshold))
