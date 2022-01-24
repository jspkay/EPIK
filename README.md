# EPIK
The solution is E.P.I.K., the Education Programmable Improving Kit. Its goal is to provide technical school professors with tools to make the laboratory
activities more engaging. This is achieved by giving the students a gaol, e.g. the students will allow E.P.I.K. to move and talk, and to do so they will 
have to use the concepts learnt in the classroom. The activities that E.P.I.K. provides are aligned with the technical school curricula, allowing the teacher 
to effectively integrate our solution in the educational path of the students. The kit will be composed of common hardware components and of a software, the 
latter of which provides both an interface to easily program E.P.I.K. and a guide to organise and perform the experiences. The kit also delivers a plastic case 
which will serve as lodging for the hardware components, and comes in a box.

# Dependences
The software is written in python (version 3). It is necessary to install the following packages:
- asyncio
- netifaces 
- subprocess
- tkinter
- json
- os
- threading
- time


# Usage
The software is split in two parts.

1. The server side goes directly on the Raspberry Pi. To start the software simply go to the server directory and type:
```python
python3 ERIS.py
```
> Note: ERIS is the old name, recently replaced by EPIK.

2. The client side goes on the laboratory computer. To start that server it's possibile to type:
```python
python3 main.py
```
