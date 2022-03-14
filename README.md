# TeXlinter_Source_code
The source code for TeXlinter

## If you want to make an executable for Windows/Linux and or macOS X on your own follow the instructions bellow
### Make sure you have python3 installed to follow these instructions

## Linux and maCOS X
1. git clone https://github.com/brentvollebregt/auto-py-to-exe.git
2. cd auto-py-to-exe
3. python3 setup.py install


## Windows
pip install auto-py-to-exe

# Then to run it, execute the following in the terminal:
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
