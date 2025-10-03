from manim import *

class Test(Scene):
    def construct(self):
        self.add(Tex("Hello, LaTeX!"))
        self.wait()

