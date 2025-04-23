import os
import subprocess
import yaml
import re  # Importar el módulo de expresiones regulares

# Configuración
cmsrun_config = "ana.py"  # Archivo de configuración de cmsRun
max_events = -1  # Número máximo de eventos a procesar (-1 para todos)
output_dir = "./xsec_results"  # Directorio para guardar los resultados
os.makedirs(output_dir, exist_ok=True)

# Directorio donde están los archivos YAML
yaml_dir = os.path.join(os.environ["CMSSW_BASE"], "src/XConeReclustering/btvNanoAndXCone-prod/crab_ymls")

# Archivos YAML específicos que queremos procesar
yaml_files = [
    "mc_summer23_st.yml",
    "mc_summer23_ttbar.yml",
    "mc_summer23_wjets.yml"
]
yaml_files = [os.path.join(yaml_dir, yml) for yml in yaml_files]

# Función para cargar datasets desde un archivo YAML
def load_datasets_from_yaml(yaml_file):
    with open(yaml_file, "r") as f:
        data = yaml.safe_load(f)
    datasets = data.get("campaign", {}).get("datasets", "").strip().split("\n")
    return [d.strip() for d in datasets if d.strip()]

# Función para obtener un archivo ROOT de un dataset usando dasgoclient
def get_root_file_from_dataset(dataset):
    try:
        das_output = subprocess.check_output(
            ["dasgoclient", "-query", f"file dataset={dataset}", "-limit", "1"],
            text=True
        )
        root_file = das_output.strip()
        if root_file:
            return f"root://xrootd-cms.infn.it/{root_file}"
    except subprocess.CalledProcessError as e:
        print(f"Error querying DAS for dataset {dataset}: {e}")
    return None

# Función para ejecutar cmsRun con un archivo ROOT
def run_cmsrun(input_file, dataset_name):
    try:
        cmsrun_command = [
            "cmsRun", cmsrun_config,
            f"inputFiles={input_file}",
            f"maxEvents={max_events}"
        ]
        print(f"Running cmsRun for dataset {dataset_name}...")
        cmsrun_output = subprocess.run(cmsrun_command, capture_output=True, text=True, check=True)
        
        # Combinar stdout y stderr
        cmsrun_stdout = cmsrun_output.stdout
        cmsrun_stderr = cmsrun_output.stderr
        cmsrun_output_combined = cmsrun_stdout + cmsrun_stderr

        # Buscar la línea que contiene "After matching: total cross section"
        for line in cmsrun_output_combined.splitlines():
            if "After matching: total cross section" in line:
                print(f"Dataset: {dataset_name}")
                print(line)  # Imprimir la línea original

                # Extraer los valores de la cross section y la incertidumbre
                match = re.search(r"After matching: total cross section = ([\d\.e+-]+) \+/- ([\d\.e+-]+) pb", line)
                if match:
                    cross_section = float(match.group(1))
                    uncertainty = float(match.group(2))

                    # Formatear con más cifras significativas
                    print(f"Formatted cross section: {cross_section:.10g} pb")
                    print(f"Formatted uncertainty: {uncertainty:.10g} pb")
                print(f"\n\n")
                break
        else:
            print(f"Failed to find 'After matching: total cross section' for dataset {dataset_name}")

    except subprocess.CalledProcessError as e:
        print(f"cmsRun failed for dataset {dataset_name}")
        print(e.stderr)
        
# Procesar únicamente los archivos YAML especificados
for yaml_file in yaml_files:
    print(f"Processing datasets from {yaml_file}...")
    datasets = load_datasets_from_yaml(yaml_file)

    for dataset in datasets:
        print(f"Processing dataset: {dataset}")
        root_file = get_root_file_from_dataset(dataset)
        if root_file:
            run_cmsrun(root_file, dataset)
        else:
            print(f"Failed to get ROOT file for dataset {dataset}")