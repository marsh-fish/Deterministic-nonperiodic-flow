from manim import *
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


class LorenzAttractor(ThreeDScene):
    def construct(self):
        # Set up 3D axes
        axes = ThreeDAxes(
            x_range=[-50, 50, 10],
            y_range=[-50, 50, 10],
            z_range=[0, 50, 10],
        )
        self.set_camera_orientation(phi=75 * DEGREES, theta=45 * DEGREES)

        self.add(axes)

        # Add the equations
        equations = MathTex(
            r"""
            \frac{\mathrm{d} x}{\mathrm{~d} t} = \sigma(y-x) \\
            \frac{\mathrm{d} y}{\mathrm{~d} t} = x(\rho-z)-y \\
            \frac{\mathrm{d} z}{\mathrm{~d} t} = x y-\beta z
            """,
            font_size=36
        )
        equations.to_corner(UL)
        self.add_fixed_in_frame_mobjects(equations)
        self.play(Write(equations))

        # Compute solutions
        epsilon = 1e-5
        evolution_time = 30
        n_points = 10
        states = [
            [10, 10, 10 + n * epsilon]
            for n in range(n_points)
        ]
        colors = color_gradient([BLUE_E, BLUE_A], len(states))

        curves = VGroup()
        for state, color in zip(states, colors):
            points = ode_solution_points(lorenz_system, state, evolution_time)
            curve = VMobject().set_points_as_corners([axes.c2p(*p) for p in points])
            curve.set_color(color)
            curve.set_opacity(0.6)
            curves.add(curve)

        self.play(Create(curves), run_time=5)

        # Add moving dots
        dots = VGroup(*[Sphere(radius=0.2).set_color(color) for color in colors])
        for dot, curve in zip(dots, curves):
            dot.move_to(curve.get_start())

        self.add(dots)

        # Track time with a custom updater
        time_tracker = ValueTracker(0)

        def update_dots(mob):
            for i, dot in enumerate(mob):
                curve = curves[i]
                # Calculate the proportional position along the curve
                dot.move_to(curve.get_end())

        dots.add_updater(update_dots)

        # Animate the time tracker and dots
        self.play(
            time_tracker.animate.set_value(evolution_time),
            run_time=evolution_time,
            rate_func=linear
        )
        self.wait()
