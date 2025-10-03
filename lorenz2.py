from manimlib import *
import numpy as np
from scipy.integrate import solve_ivp


def lorenz_system(t, state, sigma=10, rho=28, beta=8 / 3):
    x, y, z = state
    dxdt = sigma * (y - x)
    dydt = x * (rho - z) - y
    dzdt = x * y - beta * z
    return [dxdt, dydt, dzdt]


def ode_solution_points(function, state0, time, dt=0.01):
    solution = solve_ivp(
        function,
        t_span=(0, time),
        y0=state0,
        t_eval=np.arange(0, time, dt)
    )
    return solution.y.T


def for_later():
    tail = VGroup(
        TracingTail(dot, time_traced=3).match_color(dot)
        for dot in dots
    )


class LorenzAttractor(InteractiveScene):
    def construct(self):
        images = [
            ImageMobject("5.jpg"),
            ImageMobject("yoje.jpg")
        ]
        # images.move_to(axes.c2p(0, 0, 0))()
        images[0].to_edge(LEFT)
        self.add(images[0])
        images[1].to_edge(RIGHT)
        self.add(images[1])
        self.wait(3)

        # Set up axes
        axes = ThreeDAxes(
            x_range=(-50, 50, 5),
            y_range=(-50, 50, 5),
            z_range=(-0, 50, 5),
            width=16,
            height=16,
            depth=8,
        )
        axes.set_width(FRAME_WIDTH)
        axes.center()

        # self.frame.reorient(43, 76, 1, IN, 10)
        # self.frame.add_updater(lambda m, dt: m.increment_theta(dt * 3 * DEGREES))
        self.add(axes)
        
        # Compute a set of solutions
        epsilon = 1e-5
        evolution_time = 30
        n_points = 2
        states = [
            [10, 10, 10 + n * epsilon]
            for n in range(n_points)
        ]
        colors = color_gradient([BLUE_E, BLUE_A], len(states))

        curves = VGroup()
        for state, color in zip(states, colors):
            points = ode_solution_points(lorenz_system, state, evolution_time)
            curve = VMobject().set_points_smoothly(axes.c2p(*points.T))
            curve.set_stroke(color, 1, opacity=0.25)
            curves.add(curve)

        curves.set_stroke(width=2, opacity=1)

        # Display dots moving along those trajectories
        dots = Group(GlowDot(color=color, radius=0) for color in colors)
        def update_dots(dots, curves=curves):
            for dot, curve in zip(dots, curves):
                dot.move_to(curve.get_end())

        dots.add_updater(update_dots)
        
        tail = VGroup(
            TracingTail(dot, time_traced=3).match_color(dot)
            for dot in dots
        )

        self.add(dots)
        self.add(tail)
        
        for img in images:
            self.add(img)
        for img, curve in zip(images, curves):
            target_image = img.copy().scale(0.3)
            target_image.move_to(curve.get_start())
            self.play(Transform(img, target_image), run_time=1)
            
        # Define an updater for images
        def update_images(images):
            for img, curve in zip(images, curves):
                img.move_to(curve.get_end())
                
        for img in images:
            img.add_updater(lambda m, images=images: update_images(images))
        curves.set_opacity(0)
        self.play(
            *(
                ShowCreation(curve, rate_func=linear)
                for curve in curves
            ),
            run_time=evolution_time*2,
        )

