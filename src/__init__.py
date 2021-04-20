"""
General imports the whole package uses
"""
import os

# Package dir is the general path your package uses
__PACKAGE_DIR__ = os.path.dirname(os.path.realpath(__file__))
# Path to Data folder
__DATA__ = os.path.join(__PACKAGE_DIR__, 'data')
# Path to VCF file
__VCF_FILE__ = os.path.join(__DATA__, 'NA12877_API_10.vcf')
# Path to Json Schema file
__SCHEMA__ = os.path.join(__DATA__, 'schema.json')
# Path to tests folder
__TESTS__ = os.path.join(__PACKAGE_DIR__, 'tests')