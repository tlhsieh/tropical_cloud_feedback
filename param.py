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