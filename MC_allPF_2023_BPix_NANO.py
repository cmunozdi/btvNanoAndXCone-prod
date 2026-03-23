# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: MC_allPF_2023_BPix --mc --eventcontent NANOAODSIM --datatier NANOAODSIM --conditions auto:phase1_2023_realistic_postBPix --step NANO --nThreads 4 --era Run3,run3_nanoAOD_pre142X --filein /store/mc/Run3Summer23BPixMiniAODv4/ZZ_TuneCP5_13p6TeV_pythia8/MINIAODSIM/130X_mcRun3_2023_realistic_postBPix_v2-v2/50000/13d7b7b9-b42d-429a-8a89-0478ffa64f98.root -n 100 --customise PhysicsTools/NanoAOD/custom_btv_cff.BTVCustomNanoAOD_allPF --customise_commands process.genWeightsTable.keepAllPSWeights=True --no_exec
import FWCore.ParameterSet.Config as cms

from Configuration.Eras.Era_Run3_cff import Run3
from Configuration.Eras.Modifier_run3_nanoAOD_pre142X_cff import run3_nanoAOD_pre142X

process = cms.Process('NANO',Run3,run3_nanoAOD_pre142X)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('PhysicsTools.NanoAOD.nano_cff')
process.load('HLTrigger.HLTfilters.hltHighLevel_cfi')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1),
    output = cms.optional.untracked.allowed(cms.int32,cms.PSet)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('/store/mc/Run3Summer23BPixMiniAODv4/ZZ_TuneCP5_13p6TeV_pythia8/MINIAODSIM/130X_mcRun3_2023_realistic_postBPix_v2-v2/50000/13d7b7b9-b42d-429a-8a89-0478ffa64f98.root'),
    secondaryFileNames = cms.untracked.vstring()
)

process.ak8JetsPt270 = cms.EDFilter(
    "CandViewSelector",
    src = cms.InputTag("slimmedJetsAK8"),
    cut = cms.string("pt > 270")
)

process.atLeastOneAk8JetPt270 = cms.EDFilter(
    "CandViewCountFilter",
    src = cms.InputTag("ak8JetsPt270"),
    minNumber = cms.uint32(1)
)

process.genAk8JetsPt270 = cms.EDFilter(
    "CandViewSelector",
    src = cms.InputTag("slimmedGenJetsAK8"),
    cut = cms.string("pt > 270")
)

process.atLeastOneGenAk8JetPt270 = cms.EDFilter(
    "CandViewCountFilter",
    src = cms.InputTag("genAk8JetsPt270"),
    minNumber = cms.uint32(1)
)

# Combined filter not needed anymore, but kept for reference
process.ak8OrGenAk8JetsPt270 = cms.EDProducer(
    "CandViewMerger",
    src = cms.VInputTag(
        cms.InputTag("ak8JetsPt270"),
        cms.InputTag("genAk8JetsPt270")
    )
)

process.atLeastOneAk8OrGenAk8JetPt270 = cms.EDFilter(
    "CandViewCountFilter",
    src = cms.InputTag("ak8OrGenAk8JetsPt270"),
    minNumber = cms.uint32(1)
)

process.hltEventSelection = process.hltHighLevel.clone(
    TriggerResultsTag = cms.InputTag("TriggerResults", "", "HLT"),
    HLTPaths = cms.vstring(
        "HLT_Mu50_v*",
        "HLT_Ele115_CaloIdVT_GsfTrkIdT_v*",
        "HLT_Photon200_v*",
        "HLT_Ele30_WPTight_Gsf_v*"
    ),
    andOr = cms.bool(True),
    throw = cms.bool(False)
)

process.genLeptonsPt50 = cms.EDFilter(
    "CandViewSelector",
    src = cms.InputTag("prunedGenParticles"),
    cut = cms.string("pt > 50 && (abs(pdgId) == 11 || abs(pdgId) == 13)")
)

process.atLeastOneGenLeptonPt50 = cms.EDFilter(
    "CandViewCountFilter",
    src = cms.InputTag("genLeptonsPt50"),
    minNumber = cms.uint32(1)
)

process.options = cms.untracked.PSet(
    IgnoreCompletely = cms.untracked.vstring(),
    Rethrow = cms.untracked.vstring(),
    TryToContinue = cms.untracked.vstring(),
    accelerators = cms.untracked.vstring('*'),
    allowUnscheduled = cms.obsolete.untracked.bool,
    canDeleteEarly = cms.untracked.vstring(),
    deleteNonConsumedUnscheduledModules = cms.untracked.bool(True),
    dumpOptions = cms.untracked.bool(False),
    emptyRunLumiMode = cms.obsolete.untracked.string,
    eventSetup = cms.untracked.PSet(
        forceNumberOfConcurrentIOVs = cms.untracked.PSet(
            allowAnyLabel_=cms.required.untracked.uint32
        ),
        numberOfConcurrentIOVs = cms.untracked.uint32(0)
    ),
    fileMode = cms.untracked.string('FULLMERGE'),
    forceEventSetupCacheClearOnNewRun = cms.untracked.bool(False),
    holdsReferencesToDeleteEarly = cms.untracked.VPSet(),
    makeTriggerResults = cms.obsolete.untracked.bool,
    modulesToCallForTryToContinue = cms.untracked.vstring(),
    modulesToIgnoreForDeleteEarly = cms.untracked.vstring(),
    numberOfConcurrentLuminosityBlocks = cms.untracked.uint32(0),
    numberOfConcurrentRuns = cms.untracked.uint32(1),
    numberOfStreams = cms.untracked.uint32(0),
    numberOfThreads = cms.untracked.uint32(1),
    printDependencies = cms.untracked.bool(False),
    sizeOfStackForThreadsInKB = cms.optional.untracked.uint32,
    throwIfIllegalParameter = cms.untracked.bool(True),
    wantSummary = cms.untracked.bool(False)
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('MC_allPF_2023_BPix nevts:100'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.NANOAODSIMoutput = cms.OutputModule("NanoAODOutputModule",
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(9),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('NANOAODSIM'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string('MC_allPF_2023_BPix_NANO.root'),
    outputCommands = process.NANOAODSIMEventContent.outputCommands
)

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase1_2023_realistic_postBPix', '')

# Path and EndPath definitions
# Keep the weight accumulators at the front so that we keep the correct genEventCount and genEventSumw
process.weightSequence = cms.Sequence(process.genWeightsTable)
if hasattr(process, 'lheInfoTable'):
    process.weightSequence += process.lheInfoTable

# Define the Reco-level path
process.nanoAOD_step_reco = cms.Path(
    process.weightSequence +
    process.hltEventSelection +
    process.ak8JetsPt270 +
    process.atLeastOneAk8JetPt270 +
    process.nanoSequenceMC
)

# Define the Gen-level path
process.nanoAOD_step_gen = cms.Path(
    process.weightSequence +
    process.genLeptonsPt50 +
    process.atLeastOneGenLeptonPt50 +
    process.genAk8JetsPt270 +
    process.atLeastOneGenAk8JetPt270 +
    process.nanoSequenceMC
)

# EndPath definitions
process.endjob_step = cms.EndPath(process.endOfProcess)
process.NANOAODSIMoutput_step = cms.EndPath(process.NANOAODSIMoutput)

# Configure the output module for the logical OR of both paths
process.NANOAODSIMoutput.SelectEvents = cms.untracked.PSet(
    SelectEvents = cms.vstring('nanoAOD_step_reco', 'nanoAOD_step_gen')
)

# Final Schedule
process.schedule = cms.Schedule(
    process.nanoAOD_step_reco,
    process.nanoAOD_step_gen,
    process.endjob_step,
    process.NANOAODSIMoutput_step
)

from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

#Setup FWK for multithreaded
process.options.numberOfThreads = 4
process.options.numberOfStreams = 0

# customisation of the process.

# Automatic addition of the customisation function from PhysicsTools.NanoAOD.custom_btv_cff
from PhysicsTools.NanoAOD.custom_btv_cff import BTVCustomNanoAOD_allPF 

#call to customisation function BTVCustomNanoAOD_allPF imported from PhysicsTools.NanoAOD.custom_btv_cff
process = BTVCustomNanoAOD_allPF(process)

# Automatic addition of the customisation function from PhysicsTools.NanoAOD.nano_cff
from PhysicsTools.NanoAOD.nano_cff import nanoAOD_customizeCommon 

#call to customisation function nanoAOD_customizeCommon imported from PhysicsTools.NanoAOD.nano_cff
process = nanoAOD_customizeCommon(process)

# End of customisation functions


# Customisation from command line

process.genWeightsTable.keepAllPSWeights=True
# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
