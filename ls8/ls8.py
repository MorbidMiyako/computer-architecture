#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

print8 = "examples/print8.ls8"
mult = "examples/mult.ls8"


cpu = CPU()

cpu.load(mult)
cpu.run()
