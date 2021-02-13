from enum import Enum
import numpy as np

class Coords(Enum):
    WORLD = 1
    CAMERA = 2
    NORMALIZED = 3


class Models(Enum):
    cat01 = 1
    gorilla05 = 2
    michael18 = 3
    wolf02 = 4
    triangle = 5

class Face(Enum):
    INDICES = 1
    NORMAL = 2
    VISIBLE = 3

class FileDetails(Enum):
    FILE_PATH = 1
    CAMERA_POS = 2
    LIGHT_SOURCE_POS = 3


MODEL_DETAILS = {
    Models.cat01: {
        FileDetails.FILE_PATH: 'PA2_Models/cat01.off',
        FileDetails.CAMERA_POS: np.array([-50, -60, 10]),
        FileDetails.LIGHT_SOURCE_POS: np.array([-50, -60, 160])
    },
    Models.gorilla05: {
        FileDetails.FILE_PATH: 'PA2_Models/gorilla05.off',
        FileDetails.CAMERA_POS: np.array([-70, 30, 60]),
        FileDetails.LIGHT_SOURCE_POS: np.array([-70, 30, 60])
    },
    Models.michael18: {
        FileDetails.FILE_PATH: 'PA2_Models/michael18.off',
        FileDetails.CAMERA_POS: np.array([-60, -120, 10]),
        FileDetails.LIGHT_SOURCE_POS: np.array([-60, -120, 80])
    },
    Models.wolf02: {
        FileDetails.FILE_PATH: 'PA2_Models/wolf02.off',
        FileDetails.CAMERA_POS: np.array([-60, -120, 10]),
        FileDetails.LIGHT_SOURCE_POS: np.array([-60, -120, 100])
    },
    Models.triangle: {
        FileDetails.FILE_PATH: 'PA2_Models/triangle.off',
        FileDetails.CAMERA_POS: np.array([-1, 0, 0]),
        FileDetails.LIGHT_SOURCE_POS: np.array([1, 0, 0])
    },
}
