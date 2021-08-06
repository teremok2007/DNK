#!/bin/bash
#source /etc/profile
echo HOSTNAME=$HOSTNAME
export HOSTNAME=`hostname`
export USER=`whoami`
export HOUDINI_USE_HFS_PYTHON=1
# export HSTUDIO_PATH=/studio/tools/hou/hou

# Various applications uses own python:
unset PYTHONHOME

export HOUDINI_LOCATION=/studio/tools/hou/hfs17.5.173/
export CGRU_PATH=/studio/tools/rendermanager/cgru/
# export CGRU_PATH=/studio/tools/af_2.2.2/cgru/
cd $CGRU_PATH  && source ./setup.sh
cd ~

echo "Houdni location = '$HOUDINI_LOCATION'"

# Setup CGRU houdini scripts location:
export HOUDINI_CGRU_PATH=$CGRU_LOCATION/plugins/houdini

# Set Afanasy houdini scripts and otls location:
export HOUDINI_AF_PATH=$AF_ROOT/plugins/houdini

# Set Python path to afanasy submission script:
export PYTHONPATH=$HOUDINI_AF_PATH:$PYTHONPATH:$HSTUDIO_PATH

# Define OTL scan path:
HOUDINI_AF_OTLSCAN_PATH=$HIH/otls:$HOUDINI_AF_PATH:$HH/otls

# Create or add to exist OTL scan path:
export HOUDINI_OTLSCAN_PATH="${HOUDINI_AF_OTLSCAN_PATH}:${HOUDINI_OTLSCAN_PATH}"
export PATH=$CGRU_PATH/software_setup/bin:$PATH
#export HOUDINI_TOOLBAR_PATH='@:/studio/tools/hou/shelf/'

export HOUDINI_IMAGE_DISPLAY_GAMMA=2.2
export HOUDINI_EXTERNAL_HELP_BROWSER=firefox

echo $HOUDINI_OTLSCAN_PATH
echo $PYTHONPATH
echo $HOUDINI_AF_PATH
export APP_DIR="$HOUDINI_LOCATION"
export APP_EXE="/studio/tools/hou/hfs17.5.173/bin/hython"
#export LD_LIBRARY_PATH=/studio/tools/openvdb:$LD_LIBRARY_PATH
export HOUDINI_PYTHON_PANEL_PATH="$HOUDINI_PYTHON_PANEL_PATH:/studio/tools/hou/python_panels:/studio/tools/hou/plugins/pdg_mutagen/houdini/python_panels;&"
export PYTHONPATH=$PYTHONPATH:$HOUDINI_PYTHON_PANEL_PATH

#qLIB
export QLIB=/studio/tools/hou/qLib
export HOUDINI_OTLSCAN_PATH=@/otls:$QLIB/otls/base:$QLIB/otls/future:$QLIB/otls/experimental:/studio/tools/hou/otl/OTL_WORK/Studio_Tools:/studio/tools/hou/otl/OTL_WORK/T-34:/studio/tools/hou/otl/OTL_WORK/Temp
export HOUDINI_GALLERY_PATH=$QLIB/gallery:@/gallery:/studio/tools/hou/gallery
#export HOUDINI_TOOLBAR_PATH=$QLIB/toolbar:@/toolbar
export HOUDINI_SCRIPT_PATH=$QLIB/scripts:@/scripts

#studio shelf and qLib shelf
export HOUDINI_TOOLBAR_PATH=/studio/tools/hou/toolbar:@/toolbar:$QLIB/toolbar

export HOUDINI_DSO_PATH="$HOUDINI_DSO_PATH:/studio/tools/hou/dso/Substance_Plugin;&"

LC_ALL=C $APP_EXE $@
