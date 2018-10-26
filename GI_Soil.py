import os
import sys
import argparse
import textwrap

from ecohydrolib.context import Context
from ecohydrolib.metadata import GenericMetadata
from ecohydrolib.metadata import AssetProvenance
from ecohydrolib.spatialdata.utils import deleteShapefile
from ecohydrolib.spatialdata.utils import bboxFromString
from ecohydrolib.spatialdata.utils import convertGMLToShapefile
from ecohydrolib.ssurgo.featurequery import getMapunitFeaturesForBoundingBox
from ecohydrolib.ssurgo.featurequery import SSURGO_BBOX_TILE_DIVISOR
from ecohydrolib.ssurgo import featurequery

parser = argparse.ArgumentParser(description='Update MetaData file to use GI Soils')
parser.add_argument('-s', '--shapefile', dest='shpFilename', required=True, help='The name of the GI soil shapefile')
parser.add_argument('-p', '--projectDir', dest='projectDir', required=True, help='The directory to which metadata, intermediate, and final files should be saved')
parser.add_argument('--overwrite', dest='overwrite', action='store_true', required=False,help='Overwrite existing SSURGO features shapefile in project directory.  If not specified, program will halt if a dataset already exists.')

args = parser.parse_args()
cmdline = GenericMetadata.getCommandLine()

configFile = None

context = Context(args.projectDir, configFile) 
manifest = GenericMetadata.readManifestEntries(context)
if 'soil_features' in manifest:
    if args.overwrite:
        sys.stdout.write('Deleting existing SSURGO features shapefile\n')
        sys.stdout.flush()
        shpFilepath = os.path.join( context.projectDir, manifest['soil_features'] )
        deleteShapefile(shpFilepath)
    else:
        sys.exit( textwrap.fill('SSURGO features already exist in project directory.  Use --overwrite option to overwrite.') )


shpFilename = args.shpFilename ###'MapunitPolyExtended.shp'

# Write provenance
asset = AssetProvenance(GenericMetadata.MANIFEST_SECTION)
asset.name = 'soil_features'
asset.dcIdentifier = shpFilename
asset.dcSource = 'from hydroterre web service with GI' 
asset.dcTitle = 'GI with SSURGO soils data'
asset.dcPublisher = 'USDA'
asset.dcDescription = cmdline
asset.writeToMetadata(context)

# Write processing history
GenericMetadata.appendProcessingHistoryItem(context, cmdline)




