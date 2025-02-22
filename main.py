import pyxel

# Initialize Pyxel with a window size (example: 160x120)
pyxel.init(160, 120)

# Print "Hello World!" to the Pyxel screen using text
pyxel.text(50, 60, "Hello World!", pyxel.COLOR_WHITE)

# Run the Pyxel game loop
pyxel.run(lambda: None, lambda: None)
