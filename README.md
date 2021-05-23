# now.py
### View your computer stats in a terminal
Designed to be kept open, in the corner of your screen for easy access. Resizes to fit the size of your terminal

## Usage
Just run `python now.py` - You will be asked to install any missing imports

On windows, you will be asked a question to check that ANSI colour codes work - Just enter `y` or `n`

## Descriptions
### TIME
The time and date
> Hours:Minutes:seconds
> Year-Month-Day

### PROC
Processes
> The number of currently running processes
> The lowest number of processes that have been running
> The highest number of processes that have been running

### CPU
CPU
> The percentage of the CPU that is being used
> The number of cores on your CPU
> The frequency of your CPU
> 
> If your CPU is > 80%, the most CPU intensive process will be shown, the amount of CPU it is using, and the CPU bar wil flash

### MEM
Memory / RAM
> The amount in use (%)
> The amount in use (size)
> The total RAM on your computer (size)
>
> If your RAM is > 80%, the most RAM used by a process will be shown, the amount of RAM it is using, and the MEM bar wil flash

### SWAP
Swap space
> The amount in use (%)
> The amount in use (size)
> The total swap on your computer (size)

> If swap is above 80%, the SWAP bar will flash

### DISK
Drive space
> The amount used (%) on the / or C:\ drive
> The number of devices mounted
> A list of all mounted devices (/ on Linux, C:\ on Windows etc.)

### TEMP
Temperature
*Windows does not support temperature sensors*
> The temperature of each sensor on your computer
>
> If your temperature is above 75°c, the TEMP bar will flash
>
> If you are American, you can use °F by editing changing `useFahrenheit` (Line 7) to True
>
> Special names:
> 
> Name           | Displayed
> ---------------|----------
> acpitz         | Sockets
> pch_cannonlake | PCH
> coretemp       | Cores
> iwlwifi_1      | WIFI
> 
> `coretemp`  / `Cores` is always sorted shown before all others
>
