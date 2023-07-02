def boundaries(domain_name=''):
    if domain_name == 'Global':
        xlim = (0, 360)
        ylim = (-90, 90)
    elif domain_name == 'Tropics':
        xlim = (0, 360)
        ylim = (-30, 30)
    elif domain_name == 'NH Tropics':
        xlim = (0, 360)
        ylim = (0, 30)
    elif domain_name == 'SH Tropics':
        xlim = (0, 360)
        ylim = (-30, 0)
    elif domain_name == 'WP':
        xlim = (120, 180)
        ylim = (0, 30)
    elif domain_name == 'EP':
        xlim = (180, 260)
        ylim = (0, 30)
    elif domain_name == 'EP+NA':
        xlim = (180, 360)
        ylim = (0, 30)
    else:
        print('Warning: domain_name not valid')
        xlim = (0, 360)
        ylim = (-90, 90)

    return xlim, ylim

def patch_expr():
    exp_names = ['c96L33_am4p0_2010climo']

    amp = '1p5'
    
    lat = '-15.0'
    for lon in range(0, 320+1, 40):
        exp_names.append(f'c96L33_am4p0_2010climo_A{amp}.{lat}_{int(lon)}.0')
    lat = '-7.5'
    for lon in range(-20, 300+1, 40):
        exp_names.append(f'c96L33_am4p0_2010climo_A{amp}.{lat}_{int(lon)}.0')
    lat = '0.0'
    for lon in range(0, 320+1, 40):
        exp_names.append(f'c96L33_am4p0_2010climo_A{amp}.{lat}_{int(lon)}.0')
    lat = '7.5'
    for lon in range(-20, 300+1, 40):
        exp_names.append(f'c96L33_am4p0_2010climo_A{amp}.{lat}_{int(lon)}.0')
    lat = '15.0'
    for lon in range(0, 320+1, 40):
        exp_names.append(f'c96L33_am4p0_2010climo_A{amp}.{lat}_{int(lon)}.0')
            
    return exp_names