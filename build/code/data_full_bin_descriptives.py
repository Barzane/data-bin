# -*- coding: utf-8 -*-

import cPickle, numpy, math

import competitive_dummy

def weighted_avg_and_std(values, weights):

#        http://stackoverflow.com/questions/2413522/weighted-standard-deviation-in-numpy
    
    average = numpy.average(values, weights=weights)
    variance = numpy.average((values - average) ** 2, weights=weights)
    
    return (average, math.sqrt(variance))
        
def compute(monopoly_dict, competitive_dict, test_run):

    src = '..\\output\\data_full.bin'
    
    try:
        
        f = open(src, 'rb')
        data = cPickle.load(f)
        f.close()
        
    except IOError:
        
        print
        print 'file not found', src    
    
    print
    print 'descriptives:'
    
    print '\t', src
    
    southwest_routes = {}
    
    year_list = []
    carrier_list = []
    route_list = []
    airport_list = []
    
    pax = {}
    southwest_pax = {}
    
    data_1999_2013 = {}

    pax_list = []
    distance_list = []
    pax_list_legacy = []
    distance_list_legacy = []
    pax_list_1999 = []
    distance_list_1999 = []
    pax_list_2013 = []
    distance_list_2013 = []
    pax_list_monop = []
    distance_list_monop = []
    pax_list_comp = []
    distance_list_comp = []
    
    pax_hhi = {}
    hhi = {}
    pax_hhi_legacy = {}
    hhi_legacy = {}
    pax_hhi_1999 = {}
    hhi_1999 = {}
    pax_hhi_2013 = {}
    hhi_2013 = {}
    pax_hhi_monop = {}
    hhi_monop = {}
    pax_hhi_comp = {}
    hhi_comp = {}
    
    temp = {}
    temp_legacy = {}
    temp_1999 = {}
    temp_2013 = {}
    temp_monop = {}
    temp_comp = {}
    
    gdp = {}
    gdp_legacy = {}
    gdp_1999 = {}
    gdp_2013 = {}
    gdp_monop = {}
    gdp_comp = {}

    seats = {}
    seats_legacy = {}
    seats_1999 = {}
    seats_2013 = {}
    seats_monop = {}
    seats_comp = {}
    
    legacy = ['AA', 'CO', 'DL', 'NW', 'TW', 'UA', 'US']
    
    for key in data:
        
#        print data[key]['pax'], data[key]['T100pax'], data[key]['T100seats']
#        print float(data[key]['T100pax']) / data[key]['pax']
#        print float(data[key]['T100pax']) / data[key]['T100seats']
#        raw_input()        
        
        key_split = key.split('_')
        
        origin = key_split[0]
        destination = key_split[1]
        carrier = key_split[2]
        year = int(key_split[3])
        quarter = int(key_split[4]) 
        
        route = origin + '_' + destination
        
        if year not in southwest_routes:
            
            southwest_routes[year] = {}
            year_list.append(year)
            pax[year] = {}
            southwest_pax[year] = {}
            
        if quarter not in southwest_routes[year]:
            
            southwest_routes[year][quarter] = 0
            pax[year][quarter] = 0
            southwest_pax[year][quarter] = 0
        
        pax[year][quarter] += data[key]['pax']
        
        if quarter not in pax_hhi:
            
            pax_hhi[quarter] = []
            pax_hhi_legacy[quarter] = []
            pax_hhi_1999[quarter] = []
            pax_hhi_2013[quarter] = []
            pax_hhi_monop[quarter] = []
            pax_hhi_comp[quarter] = []
            
        if quarter not in hhi:
            
            hhi[quarter] = []
            hhi_legacy[quarter] = []
            hhi_1999[quarter] = []
            hhi_2013[quarter] = []
            hhi_monop[quarter] = []
            hhi_comp[quarter] = []
            
            temp[quarter] = []
            temp_legacy[quarter] = []
            temp_1999[quarter] = []
            temp_2013[quarter] = []
            temp_monop[quarter] = []
            temp_comp[quarter] = []
            
            gdp[quarter] = []
            gdp_legacy[quarter] = []
            gdp_1999[quarter] = []
            gdp_2013[quarter] = []
            gdp_monop[quarter] = []
            gdp_comp[quarter] = []
            
            seats[quarter] = []
            seats_legacy[quarter] = []
            seats_1999[quarter] = []
            seats_2013[quarter] = []
            seats_monop[quarter] = []
            seats_comp[quarter] = []
        
        if carrier == 'WN':
            
            southwest_routes[year][quarter] += 1
            southwest_pax[year][quarter] += data[key]['pax']

        if year >= 1999:
            
            data_1999_2013[key] = data[key]

        if carrier not in carrier_list:
            
            carrier_list.append(carrier)
            
        if route not in route_list:
            
            route_list.append(route)
            
        if origin not in airport_list:
            
            airport_list.append(origin)
            
        if destination not in airport_list:
            
            airport_list.append(destination)

        pax_list.append(data[key]['pax'])
        distance_list.append(data[key]['distance'])
        
        pax_hhi[quarter].append(data[key]['pax'])
        hhi[quarter].append(data[key]['hhiDB1B'])        
        temp[quarter].append(data[key]['absTempDiff'])        
        gdp[quarter].append(data[key]['meanGDPperCapita'])        
        seats[quarter].append(data[key]['T100seats'])
        
        if carrier in legacy:
            
            pax_list_legacy.append(data[key]['pax'])
            distance_list_legacy.append(data[key]['distance'])
            
            pax_hhi_legacy[quarter].append(data[key]['pax'])
            hhi_legacy[quarter].append(data[key]['hhiDB1B'])            
            temp_legacy[quarter].append(data[key]['absTempDiff'])            
            gdp_legacy[quarter].append(data[key]['meanGDPperCapita'])            
            seats_legacy[quarter].append(data[key]['T100seats'])
            
        if year == 1999:
            
            pax_list_1999.append(data[key]['pax'])
            distance_list_1999.append(data[key]['distance'])
            
            pax_hhi_1999[quarter].append(data[key]['pax'])
            hhi_1999[quarter].append(data[key]['hhiDB1B'])            
            temp_1999[quarter].append(data[key]['absTempDiff'])            
            gdp_1999[quarter].append(data[key]['meanGDPperCapita'])            
            seats_1999[quarter].append(data[key]['T100seats'])
            
        if year == 2013:
            
            pax_list_2013.append(data[key]['pax'])
            distance_list_2013.append(data[key]['distance'])
            
            pax_hhi_2013[quarter].append(data[key]['pax'])
            hhi_2013[quarter].append(data[key]['hhiDB1B'])            
            temp_2013[quarter].append(data[key]['absTempDiff'])            
            gdp_2013[quarter].append(data[key]['meanGDPperCapita'])
            seats_2013[quarter].append(data[key]['T100seats'])

        monopoly = monopoly_dict[str(year) + '_' + str(quarter)][route]
        competitive = competitive_dict[str(year) + '_' + str(quarter)][route]
        
        if monopoly:
            
            pax_list_monop.append(data[key]['pax'])
            distance_list_monop.append(data[key]['distance'])
            
            pax_hhi_monop[quarter].append(data[key]['pax'])
            hhi_monop[quarter].append(data[key]['hhiDB1B'])
            temp_monop[quarter].append(data[key]['absTempDiff'])
            gdp_monop[quarter].append(data[key]['meanGDPperCapita'])
            seats_monop[quarter].append(data[key]['T100seats'])

        if competitive:
            
            pax_list_comp.append(data[key]['pax'])
            distance_list_comp.append(data[key]['distance'])
            
            pax_hhi_comp[quarter].append(data[key]['pax'])
            hhi_comp[quarter].append(data[key]['hhiDB1B'])
            temp_comp[quarter].append(data[key]['absTempDiff'])
            gdp_comp[quarter].append(data[key]['meanGDPperCapita'])
            seats_comp[quarter].append(data[key]['T100seats'])

    year_list.sort()
    carrier_list.sort()
    route_list.sort()
    airport_list.sort()
    
    print    
    print 'number of Southwest routes by year-quarter:'
    
    for year in year_list:
        
        print '\t', year, southwest_routes[year]    
    
    southwest_route_list = []

    for year in southwest_routes:
        
        for quarter in southwest_routes[year]:
            
            item = southwest_routes[year][quarter]
            
            if item != 0:
                
                southwest_route_list.append(item)
    
    print
    print 'minimum number of Southwest routes by year-quarter:'
    
    print '\t', min(southwest_route_list)    
    
    print
    print 'maximum number of Southwest routes by year-quarter:'
    
    print '\t', max(southwest_route_list) 
        
    print
    print 'number of Southwest passengers by year-quarter:'
    
    for year in year_list:
        
        print '\t', year, southwest_pax[year]
    
    southwest_pax_percentage = []
    
    for year in southwest_routes:
        
        for quarter in southwest_routes[year]:
            
            item = 100 * float(southwest_pax[year][quarter]) / float(pax[year][quarter])
            
            if item != 0.0:
                
                southwest_pax_percentage.append(item)
    
    print
    print 'minimum % of Southwest pax (to total) by year-quarter:'
    
    print '\t', min(southwest_pax_percentage)    
    
    print
    print 'maximum % of Southwest pax (to total) by year-quarter:'
    
    print '\t', max(southwest_pax_percentage) 
    
    print
    print 'retaining years >= 1999'
    
    data = data_1999_2013
    
    del data_1999_2013
    
    print
    print 'number of observations (route-carrier-quarters):'
    
    print '\t', len(data)
    
    print
    print 'number of carriers:'
    
    print '\t', len(carrier_list)
    
#    print
#    print carrier_list
    
    print
    print 'number of routes:'
    
    print '\t', len(route_list)
    
    print
    print 'number of airports:'
    
    print '\t', len(airport_list)
    
#    print
#    print airport_list
    
    def print_output(title, full_sample, legacy, year_1999, year_2013, quarterly, monopoly, competitive, test_run):
        
        if quarterly[0]:
            
            loop = quarterly[2]
            
        else:
            
            loop = quarterly[1]
        
        print
        print '[full sample] ' + title
        
        for quarter in loop:
            
            print '\t' + str(quarter), weighted_avg_and_std(full_sample[0][quarter], full_sample[1][quarter])

        print
        print '[legacy] ' + title
        
        for quarter in loop:
            
            print '\t' + str(quarter), weighted_avg_and_std(legacy[0][quarter], legacy[1][quarter])
        
        if not test_run:
            
            print
            print '[1999] ' + title
            
            for quarter in loop:
                
                print '\t' + str(quarter), weighted_avg_and_std(year_1999[0][quarter], year_1999[1][quarter])
            
        print
        print '[2013] ' + title
        
        for quarter in loop:
            
            print '\t' + str(quarter), weighted_avg_and_std(year_2013[0][quarter], year_2013[1][quarter])
        
        print
        print '[monopoly] ' + title
        
        for quarter in loop:
            
            print '\t' + str(quarter), weighted_avg_and_std(monopoly[0][quarter], monopoly[1][quarter])
        
        print

        print '[competitive] ' + title
        
        for quarter in loop:
            
            print '\t' + str(quarter), weighted_avg_and_std(competitive[0][quarter], competitive[1][quarter])
        
        return None
    
    print_options = {}
    print_options['title'] = 'pax weighted mean distance (miles) and biased std. dev.:'
    print_options['full_sample'] = ({'': distance_list}, {'': pax_list})
    print_options['legacy'] = ({'': distance_list_legacy}, {'': pax_list_legacy})
    print_options['year_1999'] = ({'': distance_list_1999}, {'': pax_list_1999})  
    print_options['year_2013'] = ({'': distance_list_2013}, {'': pax_list_2013})
    print_options['quarterly'] = (False, [''], hhi.keys())
    print_options['monopoly'] = ({'': distance_list_monop}, {'': pax_list_monop})
    print_options['competitive'] = ({'': distance_list_comp}, {'': pax_list_comp})
    print_options['test_run'] = test_run
    
    print_output(**print_options)
    
    print_options = {}
    print_options['title'] = 'pax weighted mean HHI and biased std. dev.:'
    print_options['full_sample'] = (hhi, pax_hhi)
    print_options['legacy'] = (hhi_legacy, pax_hhi_legacy)
    print_options['year_1999'] = (hhi_1999, pax_hhi_1999)       
    print_options['year_2013'] = (hhi_2013, pax_hhi_2013)
    print_options['quarterly'] = (True, [''], hhi.keys())
    print_options['monopoly'] = (hhi_monop, pax_hhi_monop)
    print_options['competitive'] = (hhi_comp, pax_hhi_comp)
    print_options['test_run'] = test_run
    
    print_output(**print_options)
    
    print_options = {}
    print_options['title'] = 'pax weighted mean abs. temp. diff. and biased std. dev.:'
    print_options['full_sample'] = (temp, pax_hhi)
    print_options['legacy'] = (temp_legacy, pax_hhi_legacy)
    print_options['year_1999'] = (temp_1999, pax_hhi_1999)    
    print_options['year_2013'] = (temp_2013, pax_hhi_2013)
    print_options['quarterly'] = (True, [''], hhi.keys())
    print_options['monopoly'] = (temp_monop, pax_hhi_monop)
    print_options['competitive'] = (temp_comp, pax_hhi_comp)
    print_options['test_run'] = test_run
    
    print_output(**print_options)

    pax_gdp_no_missing = {}
    gdp_no_missing = {}
    pax_gdp_legacy_no_missing = {}
    gdp_legacy_no_missing = {}
    pax_gdp_1999_no_missing = {}
    gdp_1999_no_missing = {}
    pax_gdp_2013_no_missing = {}
    gdp_2013_no_missing = {}
    pax_gdp_monop_no_missing = {}
    gdp_monop_no_missing = {}
    pax_gdp_comp_no_missing = {}
    gdp_comp_no_missing = {}
    
#    GDP per capita can have missing values ('NA')    
    
    for quarter in hhi:
        
        pax_gdp_no_missing[quarter] = []
        gdp_no_missing[quarter] = []
        
        pax_gdp_legacy_no_missing[quarter] = []
        gdp_legacy_no_missing[quarter] = []
        
        pax_gdp_1999_no_missing[quarter] = []
        gdp_1999_no_missing[quarter] = []
        
        pax_gdp_2013_no_missing[quarter] = []
        gdp_2013_no_missing[quarter] = []
        
        pax_gdp_monop_no_missing[quarter] = []
        gdp_monop_no_missing[quarter] = []
        
        pax_gdp_comp_no_missing[quarter] = []
        gdp_comp_no_missing[quarter] = []
        
        if len(pax_hhi[quarter]) != len(gdp[quarter]):
            
            raise Exception('list lengths are not the same')
            
        if len(pax_hhi_legacy[quarter]) != len(gdp_legacy[quarter]):
            
            raise Exception('list lengths are not the same')
            
        if len(pax_hhi_1999[quarter]) != len(gdp_1999[quarter]):
            
            raise Exception('list lengths are not the same')
            
        if len(pax_hhi_2013[quarter]) != len(gdp_2013[quarter]):
            
            raise Exception('list lengths are not the same')
            
        if len(pax_hhi_monop[quarter]) != len(gdp_monop[quarter]):
            
            raise Exception('list lengths are not the same')
            
        if len(pax_hhi_comp[quarter]) != len(gdp_comp[quarter]):
            
            raise Exception('list lengths are not the same')
        
        for item in range(len(pax_hhi[quarter])):
            
            if gdp[quarter][item] != 'NA':
                
                pax_gdp_no_missing[quarter].append(pax_hhi[quarter][item])
                gdp_no_missing[quarter].append(gdp[quarter][item])
                
        for item in range(len(pax_hhi_legacy[quarter])):
            
            if gdp_legacy[quarter][item] != 'NA':
                
                pax_gdp_legacy_no_missing[quarter].append(pax_hhi_legacy[quarter][item])
                gdp_legacy_no_missing[quarter].append(gdp_legacy[quarter][item])
                
        for item in range(len(pax_hhi_1999[quarter])):
            
            if gdp_1999[quarter][item] != 'NA':
                
                pax_gdp_1999_no_missing[quarter].append(pax_hhi_1999[quarter][item])
                gdp_1999_no_missing[quarter].append(gdp_1999[quarter][item])
                
        for item in range(len(pax_hhi_2013[quarter])):
            
            if gdp_2013[quarter][item] != 'NA':
                
                pax_gdp_2013_no_missing[quarter].append(pax_hhi_2013[quarter][item])
                gdp_2013_no_missing[quarter].append(gdp_2013[quarter][item])
                
        for item in range(len(pax_hhi_monop[quarter])):
            
            if gdp_monop[quarter][item] != 'NA':
                
                pax_gdp_monop_no_missing[quarter].append(pax_hhi_monop[quarter][item])
                gdp_monop_no_missing[quarter].append(gdp_monop[quarter][item])
                
        for item in range(len(pax_hhi_comp[quarter])):
            
            if gdp_comp[quarter][item] != 'NA':
                
                pax_gdp_comp_no_missing[quarter].append(pax_hhi_comp[quarter][item])
                gdp_comp_no_missing[quarter].append(gdp_comp[quarter][item])

    print_options = {}
    print_options['title'] = 'pax weighted mean (mean) GDP per capita and biased std. dev.:'
    print_options['full_sample'] = (gdp_no_missing, pax_gdp_no_missing)
    print_options['legacy'] = (gdp_legacy_no_missing, pax_gdp_legacy_no_missing)
    print_options['year_1999'] = (gdp_1999_no_missing, pax_gdp_1999_no_missing)
    print_options['year_2013'] = (gdp_2013_no_missing, pax_gdp_2013_no_missing)
    print_options['quarterly'] = (True, [''], hhi.keys())
    print_options['monopoly'] = (gdp_monop_no_missing, pax_gdp_monop_no_missing)
    print_options['competitive'] = (gdp_comp_no_missing, pax_gdp_comp_no_missing)
    print_options['test_run'] = test_run
    
    print_output(**print_options)

    print_options = {}
    print_options['title'] = 'pax mean and biased std. dev. [unweighted]:'
    print_options['full_sample'] = (pax_hhi, dict([(q, list(numpy.ones(len(pax_hhi[q])))) for q in hhi.keys()]))
    print_options['legacy'] = (pax_hhi_legacy, dict([(q, list(numpy.ones(len(pax_hhi_legacy[q])))) for q in hhi.keys()]))
    print_options['year_1999'] = (pax_hhi_1999, dict([(q, list(numpy.ones(len(pax_hhi_1999[q])))) for q in hhi.keys()]))
    print_options['year_2013'] = (pax_hhi_2013, dict([(q, list(numpy.ones(len(pax_hhi_2013[q])))) for q in hhi.keys()]))
    print_options['quarterly'] = (True, [''], hhi.keys())
    print_options['monopoly'] = (pax_hhi_monop, dict([(q, list(numpy.ones(len(pax_hhi_monop[q])))) for q in hhi.keys()]))
    print_options['competitive'] = (pax_hhi_comp, dict([(q, list(numpy.ones(len(pax_hhi_comp[q])))) for q in hhi.keys()]))
    print_options['test_run'] = test_run
    
    print_output(**print_options)
    
    print_options = {}
    print_options['title'] = 'pax weighted mean T-100 seats and biased std. dev. [unweighted]:'
    print_options['full_sample'] = (seats, dict([(q, list(numpy.ones(len(seats[q])))) for q in hhi.keys()]))
    print_options['legacy'] = (seats_legacy, dict([(q, list(numpy.ones(len(seats_legacy[q])))) for q in hhi.keys()]))
    print_options['year_1999'] = (seats_1999, dict([(q, list(numpy.ones(len(seats_1999[q])))) for q in hhi.keys()]))
    print_options['year_2013'] = (seats_2013, dict([(q, list(numpy.ones(len(seats_2013[q])))) for q in hhi.keys()]))
    print_options['quarterly'] = (True, [''], hhi.keys())
    print_options['monopoly'] = (seats_monop, dict([(q, list(numpy.ones(len(seats_monop[q])))) for q in hhi.keys()]))
    print_options['competitive'] = (seats_comp, dict([(q, list(numpy.ones(len(seats_comp[q])))) for q in hhi.keys()]))
    print_options['test_run'] = test_run
    
    print_output(**print_options)    
    
    return None

def build(src_data, year, quarter, monopoly_dict, competitive_dict, test_run):
    
    monopoly_dict[str(year) + '_' + str(quarter)] = competitive_dummy.add_dummies(year, quarter, print_descriptives=True)[0]
    competitive_dict[str(year) + '_' + str(quarter)] = competitive_dummy.add_dummies(year, quarter)[1]
    
    return monopoly_dict, competitive_dict

def wrapper(test_run, test_periods, full_periods, security = None, security_max = None):

    print 'results for text and table of summary statistics'

    monopoly_dict = {}
    competitive_dict = {}

    if test_run:
        
        year_list = test_periods[0]
        quarter_list = test_periods[1]
        
    else:
                
        year_list = full_periods[0]
        quarter_list = full_periods[1]    
    
    for year in year_list:
        for quarter in quarter_list:

            src_data = '..\\output\\data_' + str(year) + '_' + str(quarter) + '.bin'
            
            try:
                            
                monopoly_dict, competitive_dict = build(src_data, year, quarter, monopoly_dict, competitive_dict, test_run)
                
            except IOError:

                raise IOError('requested data unavailable: year ' + str(year) + ', quarter ' + str(quarter))

    compute(monopoly_dict, competitive_dict, test_run)
    
    return None
    