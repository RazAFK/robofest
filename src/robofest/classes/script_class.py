from robofest.classes.limit_class import Limits

def camera_check(Camera):
    pass

def alignment():
    pass
def move_wheels():
    pass
def rotate_wheels():
    pass

def move_arm():
    pass

class Scene:
    def __init__(self, func: callable, *args):
        self.func = func
        self.args = args
    
    def play(self):
        self.func(*self.args)

class Act:
    def __init__(self, scenes: list[Scene]):
        self.scenes = scenes
    
    def play(self):
        for scene in self.scenes:
            scene.play()

class Intermission:

    def noplay(self):
        pass

class Script:

    acts = {}
    playing_act = 0
    hand_cam = None
    wheel_cam = None
    arduino = None
    reader = None
    special = (None, None)

    def __init__(self, acts: list[Act | Intermission]):
        self.acts = acts

    def add_workers(self, hand_cam, wheel_cam, arduino, reader):
        self.hand_cam = hand_cam
        self.wheel_cam = wheel_cam
        self.arduino = arduino
        self.reader = reader

    def next_act():
        pass