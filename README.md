# 3×3×3 Puzzle Cube Solver
A Python backtracking algorithm that finds all unique solutions to a 3×3×3 puzzle cube using 3D rotation generation, collision detection, recursive search, and symmetry reduction.

## How it Works
- Takes user inputs for each piece and defines them in 3×3×3 numpy arrays
- Generates all unique rotations of every piece
- Attempts every possible unique combination of pieces using backtracking
- Prunes based on colisions and bounds violations
- Normalizes cube rotations to remove duplicate solutions

### Example output of two solutions to a puzzle cube:
<img width="168" height="418" alt="image" src="https://github.com/user-attachments/assets/cc549f62-af43-486c-9826-3cd513c5490b" />

### Example input for an L-shaped piece:
<img width="1716" height="656" alt="Screenshot 2026-05-25 184110" src="https://github.com/user-attachments/assets/abb9e8a8-e6ea-406a-9952-24c39e8be4d5" />
