import time
import os
import yaml
import pkg_resources
import shutil
import argparse
import logging
import subprocess
from nanometa_live import __version__  # Import the version number

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_config(config_file):
    """
    Load configuration settings from a YAML file.

    Parameters:
        config_file (str): Path to the YAML configuration file.

    Returns:
        dict: Dictionary containing the configuration settings.
    """
    logging.info(f"Loading configuration from {config_file}")
    with open(config_file, 'r') as cf:
        return yaml.safe_load(cf)

def execute_snakemake(snakefile_path, snakemake_cores):
    """
    Execute the Snakemake workflow with the specified number of cores.

    Parameters:
        snakefile_path (str): Path to the Snakefile.
        snakemake_cores (int): Number of cores to use for Snakemake.
    """
    logging.info(f"Executing Snakemake workflow with {snakemake_cores} cores")
    log_file_path = "snakemake_output.log"  # Change this to your desired log file path
    with open(log_file_path, "a") as log_file:
        system_cmd = f"snakemake --cores {snakemake_cores} --rerun-incomplete --use-conda --snakefile {snakefile_path}"
        logging.info(f'Executing shell command: {system_cmd}')
        subprocess.run(system_cmd, shell=True, stdout=log_file, stderr=subprocess.STDOUT)

def remove_temp_files(config_contents):
    """
    Remove temporary files and directories as specified in the configuration.

    Parameters:
        config_contents (dict): Dictionary containing the configuration settings.
    """
    logging.info("Initiating cleanup of temporary files")

    # Define the paths to temporary directories and files
    kraken_results_dir = os.path.join(config_contents["main_dir"], 'kraken_results/')
    qc_dir = os.path.join(config_contents["main_dir"], 'qc_data/')
    qc_file_to_keep = os.path.join(config_contents["main_dir"], 'qc_data/cumul_qc.txt')
    validation_placeholders = os.path.join(config_contents["main_dir"], 'validation_fastas/placeholders')
    force_valid_file = os.path.join(config_contents["main_dir"], 'validation_fastas/force_validation.txt')
    force_blast_file = os.path.join(config_contents["main_dir"], 'blast_result_files/force_blast.txt')

    # Remove Kraken results directory
    if os.path.exists(kraken_results_dir):
        shutil.rmtree(kraken_results_dir)
        logging.info('Kraken results directory removed.')

    # Remove QC files, but keep the cumulative file
    if os.path.exists(qc_dir):
        for filename in os.listdir(qc_dir):
            file_path = os.path.join(qc_dir, filename)
            if file_path != qc_file_to_keep and os.path.isfile(file_path):
                os.remove(file_path)
        logging.info('QC files removed. Cumulative file kept.')

    # Remove validation placeholders
    if os.path.exists(validation_placeholders):
        shutil.rmtree(validation_placeholders)
        logging.info('Validation placeholders removed.')

    # Remove force_validation file
    if os.path.isfile(force_valid_file):
        os.remove(force_valid_file)
        logging.info('Force_validation file removed.')

    # Remove force_blast file
    if os.path.isfile(force_blast_file):
        os.remove(force_blast_file)
        logging.info('Force_blast file removed.')

    logging.info('Cleanup done.')


def timed_senser(config_file):
    """
    Continuously execute the Snakemake workflow at a set time interval.

    Parameters:
        config_file (str): Path to the YAML configuration file.
    """
    logging.info("Starting timed Snakemake workflow")
    config_contents = load_config(config_file)
    t = config_contents['check_intervals_seconds']
    snakemake_cores = config_contents['snakemake_cores']
    snakefile_path = pkg_resources.resource_filename('nanometa_live', 'Snakefile')

    while True:
        try:
            time.sleep(t)
            logging.info(f"Current interval: {t} seconds.")
            execute_snakemake(snakefile_path, snakemake_cores)
            logging.info("Run completed.")
        except KeyboardInterrupt:
            logging.info("Interrupted by user.")
            if config_contents.get('remove_temp_files') == "yes":
                remove_temp_files(config_contents)
            break

def main():
    """
    Main function that parses command-line arguments and executes the timed_senser function.
    """
    logging.info("nanometa_live backend started")

    parser = argparse.ArgumentParser(description='A script that runs the Snakemake workflow at a set time interval.')
    parser.add_argument('--config', default='config.yaml', help='Path to the configuration file. Default is config.yaml.')
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}', help="Show the current version of the script.")
    parser.add_argument('-p', '--path', default='', help="The path to the project directory.")
    args = parser.parse_args()


    # Check if any arguments were provided
    if not any(vars(args).values()):
        print("No arguments provided. Using default values.")
        timed_senser('config.yaml')
    else:
        if hasattr(args, 'version') and args.version:
            parser.print_version()
        else:
            config_file_path = os.path.join(args.path, args.config) if args.path else args.config
            timed_senser(config_file_path)

if __name__ == "__main__":
    main()
