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

# Mover ek archivo NANO a un directorio temporal
# TEMP_DIR=$(mktemp -d)
# mv "$NANO_FILE" "$TEMP_DIR"
NANO_FILE_BASENAME=$(basename "$NANO_FILE")
# NANO_FILE="$TEMP_DIR/$NANO_FILE_BASENAME"

# Derivate the output file name for XConeReclustering
XCONE_OUTPUT_FILE=$(echo "$NANO_FILE_BASENAME" | sed 's/NANO/XCone/')

echo "XCone output file will be: $XCONE_OUTPUT_FILE"


# Executes the reclustering with XCone
python3 ProcessNanoToBoostedTopQuarkWithXCone.py --input "$NANO_FILE" --output "$XCONE_OUTPUT_FILE" --isMC
# python3 $CMSSW_BASE/src/XConeReclustering/ProcessNanoToBoostedTopQuarkWithXCone.py --input "$NANO_FILE" --output "$XCONE_OUTPUT_FILE" #--isMC

# Delete intermediate files
# rm -f $NANO_FILE
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