import pandas as pd


class VcfParser:
    """
    Class for parsing of VCF file
    """
    def __init__(self, vcf_path):
        self.vcf_path = vcf_path
        self.read()

    def read_header(self):
        # Read and store header for writing
        with open(self.vcf_path, 'r') as vcf_file:
            header = [l.split('\t') for l in vcf_file if l.startswith('##')]
        return header

    def read_content(self):
        # Read content data
        with open(self.vcf_path, 'r') as vcf_file:
            lines = [l.replace('\n', '').split('\t') for l in vcf_file if not l.startswith('##')]
        return pd.DataFrame(lines[1:], columns=lines[0])

    def read(self):
        self.header = self.read_header()
        self.df = self.read_content()
        self.df = self.df.rename(columns={'#CHROM': 'CHROM'}, inplace=False)

    def write(self):
        # Write header
        with open(self.vcf_path, 'w') as new_vcf:
            for h in self.header:
                new_vcf.write(h[0])

        # Append modified content
        self.df = self.df.rename(columns={'CHROM': '#CHROM'}, inplace=False)
        self.df.to_csv(self.vcf_path, mode='a', header=True, index=False, sep='\t')
        self.df = self.df.rename(columns={'#CHROM': 'CHROM'}, inplace=False)
