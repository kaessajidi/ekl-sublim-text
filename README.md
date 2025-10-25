# EKL Syntax for Sublime Text

This package adds EKL highlighting for Sublime Text.

## Files covered
- `*.ekl`
- `*.CATRule`
- `*.CAT*`

## Installation
1. Copy the two files into your Sublime Text Packages directory:
   - `EKL.sublime-syntax`
   - `README.md` (optional)

   Typical locations:
   - Windows: `%APPDATA%\Sublime Text\Packages\EKL/`
   - Portable: `Sublime Text\Data\Packages\EKL/`

2. Restart Sublime Text (or Preferences → Package Control → Satisfy Dependencies if prompted).

3. Open an EKL file and set the syntax to EKL if not auto-detected (bottom-right status bar → Plain Text → EKL).

## Features
- EKL keywords: `let`, `set`, `function`, `returns`, `for`, `while`, `if`, `else`, `return`, `include`, `exit`, `exitfunction`
- EKL types: `VPMReference`, `AdvisorParameterSet`, `DTSheetType`, `List`, `String`, `Integer`, `Real`, `Boolean`, `Map`, `HTTPClient`, `DataTreeNode`, `KWETuple`, `ValuePointer`, plus `Hole`, `Surface`, `Curve`, `Line`, `Point`, `Plane`, `Body`
- Constants: `TRUE`, `FALSE`, `NULL`
- Operators: `::`, `->`, `==`, `<>`, `<=`, `>=`, `<`, `>`, `=`, `+`, `-`, `*`, `/`, `%`, `&`, `|`, `!`, `^`, `~`
- Units like `5 mm`, `10deg`, `2.5 s`
- Parameter paths like `PartBody\Hole.1\Diameter`
- Comments `//` and `/* ... */`

## Notes
- If a file uses `.CAT*` with content not EKL, you can switch back to the appropriate syntax from the status bar.

