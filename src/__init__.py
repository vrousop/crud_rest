"""
General imports the whole package uses
"""
import os

# Package dir is the general path your package uses
__PACKAGE_DIR__ = os.path.dirname(os.path.realpath(__file__))
# Other paths are relative to Package dir
__DATA__ = os.path.join(__PACKAGE_DIR__, 'data')

__VCF_FILE__ = os.path.join(__DATA__, 'NA12877_API_10.vcf')

__SCHEMA__ = os.path.join(__DATA__, 'schema.json')

__TESTS__ = os.path.join(__PACKAGE_DIR__, 'tests')