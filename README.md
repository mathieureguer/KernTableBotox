# Kern Table Botox
Mathieu Reguer


## Installation

The following external package are required: `fonttools`, `click`. 
This required package will be intalled automatically with the following instalation process:

Just press `enter` in the terminal after each of the commands below to launch them.

1. `pip` is a handy tool to easily install python packages. 
    You propbably already have it, you can just skip to step 2. Come back here if it does not work.
    If you do not have it, run the following command (you will be asked for your pasword):
    ``` bash
    sudo easy_install pip
    ```


2. Copy the whole `KernTableBotox` folder to a chosen location on your computer. 

3. In the Terminal `cd` to this location. Just type `cd `, add a space, and drag and drop the folder in the Terminal window. It should look like this. Press enter.
    ``` bash
    cd path/to/KernTableBotox/
    ```

4. Then run the following command
    ``` bash
    sudo -H pip install .
    ```
    `sudo` runs the command with admin priviledge, you will be asked your password. The password will be invisible.

5. Done! If everything worked, you should be abble to run the following command in the terminal:
    ``` bash
    KernTableBotox --help
    ```

6. To update the tool, just copy the updated package to your computer, `cd` to its location and run the following command (`-U` is for update):
    ``` bash
    sudo -H pip install -U .
    ```
    
Once the tools are intalled, their name can be autocompleted in the Terminal window by pressing the `tab` key.

- Typing `KernT` then `tab` file automatically complete to `KernTableBotox`

## Usage

### KernTableBotox

KernTableBotox is a command line tool to inject an old school `flat` kern table into compiled fonts. 
It will parse the modern OpenType Kerning data, flatten all the pairs and inject them in a `kern` table. This is mostly useful for PowerPoint kerning support. Yay.
The number of pairs should not matters, KernTableBotox will create the required subtables. The more pairs you have the bigger the font will get though.


``` bash
KernTableBotox path/to/my/font.otf
```

It works on both font files and folder. If you feed it a path to a folder instead of a font file, it will run for every otf in that folder

``` bash
KernTableBotox path/to/my/folder
```

The fonts are saved in the same folder, with the `_kerntable` suffix unless an output directory is specified (see below)

##### output option

The `-o` (or `--output_dir`) option can be used to specify a name for the output directory.

``` bash
KernTableBotox path/to/my/folder -o myOutputFolder
```

The `-t` (or `--suffix_tag`) option can be used to specify another suffix for the font files.

``` bash
KernTableBotox path/to/my/folder -t my_cool_suffix myOutputFolder
```

The `--no_suffix` option can be used to prevent the use of a suffix. The font will be saved in place (if `-o` is not set to another directory).

``` bash
KernTableBotox path/to/my/folder --no_suffix my_cool_suffix myOutputFolder
```








