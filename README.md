# primula: A Simple Circuit Simulator


## Why??
I dunno. Just for fun? And to improve my knowledge about digital circuits and
simulation?

## What?
It implements basic components which have multiple pins, wires to connect them,
and a simulator. Whenever a wire is connected anywhere, the simulation is
updated.  Any signal changes will automatically propagate around the circuit
until a fix-point is reached.

I think that means that oscillating or metastable circuits are not permitted.
But it was a while ago since I wrote the code so maybe that isn't true?

## Where?
Various classic circuits (latches and flip-flops) are implemented in the
test-suite, and their properties are tested to make sure the simulated circuits
behave as expected.

There are also prefabricated components for various latches and flip flops
which are for convenience and performance.

Eventually it would be nice to have components like n-bit busses, multiplexers,
memories, and all the rest of it.
