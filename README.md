# Teresa

Basic Sudoku solver in Python. Uses multiple strategies to generate consequences of given or asserted values. Inspired by tree-searching algorithms.
Named in honor of my friend's grandmother.

## Usage

1. Run by starting `main.py`
2. Enter the sudoku, in empty places write ` ` or `-`; at the end of every line just press enter
   For example:
   ![An example image](/example.PNG)
   should be represented as:

   ```
   42-3--7--
   986-1-3--
   3----5---
   -9----1--
   73-----68
   --8----5-
   ---1----7
   --3-2-541
   --4--3-89
   ```
   
3. Wait.

## Implemented rules

- [x] Naked single
- [x] Hidden single
