from common import Coords, Face


def displayFaceDetails(obj):
    print("------------------------")
    for j, face in enumerate(obj.faces[Face.INDICES]):
        print(f"-----Face {j+1}-----")
        print(f"Normal: {obj.faces[Face.NORMAL][j]}")
        print(f"Visible: {obj.faces[Face.VISIBLE][j]}")
        print(f"Intensity: {obj.faces[Face.LIGHT_INTENSITY][j]}")
        for i, vertex_index in enumerate(obj.faces[Face.INDICES][j]):
            print(f"Vertex {chr(ord('A')+vertex_index)}")
            print(
                f"\tWorld Coords: {obj.vertices[Coords.WORLD][vertex_index]}")
            print(
                f"\tCamera Coords: {obj.vertices[Coords.CAMERA][vertex_index]}")
            print(
                f"\tNormalized Coords: {obj.vertices[Coords.NORMALIZED][vertex_index]}")
    print("------------------------")
