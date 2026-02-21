from robofest.classes.limit_class import Limits

class Scene:
    def __init__(self, func: callable, *args):
        self.func = func
        self.args = args
    
    def play(self):
        self.func(*self.args)

class Act:
    def __init__(self, scenes: list[Scene]):
        self.scenes = scenes

class Script:

    acts = {}
    playing_act = 0

    def camera_check():
        pass

    def alignment():
        pass
    def move_wheels():
        pass
    def rotate_wheels():
        pass

    def move_arm():
        pass

    def next_act():
        pass

