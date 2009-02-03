#
#Use this cfg file to process the BcGenerator output with the LHEInterface for hadronization
#
#!/usr/bin/env cmsRun
import FWCore.ParameterSet.Config as cms

process = cms.Process("Gen")
process.load("Configuration.StandardSequences.Generator_cff")
process.load("Configuration.StandardSequences.Services_cff")
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.threshold = 'INFO'
process.load('Configuration/StandardSequences/VtxSmearedEarly10TeVCollision_cff')
#process.load('Configuration/StandardSequences/VtxSmearedGauss_cff')
process.load("Configuration.Generator.PythiaUESettings_cfi")
process.load('Configuration/EventContent/EventContent_cff')

process.source = cms.Source("LHESource",
	fileNames = cms.untracked.vstring('file:/gwpool/users/taroni/Bc/CMSSW_2_1_9/src/GeneratorInterface/DedicatedExtGen/test/BCVEGPY.lhe')
)

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))

process.configurationMetadata = cms.untracked.PSet(
	version = cms.untracked.string('alpha'),
	name = cms.untracked.string('LHEF input'),
	annotation = cms.untracked.string('bcvegpy')
)


process.RandomNumberGeneratorService.generator = cms.PSet(
	initialSeed = cms.untracked.uint32(123456789),
	engineName = cms.untracked.string('HepJamesRandom')
        )


process.generator = cms.EDProducer("LHEProducer",
	eventsToPrint = cms.untracked.uint32(2),
        hadronisation = cms.PSet(
		process.pythiaUESettingsBlock,
		generator = cms.string('Pythia6'),
		maxEventsToPrint = cms.untracked.int32(2),
		pythiaPylistVerbosity = cms.untracked.int32(2),
		parameterSets = cms.vstring(
			'pythiaUESettings', 
                        'processParameters'
		),
                processParameters = cms.vstring(
                      'MSTP(51)=10042',
                      'MSTP(52)=2',
		      'MSTP(61)=0             ! Hadronization of the initial protons',
                      'MDME(997,2) = 0        ! PHASE SPACE',
                      'BRAT(997)   = 1.       ! BRANCHING FRACTION',
                      'KFDP(997,1) = 211      ! pi+',
                      'KFDP(997,2) = 443      ! J/psi',
                      'KFDP(997,3) = 0        ! nada',
                      'KFDP(997,4) = 0        ! nada',
                      'KFDP(997,5) = 0        ! nada',
                      'PMAS(143,1) = 6.286',
                      'PMAS(143,4) = 0.138',
                      # J/psi decays
                      'MDME(858,1) = 0  ! J/psi->e+e-',
                      'MDME(859,1) = 1  ! J/psi->mumu',
                      'MDME(860,1) = 0',
                      
                      'MDME(998,1) = 3',
                      'MDME(999,1) = 3',
                      'MDME(1000,1) = 3',
                      'MDME(1001,1) = 3',
                      'MDME(1002,1) = 3',
                      'MDME(1003,1) = 3',
                      'MDME(1004,1) = 3',
                      'MDME(1005,1) = 3',
                      'MDME(1006,1) = 3',
                      'MDME(1007,1) = 3',
                      'MDME(1008,1) = 3',
                      'MDME(1009,1) = 3',
                      'MDME(1010,1) = 3',
                      'MDME(1011,1) = 3',
                      'MDME(1012,1) = 3',
                      'MDME(1013,1) = 3',
                      'MDME(1014,1) = 3',
                      'MDME(1015,1) = 3',
                      'MDME(1016,1) = 3',
                      'MDME(1017,1) = 3',
                      'MDME(1018,1) = 3',
                      'MDME(1019,1) = 3',
                      'MDME(1020,1) = 3',
                      'MDME(1021,1) = 3',
                      'MDME(1022,1) = 3',
                      'MDME(1023,1) = 3',
                      'MDME(1024,1) = 3',
                      'MDME(1025,1) = 3',
                      'MDME(1026,1) = 3',
                      'MDME(1027,1) = 3',	       
                      'MDME(997,1) = 2        !  Bc -> pi J/Psi',		   
                      'MSTJ(22)=2   ! Do not decay unstable particles',
                      'PARJ(71)=10. ! with c*tau > cTauMin (in mm) in PYTHIA'
                )
           )
)

process.p0 = cms.Path(
	process.generator *
	process.pgen
)

process.VtxSmeared.src = 'generator'
process.genEventWeight.src = 'generator'
process.genEventScale.src = 'generator'
process.genEventPdfInfo.src = 'generator'
process.genParticles.src = 'generator'
process.genParticleCandidates.src = 'generator'

process.genParticles.abortOnUnknownPDGCode = False

process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")

process.printList = cms.EDFilter("ParticleListDrawer",
	src = cms.InputTag("genParticles"),
	maxEventsToPrint = cms.untracked.int32(-1)
)

process.printTree = cms.EDFilter("ParticleTreeDrawer",
	src = cms.InputTag("genParticles"),
	printP4 = cms.untracked.bool(False),
	printPtEtaPhi = cms.untracked.bool(False),
	printVertex = cms.untracked.bool(True),
	printStatus = cms.untracked.bool(False),
	printIndex = cms.untracked.bool(False),
	status = cms.untracked.vint32(1, 2, 3)
)

process.p = cms.Path(
	process.printList *
	process.printTree
)

0
process.GEN = cms.OutputModule("PoolOutputModule",
	process.FEVTSIMEventContent,
	dataset = cms.untracked.PSet(dataTier = cms.untracked.string('GEN')),
	SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('p0')),
	fileName = cms.untracked.string('newGen.root')
)
process.GEN.outputCommands.append("keep *_generator_*_*")

process.outpath = cms.EndPath(process.GEN)

process.schedule = cms.Schedule(process.p0, process.outpath)
