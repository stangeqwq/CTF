# APARTMENT
This CTF challenge is basically a logic test using logic gates.

## The Challenge
It’s a cold day, and the snow is falling horizontally. It pierces your sight. You better use those extra pairs of socks that you were strangely given by the driver. Someone is waving on the other side of the street. You walk over to her. “Hi AGENT, I’m AGENT X, we’ve found the apartment of a person that we suspect got something to do with the mission. Come along!.”
It turned out suspect’s appartment has an electronic lock. After analyzing the PCB and looking up the chips you come to the conclusion that it’s just a set of logic gates!

## The Solution
We look at the given logic gates image.

![logic gates](logic-lock.png)

The gates used in the image are `AND`, `NOR`, `XOR`, and `NOT` gates. Working backwards from the right where the value is `1` or `set`. We find that the following letters should be `set` to bypass this logic-lock: `BCFIJ`. The flag is `CTF{BCFIJ}`.
