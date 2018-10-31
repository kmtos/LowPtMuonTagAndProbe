#!/bin/bash

export SCRAM_ARCH=slc6_amd64_gcc491
cd  /afs/cern.ch/work/k/ktos/public/CMSSW_7_4_10/src/
eval `scramv1 runtime -sh`
cd -
source /afs/cern.ch/cms/caf/setup.sh
cp /afs/cern.ch/work/k/ktos/public/CMSSW_7_4_10/src/MuonAnalysis/TagAndProbe/test/zmumu/fitMuonID_DY_RunAll_BSUB.py .
cmsRun fitMuonID_DY_RunAll_BSUB.py
exit 0
