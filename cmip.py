def model_list():
    return sorted( set(models_high_res()) & set(models_cloud_feedback()) )

def models_high_res():
    """Return list of high-resolution (dx <= 100 km) models, according to https://esgf-node.llnl.gov/search/cmip6/"""

    return [
        'AWI-CM-1-1-MR',
        'BCC-CSM2-MR',
        'CAMS-CSM1-0',
        'CAS-ESM2-0',
        'CESM2',
        'CESM2-WACCM',
        'CMCC-CM2-HR4',
        'CMCC-CM2-SR5',
        'CMCC-ESM2',
        'CNRM-CM6-1-HR',
        'E3SM-1-0',
        'EC-Earth3',
        'EC-Earth3-Veg',
        'FGOALS-f3-L',
        'FIO-ESM-2-0',
        'GFDL-CM4',
        'GFDL-ESM4',
        'HadGEM3-GC31-MM',
        'INM-CM4-8',
        'INM-CM5-0',
        'MPI-ESM1-2-HR',
        'MRI-ESM2-0',
        'NorESM2-MM',
        'SAM0-UNICON',
        'TaiESM1',
        ]

def models_cloud_feedback():
    """Return list of models with well-defined global mean cloud feedback (Gregory plot r^2 > 0.3)"""

    return [
        'ACCESS-CM2',
        'ACCESS-ESM1-5',
        'AWI-CM-1-1-MR',
        'BCC-CSM2-MR',
        'BCC-ESM1',
        'CESM2',
        'CESM2-WACCM',
        'CMCC-CM2-SR5',
        'CNRM-CM6-1',
        'CNRM-ESM2-1',
        'CanESM5',
        'E3SM-1-0',
        'EC-Earth3-Veg',
        'FGOALS-g3',
        'GFDL-CM4',
        'GFDL-ESM4',
        'GISS-E2-1-H',
        'IPSL-CM6A-LR',
        'KIOST-ESM',
        'MPI-ESM1-2-HR',
        'MPI-ESM1-2-LR',
        'MRI-ESM2-0',
        'NorCPM1',
        'SAM0-UNICON',
        'TaiESM1',
        'UKESM1-0-LL',
        ]

if __name__ == '__main__':
    print(model_list())