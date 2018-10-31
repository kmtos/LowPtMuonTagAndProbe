import FWCore.ParameterSet.Config as cms

process = cms.Process("TagProbe")

process.load('FWCore.MessageService.MessageLogger_cfi')
process.source = cms.Source("EmptySource")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )

process.TnP_Muon_ID = cms.EDAnalyzer("TagProbeFitTreeAnalyzer",
    ## Input, output 
    InputFileNames = cms.vstring("file:../../../SkimTrees/skimmedTree_DY_MTight_RunB_IsoMu24_tagPtgt26p0_80to100_PART2.root",
 				 "file:../../../SkimTrees/skimmedTree_DY_MTight_RunC_IsoMu24_tagPtgt26p0_80to100_PART2.root",
				 "file:../../../SkimTrees/skimmedTree_DY_MTight_RunD_IsoMu24_tagPtgt26p0_80to100_PART2.root",
                                 "file:../../../SkimTrees/skimmedTree_DY_MTight_RunE_IsoMu24_tagPtgt26p0_80to100_PART2.root", 
                                 "file:../../../SkimTrees/skimmedTree_DY_MTight_RunF_IsoMu24_tagPtgt26p0_80to100_PART2.root", 
				 ), 
    OutputFileName = cms.string("TnP_Muon_ID_RunBF_DY_IsoMu24_pt26_80to100_PART2.root"),
    InputTreeName = cms.string("fitter_tree"), 
    InputDirectoryName = cms.string("tpTree"),  
    ## Variables for binning
    Variables = cms.PSet(
        mass   = cms.vstring("Tag-muon Mass", "80", "100", "GeV/c^{2}"),
        pt     = cms.vstring("muon p_{T}", "0", "100", "GeV/c"),
        abseta = cms.vstring("muon |#eta|", "0", "2.5", ""),
    ),
    ## Flags you want to use to define numerator and possibly denominator
    Categories = cms.PSet(
        Medium = cms.vstring("Medium", "dummy[pass=1,fail=0]"),
        Medium2016 = cms.vstring("Medium2016", "dummy[pass=1,fail=0]"),
        Loose = cms.vstring("Loose", "dummy[pass=1,fail=0]"),
    ),
    ## What to fit
    Efficiencies = cms.PSet(
        Medium_pt_eta = cms.PSet(
            UnbinnedVariables = cms.vstring("mass"),
            EfficiencyCategoryAndState = cms.vstring("Medium", "pass"), ## Numerator definition
            BinnedVariables = cms.PSet(
                ## Binning in continuous variables
                pt     = cms.vdouble( 3, 10, 15, 20 ),
                abseta = cms.vdouble( 0.0, .9, 1.2, 2.1, 2.4),
                ## flags and conditions required at the denominator, 
            ),
            BinToPDFmap = cms.vstring("vpvPlusExpo"), ## PDF to use, as defined below
        ),
       Medium2016_pt_eta = cms.PSet(
           UnbinnedVariables = cms.vstring("mass"),
           EfficiencyCategoryAndState = cms.vstring("Medium2016", "pass"), ## Numerator definition
           BinnedVariables = cms.PSet(
               ## Binning in continuous variables
               pt     = cms.vdouble( 3, 10, 15, 20 ),
               abseta = cms.vdouble( 0.0, .9, 1.2, 2.1, 2.4),
               ## flags and conditions required at the denominator, 
           ),
           BinToPDFmap = cms.vstring("vpvPlusExpo"), ## PDF to use, as defined below
       ),
       Loose_pt_eta = cms.PSet(
           UnbinnedVariables = cms.vstring("mass"),
           EfficiencyCategoryAndState = cms.vstring("Loose", "pass"), ## Numerator definition
           BinnedVariables = cms.PSet(
               ## Binning in continuous variables
               pt     = cms.vdouble( 3, 10, 15, 20 ),
               abseta = cms.vdouble( 0.0, .9, 1.2, 2.1, 2.4),
               ## flags and conditions required at the denominator, 
           ),
           BinToPDFmap = cms.vstring("vpvPlusExpo"), ## PDF to use, as defined below
       ),

    ),
    PDFs = cms.PSet(
        vpvPlusExpo = cms.vstring(
            "Voigtian::signal1(mass, mean1[90,85,95], width[2.495], sigma1[2,1,3])",
            "Voigtian::signal2(mass, mean2[90,85,95], width,        sigma2[4,2,10])",
            "SUM::signal(vFrac[0.8,0,1]*signal1, signal2)",
            "Exponential::backgroundPass(mass, lp[-0.1,-1,0.1])",
            "Exponential::backgroundFail(mass, lf[-0.1,-1,0.1])",
            "efficiency[0.9,0,1]",
            "signalFractionInPassing[0.9]"
        ),
    ),

    ## How to do the fit
    binnedFit = cms.bool(True),
    binsForFit = cms.uint32(40),
    saveDistributionsPlot = cms.bool(True),
    NumCPU = cms.uint32(1), ## leave to 1 for now, RooFit gives funny results otherwise
    SaveWorkspace = cms.bool(False),
)

#### Slighly different configuration for isolation, where the "passing" is defined by a cut
process.TnP_Muon_Iso = process.TnP_Muon_ID.clone(
    OutputFileName = cms.string("TnP_Muon_Iso_RunBF_DY_IsoMu24_pt26_80to100.root"),
    ## More variables
    Variables = process.TnP_Muon_ID.Variables.clone(
        combRelIsoPF04dBeta = cms.vstring("PF Combined Relative Iso", "0", "4", ""),
    ),
    ## Cuts: name, variable, cut threshold
    Cuts = cms.PSet(
        RelIso = cms.vstring("RelIso" ,"combRelIsoPF04dBeta", "0.25"),
    ),
    ## What to fit
    Efficiencies = cms.PSet(
        Iso_MediumID = cms.PSet(
            UnbinnedVariables = cms.vstring("mass"),
            EfficiencyCategoryAndState = cms.vstring("RelIso", "below"), ## variable is below cut value 
            BinnedVariables = cms.PSet(
                Medium = cms.vstring("pass"),                 ## 
                pt     = cms.vdouble( 3, 10, 15, 20 ),
                abseta = cms.vdouble( 0.0, .9, 1.2, 2.1, 2.4 ),
            ),
            BinToPDFmap = cms.vstring("vpvPlusExpo"), ## PDF to use, as defined below
        ),
        Iso_Medium2016ID = cms.PSet(
            UnbinnedVariables = cms.vstring("mass"),
            EfficiencyCategoryAndState = cms.vstring("RelIso", "below"), ## variable is below cut value 
            BinnedVariables = cms.PSet(
                Medium2016 = cms.vstring("pass"),                 ## 
                pt     = cms.vdouble( 3, 10, 15, 20 ),
                abseta = cms.vdouble( 0.0, .9, 1.2, 2.1, 2.4 ),
            ),
            BinToPDFmap = cms.vstring("vpvPlusExpo"), ## PDF to use, as defined below
        ),
        Iso_LooseID = cms.PSet(
            UnbinnedVariables = cms.vstring("mass"),
            EfficiencyCategoryAndState = cms.vstring("RelIso", "below"), ## variable is below cut value 
            BinnedVariables = cms.PSet(
                Loose = cms.vstring("pass"),                 ## 
                pt     = cms.vdouble( 3, 10, 15, 20 ),
                abseta = cms.vdouble( 0.0, .9, 1.2, 2.1, 2.4 ),
            ),
            BinToPDFmap = cms.vstring("vpvPlusExpo"), ## PDF to use, as defined below
        ),
    ),

)
#process.p1 = cms.Path(process.TnP_Muon_ID)
process.p2 = cms.Path(process.TnP_Muon_Iso)
