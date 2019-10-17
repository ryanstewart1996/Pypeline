# Pypeline
Pipeline outflow analysis tool and fluid mechanics library
This collections of python scripts measures the number of barrels of fluid that could potentially
be spilled at different points along a pipeline.

To calculate the potential spill at a location along the pipe,
Bernoulli’s equation is used. The velocity of the outflow is dependent
on the elevation difference between the location of the spill and the
max elevation points of the pipeline. Since we have one equation with
two unknowns, we reiterate the calculation as time increases.
As time passes, the elevation difference will change, resulting in a new velocity.
This is iterated until the time elapsed equals the time it takes for the valves to shut off.


Future opportunities to further develop this program include:
• Creating a Microsoft Excel add-on to make it easier for non-programmers to interface with the analysis tool
• Re-writing the software in a faster programming language (C, C++, etc.)
• Create a Raspberry Pi cluster to better maximize the speed of rendering
for very long segments of pipe (200km-500km) or use CUDA for faster rendering times
• Apply the fluid mechanic functions created during development of this software to other fluid applications and problems

