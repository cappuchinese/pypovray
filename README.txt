Authors: Lisa Hu and Maartje van der Hulst
Date (DD/MM/YYYY): 21/01/2022
Version: 1.0


pyPOVRAY Final assignment


Description
This directory contains the final project of creating a short film of a biological process.
For this process, the second reaction of the citric acid cycle has been visualized.
The animation shows the mechanism of citrate converting into isocitrate in its respective enzyme, aconitase.


Context
A short description of the files given:
    citrate_new.pdb				- The PDB file for the citrate molecule
    eindopdracht_LisaHu_MaartjevdHulst.py	- The Python script to create the movie
    final.mp4					- The animation of the process
    isocitrate_new.pdb				- The PDB file for the isocitrate molecule
    SLURMshelscript.sh				- A SLURM bash script to run the script over multiple workstations
    Verslag_Lisa_Hu_Maartje_vd_Hulst.pdf	- Report concluding the project


Installation
To run these scripts, first the project needs to be cloned from a git repository:
    git clone https://<user>@bitbucket.org/mkempenaar/pypovray.git
    NOTE: Change <user> to your own username or delete it if you do not have a Atlassian account.

Move to the newly cloned repository:
    cd pypovray

To check if the latest version is installed:
    git status

To retrieve the latest version:
    git pull

Download the requirements:
    sh setup.sh
    pip3 install -r requirements.txt

Unzip this folder in the ~/pypovray/ directory:
    unzip eindopdracht_LisaHu_MaartjevdHulst
    NOTE: The scripts have to be in the ~/pypovray/ directory and do not work if they are located in another directory

Overwrite the default.ini file in the pypovray library with the .ini file given.
NOTE: Change the "AppLocation" in this file to the path your local pypovray project.


Usage
To render the movie, the script must be run twice with a few minor changes.

For the first run:
    1. Open the Python eindopdracht script.
    2. Scroll down to the end of the script, where the boilerplate code is written.
    3. Uncomment the following lines:
        for i in range(1000, 1050):
            pypovray.render_scene_to_png(main, i)
    4. Comment the following line:
        pypovray.render_scene_to_png(main, int(sys.argv[1]))
    5. Run the script:
	python3 eindopdracht_LisaHu_MaartjevdHulst.py

Now frames 1000-1050 will be generated. Upon finishing this run, the following step should be followed for the second run:
    1. Comment the following lines:
         for i in range(1000, 1050):
             pypovray.render_scene_to_png(main, i)
    2. Uncomment the following line:
         pypovray.render_scene_to_png(main, int(sys.argv[1]))
    3. Open the SLURMshellscript.sh file.
    4. Change the --chdir to the directory of where the project is located.
    5. Change the -o to a directory where the slurm output can be written to.
    6. Optional: change the job name
    7. Run the following command in the terminal:
         sbatch SLURMshellscript.sh

With the command `squeue`, the progress of the slurm can be tracked. After finishing all the jobs, it is important to run this last command to form the animation:
    ffmpeg -f image2 -framerate 30 -pattern_type glob -i 'images/simulation_*.png' -c:v libx264 -r 30 -crf 2 -pix_fmt yuv420p -loglevel warning movies/final.mp4
The output will be stored as final.mp4 in the ~/pypovray/movies/ folder
DISCLAIMER: Running the movie this way might let the movie bug due to surpassing the 1000 frames. From second 4 until second ~5.5 the final scene is shown, which is the isocitrate visualization. From there on it should run as usual.

Support
If any error occurs, please contact via e-mail: l.j.b.hu@st.hanze.nl or m.van.der.hulst@st.hanze.nl


Authors and acknowledgment
This project was made available by Marcel Kempenaar, lecturer of Bioinformatics on the Hanzehogeschool Groningen, University of Applied Sciences.
The scripts for the assignments were written by Lisa Hu and Maartje van der Hulst, students of Bioinformatics.
