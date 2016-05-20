# -*- coding: utf-8 -*-

import pandas as pd
import os
from ddf_utils.str import to_concept_id
from ddf_utils.index import create_index_file

# configure file path
source = '../source/gapdata008 v6.xlsx'
out_dir = '../../'


if __name__ == '__main__':
    data001 = pd.read_excel(source, sheetname='Data & metadata')

    # entities
    area = data001['Area'].unique()
    area_id = list(map(to_concept_id, area))
    ent = pd.DataFrame([], columns=['area', 'name'])
    ent['area'] = area_id
    ent['name'] = area

    path = os.path.join(out_dir, 'ddf--entities--area.csv')
    ent.to_csv(path, index=False)

    # datapoints
    data001_dp_1 = data001[['Area', 'Year', 'Total Fertility Rate (TFR), also called Children per Woman']].copy()
    data001_dp_2 = data001[['Area', 'Year', 'TFR interpolated']].copy()

    data001_dp_1.columns = ['area', 'year', 'total_fertility_rate']
    data001_dp_2.columns = ['area', 'year', 'total_fertility_rate_interpolated']

    data001_dp_1['area'] = data001_dp_1['area'].map(to_concept_id)
    data001_dp_2['area'] = data001_dp_2['area'].map(to_concept_id)

    path1 = os.path.join(out_dir, 'ddf--datapoints--total_fertility_rate--by--area--year.csv')
    path2 = os.path.join(out_dir, 'ddf--datapoints--total_fertility_rate_interpolated--by--area--year.csv')

    data001_dp_1.dropna().sort_values(by=['area', 'year']).to_csv(path1, index=False)
    data001_dp_2.dropna().sort_values(by=['area', 'year']).to_csv(path2, index=False)

    # concept
    conc = ['total_fertility_rate', 'total_fertility_rate_interpolated', 'area', 'year', 'name']

    cdf = pd.DataFrame([], columns=['concept', 'name', 'concept_type'])
    cdf['concept'] = conc
    cdf['name'] = ['Total Fertility Rate (TFR), also called Children per Woman', 'TFR interpolated', 'Area', 'Year', 'Name']
    cdf['concept_type'] = ['measure', 'measure', 'entity_domain', 'time', 'string']

    path = os.path.join(out_dir, 'ddf--concepts.csv')
    cdf.to_csv(path, index=False)

    # index
    create_index_file(out_dir)

    print('Done.')
