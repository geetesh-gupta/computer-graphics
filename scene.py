class Scene:
    def __init__(self, camera_pos, camera_direction, light_source_pos, viewport):
        self.camera_pos = camera_pos
        self.camera_direction = camera_direction
        self.light_source_pos = light_source_pos
        self.object = None
        self.viewport = viewport

    def add_object(self, obj):
        self.object = obj

    def simulate_model(self):
        self.object.get_camera_coords(self.camera_pos)
        self.object.get_face_normals()
        self.object.get_view_frustum(self.camera_pos)
        self.object.get_normalized_coords()
        self.object.backface_detection(self.camera_direction)
        self.object.apply_phong_shading(
            self.camera_direction, self.light_source_pos)
        self.object.window_viewport_transformation(self.viewport)
