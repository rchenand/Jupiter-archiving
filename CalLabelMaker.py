from astropy.io import fits
from datetime import date
from datetime import datetime
import glob
import os
import time
from stat import *


#Script for calibrated images of Jupiter meaning primary image and ancillary cmap, mu
#note: fits files should be unzipped or astropy.io will not like them

#checking for correct working directory
if 'data_calibrated' in os.getcwd():
    print('Found Folder. Syntax is fine. Making labels now...')
   
    for cal_fname in glob.glob('/home/rchenand/jup_supp.naoj-hawaii_comics/data_calibrated/2013/*/*fits*'):

        fname = cal_fname.split('/')[-1]            #basename of the file 
        new_label = open(cal_fname + '.xml', 'w')
    
        #template selection
        if 'cmap' in cal_fname or 'mu' in cal_fname: # for ancillary files
            template = open('/home/rchenand/Templates-COMICS/Ground-Based_FITS-ancillary.xml')
        else:
            template = open('/home/rchenand/Templates-COMICS/Ground-Based_FITS-calibrated.xml')
        
        #fits file reading and label making
        hdul = fits.open(cal_fname)
        hdr = hdul[0].header
        img = hdul[0].data
        
        for line in template:
            if '$' not in line:
                new_label.write(line)                           #line is written from template
            else:
                var = line[line.find('$')+1:line.rfind('$')]    #line contains variable
                if var == 'PRODUCT_ID':
                    #product LID
                    new_label.write(line.replace('$' + var + '$', 'data_calibrated:' + fname.lower()))
                elif var == 'PRODUCT_DESCRIPTION':
                    #product descriptions, mu/cmap
                    elif 'mu' in fname:
                        new_label.write(line.replace('$' + var + '$', 'Ground Based FITS, emission angle adjustment for cylindrical map.'))
                    elif 'cmap' in fname:
                        new_label.write(line.replace('$' + var + '$', 'Ground Based FITS, cylindrical map projection.'))
                    else:
                        new_label.write(line.replace('$' + var + '$', 'Ground Based FITS, derived data file.'))
                elif var == 'MODIFICATION_DATE':
                    #modification date
                    new_label.write(line.replace('$' + var + '$', str(date.today())))
                elif var == 'START_TIME':
                    #start time of observation
                    print(cal_fname) #time segment needs to be to 4 seconds, ensuring that
                    if len(hdr['UT']) == 9:
                        s_time = hdr['DATE-OBS']+'T'+hdr['UT']+'0000'+'Z'
                    if len(hdr['UT']) == 10:
                        s_time = hdr['DATE-OBS']+'T'+hdr['UT']+'000'+'Z'
                    elif len(hdr['UT']) == 11:
                        s_time = hdr['DATE-OBS']+'T'+hdr['UT']+'00'+'Z'
                    elif len(hdr['UT']) == 12:
                        s_time = hdr['DATE-OBS']+'T'+hdr['UT']+'0'+'Z'
                    elif len(hdr['UT']) >= 14:
                        xting = hdr['UT']
                        s_time = hdr['DATE-OBS']+'T'+ xting[:13]+'Z'
                    else:
                        s_time = hdr['DATE-OBS']+'T'+hdr['UT']+'Z'
                    new_label.write(line.replace('$' + var + '$', s_time))
                elif var == 'PROCESSING_DESCRIPTION':
                    #processing level desc., /mu/cmap
                    if 'cmap' in fname:
                        new_label.write(line.replace('$' + var + '$', 'Projection onto linear cylindrical coordinate system longitude in System III along abscissa and planetocentric latitude in the ordinate'))
                    elif 'mu' in fname:
                        new_label.write(line.replace('$' + var + '$', 'Cosine of the emission angle for each point on cylindrical map from the angle between the local zenith and direction of the Earth-based observer'))

                    else:
                        new_label.write(line.replace('$' + var + '$', 'Derived results from calibrated data products.'))
                elif var == 'FILE_NAME':
                    #file name
                    new_label.write(line.replace('$' + var + '$', fname))
                elif var == 'PRODUCT_CREATION_TIME':
                    #creation time 
                    #NOTE: This value can be taken from FITS file or in a crunch using today/now time
    
                   # today's date/time
                    c_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.0000Z")
                    new_label.write(line.replace('$' + var + '$', c_time))
                elif var == 'FILE_SIZE':
                    #file size
                    new_label.write(line.replace('$' + var + '$', str(os.stat(cal_fname).st_size)))
                elif var == 'BYTES':
                    #header length in bytes
                    size_offset = ((len(hdr)+1) // 36) * 2880
                    new_label.write(line.replace('$' + var + '$', str(size_offset)))
                elif var == 'LINE_SAMPLES':
                    #elements in axis 1
                    new_label.write(line.replace('$' + var + '$', str(hdr['NAXIS1'])))
                elif var == 'LINES':
                    #elements in axis 2
                    new_label.write(line.replace('$' + var + '$', str(hdr['NAXIS2'])))
        new_label.close()
        template.close()

else:
    print("COULD NOT LOCATE data_calibrated folder")
