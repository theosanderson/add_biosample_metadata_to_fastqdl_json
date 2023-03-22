# add_biosample_metadata_to_fastqdl_json


[Fastq-dl](https://github.com/rpetit3/fastq-dl) is a great tool for downloading, for example, all the fastq files from a BioProject. It creates a file called `fastq-run-info.json` with information about each run.

The script in this repo reads in this file, queries the ENA API for the metadata associated with each BioSample in it, and adds this additional metadata to a copy of that file.

Usage example:
```
python add_biosample_metadata_to_fastqdl_json.py fastq-run-info.json --output fastq-run-info-with-extra.json
```
