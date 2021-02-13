class Scene:
    def __init__(self, camera_pos, camera_direction, light_source_pos):
        self.camera_pos = camera_pos
        self.camera_direction = camera_direction
        self.light_source_pos = light_source_pos
        self.object = None
    
    def add_object(self, obj):
        self.object = obj

    def simulate_model(self):
        self.object.get_camera_coords(self.camera_pos)
        self.object.get_face_normals()
        self.object.get_view_frustum(self.camera_pos)
        self.object.get_normalized_coords()
        self.object.backface_detection(self.camera_direction)
