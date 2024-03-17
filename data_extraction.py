from PyPDF2 import PdfReader
import glob
import os
import re
import pandas as pd
import numpy as np
from natsort import index_natsorted


roughness_dict = {"sample_name": [], "Ra": [], "Rq": [], "Rz": []}

for name in glob.glob('roughness_values/*.pdf'):
    reader = PdfReader(name)
    text = reader.pages[0].extract_text()
    sample_name = os.path.basename(name).split('.')[0]
    Ra = float(re.search('Ra (.*)µm', text).group(1))
    Rq = float(re.search('Rq (.*)µm', text).group(1))
    Rz = float(re.search('Rz (.*)µm', text).group(1))
    roughness_dict['sample_name'].append(sample_name)
    roughness_dict['Ra'].append(Ra)
    roughness_dict['Rq'].append(Rq)
    roughness_dict['Rz'].append(Rz)

roughness_df = pd.DataFrame(roughness_dict)
roughness_df.sort_values(by=['sample_name'],
                         key=lambda x: np.argsort(
                             index_natsorted(roughness_df["sample_name"])),
                         inplace=True)

roughness_df.to_excel('data/roughness_values_all.xlsx', index=False)

roughness_avg_df = roughness_df.groupby('sample_name', as_index=False).mean()
roughness_avg_df.sort_values(by=['sample_name'],
                             key=lambda x: np.argsort(index_natsorted(
                                 roughness_avg_df["sample_name"])),
                             inplace=True)
roughness_avg_df.to_excel('data/roughness_values_avg.xlsx', index=False)
