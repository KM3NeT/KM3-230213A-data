# KM3NeT Event Display of the UHE Event

## Installation

Be aware that running the display requires a local installation that will take a few minutes.

### Installing Julia

The [`RainbowAlga`](https://git.km3net.de/tgal/RainbowAlga.jl) event display is
written in Julia, therefore Julia needs to be present on the system.
The following command will install [Julia](https://julialang.org) and the command
line tool [`juliaup`](https://github.com/JuliaLang/juliaup) (to manage Julia versions)
on a Linux or macOS machine:

    curl -fsSL https://install.julialang.org | sh

On windows, Julia can be installed directly from the
[Windows store](https://www.microsoft.com/store/apps/9NJNWW8PVKMN) or using `winget`:

    winget install julia -s msstore

### Adding the KM3NeT Julia Registry

If Julia was never used before, the general Julia registry needs to be initialised
before adding additional package registries

    julia -e 'using Pkg; Pkg.Registry.add()'

The KM3NeT Julia registry can now be added with

    git clone https://git.km3net.de/common/julia-registry.git ~/.julia/registries/KM3NeT

### Instantiating the envrionment

Make sure you are inside "this" directory:

    cd event-display

To instantiate the project with all the required dependencies, run

    julia --project=. -e 'using Pkg; Pkg.instantiate()'

## Launching the RainbowAlga GUI

After following the installation steps, run the following command from within
this directory:

    julia --project=. uhe_event_gui.jl

## Keybindings

You can use <kbd>&larr;</kbd> and <kbd>&rarr;</kbd> to go back and forth in time and <kbd>R</kbd> to reset the time.

| Key               | Command                   |
|-------------------|---------------------------|
| <kbd>&larr;</kbd> | Time step back            |
| <kbd>&rarr;</kbd> | Time step forward         |
| <kbd>&uarr;</kbd> | Faster                    |
| <kbd>&darr;</kbd> | Slower                    |
| <kbd>,</kbd>      | Decrease ToT cut          |
| <kbd>.</kbd>      | Increase ToT cut          |
| <kbd>R</kbd>      | Reset time to 0           |
| <kbd>A</kbd>      | Toggle auto-rotation      |
| <kbd>L</kbd>      | Toggle loop               |
| <kbd>D</kbd>      | Toggle dark mode          |
| <kbd>C</kbd>      | Cycle between hit clouds  |
| <kbd>1</kbd> - <kbd>9</kbd>      | Load perspective |
| <kbd>Shift</kbd><kbd>1</kbd> - <kbd>9</kbd>      | Save perspective |
| <kbd>Space</kbd>  | Play/Pause                |
| <kbd>Q</kbd>      | Quit                      |

Perspectives 1, 2 and 3 are the ones shown in Figure 1 of the original Nature paper.
