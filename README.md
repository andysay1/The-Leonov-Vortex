# The Leonov Vortex

An elegant mathematical formula for creating a saturated spiral vortex, visualized with the Manim animation engine. This project explores the properties of the vortex and provides animations explaining its behavior.

![Demo Animation](leonov-vortex-demo.gif)
*(To add this animation, upload the GIF to the repository and make sure the filename matches)*

---

### The Formula

The vortex is defined in polar coordinates `(r, θ)` by the vector function:

$$
\mathbf{v}(r, \theta) = \text{polar\_vec}\big(p_1 \cdot \tanh(r), \; p_0 + \theta\big)
$$

Where:
- **`p1`**: A parameter controlling the maximum magnitude (strength) of the vortex.
- **`p0`**: A parameter controlling the "twist" or spiral angle.
- **`tanh(r)`**: The hyperbolic tangent function, which ensures the vortex strength saturates at large distances from the center, creating a stable and well-behaved field.

### Code Files

- `test_formula.py`: A Python script with unit tests to verify the mathematical properties of the formula.

### How to Run

1.  Make sure you have Manim Community and its dependencies installed.
    ```bash
    pip install manim
    ```
2.  To render an animation, run:
    ```bash
    manim -pqh <filename.py> <SceneName>
    ```
    For example:
    ```bash
    manim -pql explain_vortex.py ExplainVortex
    ```

### License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

*Made by ANDREI LEONOV*
