## (GA4GH > Oncotator > MutSig)
### GA4GH Client
Source Code: https://github.com/jacmarjorie/ga4gh_galaxy_interface/blob/harmony_point/ga4gh_hp_client.py

Example Run: 

    python ga4gh_hp_client.py \
    -u http://192.168.100.136:10022 http://192.168.100.137:10022 \
    -o /opt/output/allvariants.txt

Generic Run: python ga4gh_hp_client.py -u gateway_url_1 gateway_url_2 -o path_to_output_file -q query term
* Note that -q is optional.

Docker execution: 
* Assuming that we want to write the output of the ga4gh_client to /path/to/write/ga4gh/out/. Note that in the original July MutSig workflow, this output needed to be written in a secure location and could not be written (without encryption) to the NFS.

Example command:

    docker run -v /path/to/write/ga4gh/out/:/opt/data:rw \
    -t ga4gh \
    python /opt/ga4gh_client/ga4gh_hp_client.py \
    -u http://localhost:5000/variants/search \
    -o /opt/data/output.txt

### Oncotator
Source Code: https://github.com/broadinstitute/oncotator

Full Instructions to Install here: http://gatkforums.broadinstitute.org/discussion/4154/howto-install-and-run-oncotator-for-the-first-time. Note from these instructions that Oncotator relies on the 14G datasource referenced in that link, as well as the clincial override file.

Example command: 

    oncotator \
    -v \
    -c /opt/data/oncotator/trans.over.clin.txt \
    --db-dir /opt/data/oncotator/oncotator_v1_ds_Jan262014/ \
    /opt/data/input/test.txt \
    /opt/oncotator_output.tsv \
    hg19


* In a clinical setting, Oncotator is ran with the -c flag using this file: https://www.broadinstitute.org/~lichtens/oncobeta/tx_exact_uniprot_matches.AKT1_CRLF2_FGFR1.txt

Docker execution:
* Assuming your oncotator datasource (in a folder called oncotator_v1_ds_Jan262014) is located at /path/to/oncotator/datasource, the static reference files are located at /path/to/oncotator/static/files (this includes file references above with -c option), the input file exist at /path/to/oncotator/input, and the output file should be written to /path/to/write/oncotator/output

Example command:

    docker run \
    -v /path/to/oncotator/datasource/:/opt/oncotator_datasource:rw \
    -v /path/to/oncotator/static/files:/opt/oncotator_files:rw \
    -v /path/to/oncotator/input/:/opt/oncotator_input:rw \
    -v /path/to/write/oncotator/output:/opt/oncotator_output \
    -t oncotator \
    oncotator -v -c /opt/oncotator_files/trans.over.clin.txt \
    --db-dir /opt/oncotator_datasource/oncotator_v1_ds_Jan262014/ \
    /opt/oncotator_input/test.txt \
    /opt/oncotator_output/oncotator_output.tsv \
    hg19

### MutSig
Source Code: https://www.broadinstitute.org/cancer/cga/sites/default/files/data/tools/mutsig/MutSigCV_1.4.zip

* MutSig is depedent on MatLab compiler R2013a: 
http://www.mathworks.com/supportfiles/MCR_Runtime/R2013a/MCR_R2013a_glnxa64_installer.zip && unzip MCR_R2013a_glnxa64_installer.zip

Static Input Files: http://www.broadinstitute.org/cancer/cga/mutsig_run#reference_files

To run MutSigCV in this way, please first download the following four reference files:

1. genome reference sequence: chr_files_hg18.zip or chr_files_hg19.zip, unzip this file to yield a directory (chr_files_hg18/ or chr_files_hg19/) of chr*.txt files.

2. mutation_type_dictionary_file.txt

3. exome_full192.coverage.txt.zip; unzip this file to yield exome_full192.coverage.txt

4. gene.covariates.txt

Docker execution:

* Assuming all static files listed above exist at /path/to/mutsig/static_files/, and the output will be written to a file prepended with test_out at location /path/to/write/mutsig/output

Example command:

    docker run -v /path/to/mutsig/static_files/:/opt/mutsig/data:rw \
    -v /path/to/write/mutsig/output:/opt/mutsig/out:rw \
    -t mutsig /opt/mutsig/MutSigCV_1.4/run_MutSigCV.sh \
    /usr/local/MATLAB/MATLAB_Compiler_Runtime/v81 \
    /opt/mutsig/data/LUSC.maf \
    /opt/mutsig/data/exome_full192.coverage.txt \
    /opt/mutsig/data/gene.covariates.txt \
    /opt/mutsig/out/test_out \
    /opt/mutsig/data/mutation_type_dictionary_file.txt \
    /opt/mutsig/data/chr_files_hg19
