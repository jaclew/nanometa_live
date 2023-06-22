# Nanometa Live
Short introduction. Pictures here.

For more information, see the [wiki](https://github.com/FOI-Bioinformatics/nanometa_live/wiki).

## INSTALL
The program uses a conda environment, so conda or mamba will need to be installed for it to work. Mambaforge is recommended.

**Install with conda**

Conda installation instructions...

**Install from source**

&emsp;&emsp;**1.** Clone or download the files from GitHub, for example:

&emsp;&emsp;&emsp;&emsp;*$ git clone https://github.com/FOI-Bioinformatics/nanometa_live*

&emsp;&emsp;**2.** From the main folder, containing **nanometa_live_env.yml**, create a conda/mamba environment from the yml file, for example:

&emsp;&emsp;&emsp;&emsp;*$ mamba env create -f nanometa_live_env.yml*

&emsp;&emsp;**3.** Activate the environment:

&emsp;&emsp;&emsp;&emsp;*$ conda activate nanometa_live_env*

&emsp;&emsp;**4.** Install the program in the environment. While standing in the directory containing **setup.py**:

&emsp;&emsp;&emsp;&emsp;*$ pip install .*

The program is now installed and can be accessed from any directory using the instructions below.

## QUICK USE TUTORIAL
The tutorial files can be downloaded at https://drive.google.com/drive/folders/1fjAihcPw409Pw8C3z_YPQnBnRMuoDE4u?usp=sharing. We will use the built-in nanopore simulator to do a test run using a GTDB database for Kraken2.

#### 1. Make sure the environment is activated:
&emsp;&emsp;*$ conda activate nanometa_live_env*

#### 2. Create a new project
&emsp;&emsp;*$ nanometa-new --path /home/user/metagenomic_project*

#### 3. Modify the config file
Go into the newly created directory and open the config file.  

Change the **Nanopore output directory** */home/user/nanopore_out* to your user name (or other desired path).

Set the **Kraken 2 database** directory to wherever you put your database from the tutorial files, for example */home/user/kraken2.gtdb_bac120_4Gb*. Naturally you need to unpack it. 

Remember to save your config file after modification.

#### 4. Build BLAST databases for validation
The *nanometa-blastdb* command constructs the needed files for validating the sequences that Kraken 2 finds.

The example refseqs from the tutorial files should be placed in a directory, for example */home/user/example_refseqs*. This directory should contain the following files: "321.fasta", "852.fasta", "5061.fasta", "13373.fasta".

Standing in your project directory (*/home/user/metagenomic_project*), run the command with the example_refseqs directory in as input:

&emsp;&emsp;*$ nanometa-blastdb -i /home/user/example_refseqs*

The folder *blast_databases* should be created in your project directory, containing 8 database files for each ID, with different endings: "idnumber.fasta.xxx".

#### 5. Start Nanopore sequencing
For the tutorial, we will use the Nanopore simulator that comes with the program. Put the 8 tutorial test batch files, ending in fastq.gz, in a folder called */home/user/nanometa_test_data*, and from a separate terminal run:

&emsp;&emsp;*$ nanometa-sim -i /home/user/nanometa_test_data -o /home/user/nanopore_out*

The -o folder is the simulated Nanopore output, and needs to be the same as specified in the config under **Nanopore output directory**. The simulator automatically copies a file from the nanometa_test_data directory every 1-2 minutes until all the files are copied, to mimic the Nanopore batches. 

#### 6. Start the backend
Start a separate terminal, make sure you are in the project directory */home/user/metagenomic_project* and run:

&emsp;&emsp;*$ nanometa-pipe*

To exit the pipeline, press *ctrl+C*. Might have to be pressed several times.

#### 7. Start the GUI
Start a separate terminal, make sure you are in the project directory and run:

&emsp;&emsp;*$ nanometa*

Hold *ctrl* and click the port link if the GUI does not open by itself.

To exit the GUI, press *ctrl+C* in this terminal. The browser window can be closed as a regular window.

#### 8. Navigating the GUI

There are tooltips in the GUI for most of the settings. Hover over an object to display the tooltips. There are thorough descriptions of the plots in the [wiki](https://github.com/FOI-Bioinformatics/nanometa_live/wiki). 

The tutorial species of interest have been chosen to display all the possible abundance visualizations in the GUI:

&emsp;**ID 5061** - *Clostridium_H novyi* - **0 reads** in test data - corresponding NCBI taxID: 386415 - refseq accession: GCF_000014125.1

&emsp;**ID 13373** - *Faecalibacterium prausnitzii_M* - **3 reads** in test data - corresponding NCBI taxID: 853 - refseq accession: GCF_000154385.1

&emsp;**ID 852** - *Bacteroides fragilis_A* - **48 reads** in test data - corresponding NCBI taxID: 817 - refseq accession: GCF_002849695.1

&emsp;**ID 321** - *Bifidobacterium adolescentis* - **552 reads** in test data - corresponding NCBI taxID: 367928 - refseq accession: GCF_000010425.1

With the default settings, species with a read count higher than 10 will appear as yellow, and species with a read count higher than 100 will appear as red.


## Contact and community guidelines
Contact regarding Nanometa Live: Kristoffer, **kristoffersandas@yahoo.se**

For problems, comments or support, post an issue. 
