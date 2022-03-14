# TeXlinter_Source_code
The source code for TeXlinter

**!!Exclaimer!!**

## If you want to make an executable for Windows/Linux and or macOS X on your own follow the instructions bellow
### Make sure you have python3 installed to follow these instructions

pip install auto-py-to-exe

## Then to run it, execute the following in the terminal:
auto-py-to-exe

## This will bring up the following window
![bild](https://user-images.githubusercontent.com/99668019/158139599-f088a51e-0aec-4a39-bfd2-a7a72f8279ac.png)

First you need to add the script.\
Chose One Directory, Console Based\
Under Settings, you can chose where you want the output folder to be located\
Then just hit the Convert py to .exe button and you will be done

## If you want to use the linter from anywhere outside the executable folder you just created follow the instructions bellow
## On Linux and macOS X
export PATH="$Path-to-the-linter-folder:$PATH"

## On Windows
1. Start cmd as administrator
2. setx /M PATH "%PATH%;your-new-path-to-TeXlinter-folder"


## How to use the TeXlinter

## On Windows
TeXlinter.exe "your LaTex document"
## If you have your own rules
TeXlinter.exe "your LaTex document" --rules <your own rule .json or .yaml>
## If you want to see what have changed
TeXlinter.exe "your LaTex document" --header
## If you need a reminder
TeXlinter.exe help

## If you want to run a test and see what the linter changes
## Run the following
TeXlinter.exe --header "path to TeXlinter folder/test.tex"
  
## On Linux/macOS X
TeXlinter <”your LaTex document”>
## If you have your own rules
TeXlinter <”your LaTex document”> –rules <”your own rule .json or .yaml”>
## If you want to see what changes have happend
TeXlinter <”your LaTex document”> –header
## If you want to get help how to run the application
TeXlinter -h
## If you want to run a test too see how the application runs and do
TeXlinter <”path to where you have installed pipx/test.tex”> –header
