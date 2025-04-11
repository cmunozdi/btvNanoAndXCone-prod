import os
from CRABClient.UserUtilities import config
config = config()

config.General.requestName = '_requestName_'
config.General.workArea = '_workArea_'
config.General.transferLogs = True 

config.JobType.pluginName = 'Analysis'
config.JobType.disableAutomaticOutputCollection = True #This avoids to copy the output file from cmsRun to the crab output directory, although it is generated in the specific job crab workdir
config.JobType.psetName = '_psetName_'
config.JobType.maxMemoryMB = 5000 
config.JobType.numCores = 4
config.JobType.allowUndistributedCMSSW = True

cmssw_base = os.environ['CMSSW_BASE']
config.JobType.scriptExe = '_postprocess_'
config.JobType.inputFiles = [
                                '_postprocess_',
                                f'{cmssw_base}/src/XConeReclustering/ProcessNanoToBoostedTopQuarkWithXCone.py',
                                f'{cmssw_base}/src/XConeReclustering/selection_helpers_BoostedTopQuark.h',
                                f'{cmssw_base}/src/XConeReclustering/deltaPhi.h',
                                f'{cmssw_base}/src/XConeReclustering/deltaR.h',
                                f'{cmssw_base}/src/XConeReclustering/selection_helpers_BoostedTopQuark.cc'
                            ]
config.JobType.outputFiles = ['_outXConeFileName_']

config.Debug.extraJDL = ['+CMS_ALLOW_OVERFLOW=False']

config.Data.inputDataset = '_inputDataset_'
config.Data.outputDatasetTag = '_outputDatasetTag_'
config.Data.outLFNDirBase = '_outLFNDirBase_'
config.Data.splitting = '_splitting_'
config.Data.ignoreLocality = False
config.Data.publication = _publication_
config.Data.allowNonValidInputDataset = True
config.Data.publishDBS = 'phys03'

config.Site.storageSite = '_storageSite_'