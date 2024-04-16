# ump-analysis
Using statcast data via [pybaseball](https://github.com/jldbc/pybaseball) to analyze umpire's calls.
 
## Overview
The data used for this analysis comes from [pybaseball's](https://github.com/jldbc/pybaseball) statcast data. Data is pulled from pybaseball, then filtered to only include decisions that the home plate umpire makes when it comes to pitches: balls and called strikes. Determining the correctness of a call is done in pretty much the same way [@UmpScorecards](https://umpscorecards.com/home/) does their analysis. There are 5 variables from the statcast data that are used:
* `plate_x` - the horizontal position of the ball as it crosses the plate. Measured in feet from the ground.
* `plate_z` - the vertical position of the ball as it crosses the plate. Measured in feet from the ground.
* `sz_top` - the top of the strike zone set by the operator. Measured in feet from the ground.
* `sz_bot` - the bottom of the strike zone set by the operator. Measured in feet from the ground.
* `type` - the call (ball or strike) made by the umpire.
 
Put simply, if a ball is called on a pitch that arrives within the strike zone set by the operator, an incorrect call was made. The same is true vice versa. This is is simply added as an indicator variable in a new column that is added to the end of the data, `correct_call`. A value of `1` indicates the correct call was made, while a value of `0` indicates an incorrect call was made.

## Dependencies
* pandas
* scikit-learn
* matplotlib
* seaborn

## Retrosheet
     The information used here was obtained free of
     charge from and is copyrighted by Retrosheet.  Interested
     parties may contact Retrosheet at "www.retrosheet.org".
Retrosheet data is gathered from the [chadwickbureau/retrosheet](https://github.com/chadwickbureau/retrosheet) repository through [pybaseball](https://github.com/jldbc/pybaseball).

For user security, **this repository does not provide the .exe files needed to parse this data**. The user must source these executables on their own to work with retrosheet data. There are executables provided by RetroshBeet at [https://www.retrosheet.org/tools.htm](); use these files at your own risk. The ump-analyis repository utilizes `BEVENTS.EXE` and `BGAME.EXE`. Place the unziped executable(s) in the `./ump-analyis/retrosheet` directory.

## Todos/Goals
 - [ ] figure out how to match Retrosheet game data with statcast data
 - [ ] match data to specific umpires, have options for outputs based on missed call frequency, who had the worst calls, etc.
 - [x] implement data visualization with graphs or heatmaps
 - [ ] make it operable from the terminal
 - [ ] add progress bars ([tqdm](https://github.com/tqdm/tqdm)?)
 - [ ] create a GUI