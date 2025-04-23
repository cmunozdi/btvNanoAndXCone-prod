#!/bin/bash
set -e 

echo "Starting post-processing"

# Printing environment variables for debugging
# echo "Environment variables:"
# env
# echo "Current directory:"
# pwd
# echo "Directory contents:"
# ls -l

# Set up the environment for CMSSW
# export SCRAM_ARCH=el9_amd64_gcc11
# source /cvmfs/cms.cern.ch/cmsset_default.sh
# eval `scramv1 runtime -sh`

# Cambiar al directorio base de CMSSW
cd $CMSSW_BASE
echo pwd
# Capturar la salida de scram tool info fastjet-contrib
FJC_INFO=$(scram tool info fastjet-contrib)

# Extraer las rutas necesarias
export FASTJET_CONTRIB_BASE=$(echo "$FJC_INFO" | grep "FASTJET_CONTRIB_BASE" | cut -d '=' -f 2)
export CPLUS_INCLUDE_PATH=$FASTJET_CONTRIB_BASE/include:$CPLUS_INCLUDE_PATH
export LD_LIBRARY_PATH=$FASTJET_CONTRIB_BASE/lib:$LD_LIBRARY_PATH

# Regresar al directorio original
cd -

# Shows fastjet-contib information
# echo "Checking fastjet-contrib configuration:"
# scram tool info fastjet-contrib || echo "fastjet-contrib not found or not configured properly."

echo "Running cmsRun to generate NANO.root"
cmsRun -j FrameworkJobReport.xml PSet.py #data_2023_22Sep2023_NANO.py > cmsRun.log 2>&1 #PSet.py #
# cmsRun -j FrameworkJobReport.xml -p data_2023_22Sep2023_NANO.py #PSet.py #

# Search for the output NANOAODSIM file from cmsRun using CRAB_localOutputFiles
if [ -n "$CRAB_localOutputFiles" ]; then
    # Extraer el nombre de salida después del '='
    NANO_FILE=$(echo "$CRAB_localOutputFiles" | awk -F'=' '{print $2}')
    echo "Crab local output files found: $NANO_FILE"
else
    # If the variable is not defined, search for the pattern
    NANO_FILE=$(ls *NANO*.root 2>/dev/null | head -n 1)
    echo "No Crab local output files found, searching for NANO files: $NANO_FILE"
fi

if [ -z "$NANO_FILE" ]; then
    echo "NANO file not found"
    ls -l
    exit 1
fi

echo "NANO file found: $NANO_FILE"

NANO_FILE_BASENAME=$(basename "$NANO_FILE")
# Derivate the output file name for XConeReclustering
XCONE_OUTPUT_FILE=$(echo "$NANO_FILE_BASENAME" | sed 's/NANO/XCone/')

echo "XCone output file will be: $XCONE_OUTPUT_FILE"


# Executes the reclustering with XCone
python3 ProcessNanoToBoostedTopQuarkWithXCone.py --input "$NANO_FILE" --output "$XCONE_OUTPUT_FILE" #--isMC

# Derivate output file name with runs tree
RUNS_OUTPUT_FILE="${XCONE_OUTPUT_FILE/.root/_runs.root}"
echo "Runs output file is: $RUNS_OUTPUT_FILE"

# Derivate output file name with Luminosity Blocks tree
LUMI_OUTPUT_FILE="${XCONE_OUTPUT_FILE/.root/_lumi.root}"
echo "Luminosity Blocks output file is: $LUMI_OUTPUT_FILE"

# Verify both output files exist
if [ ! -f "$XCONE_OUTPUT_FILE" ]; then
    echo "ERROR: XCone output file $XCONE_OUTPUT_FILE not found!"
    exit 1
fi
if [ ! -f "$RUNS_OUTPUT_FILE" ]; then
    echo "ERROR: Runs output file $RUNS_OUTPUT_FILE not found!"
    exit 1
fi
if [ ! -f "$LUMI_OUTPUT_FILE" ]; then
    echo "ERROR: Luminosity Blocks output file $LUMI_OUTPUT_FILE not found!"
    exit 1
fi

# Merge the XCone output file with the runs tree
FINAL_OUTPUT_FILE="final_${XCONE_OUTPUT_FILE}"
echo "Final output file will be: $FINAL_OUTPUT_FILE"
hadd -f "$FINAL_OUTPUT_FILE" "$XCONE_OUTPUT_FILE" "$RUNS_OUTPUT_FILE" "$LUMI_OUTPUT_FILE"

# Replace the original file with the merged one
mv "$FINAL_OUTPUT_FILE" "$XCONE_OUTPUT_FILE"
rm -f "$RUNS_OUTPUT_FILE" "$LUMI_OUTPUT_FILE"

# Delete intermediate files
# rm -f "$NANO_FILE"
# rm -f $SKIM_FILE

echo "Post-processing completed"


# # Ejecutar nano_postproc.py sin directorios intermedios
# python3 $CMSSW_BASE/src/PhysicsTools/NanoAODTools/scripts/nano_postproc.py . $NANO_FILE --bo $CMSSW_BASE/src/PhysicsTools/NanoAODTools/scripts/keep_and_drop.txt
# # python3 nano_postproc.py . "$NANO_FILE" --bo keep_and_drop.txt

# # Buscar el archivo generado por nano_postproc.py
# SKIM_FILE=$(ls *Skim.root | head -n 1)

# if [ -z "$SKIM_FILE" ]; then
#     echo "Skim file not found"
#     exit 1
# fi

# # Ejecutar haddnano.py sin directorios intermedios
# python3 $CMSSW_BASE/src/PhysicsTools/NanoAODTools/scripts/haddnano.py testNano_NANO_Skim_haddnano.root $SKIM_FILE
# # python3 haddnano.py testNano_NANO_Skim_haddnano.root "$SKIM_FILE"

# # Buscar el archivo generado por haddnano.py
# HADD_FILE=$(ls *haddnano.root | head -n 1)

# if [ -z "$HADD_FILE" ]; then
#     echo "Hadd file not found"
#     exit 1
# fi