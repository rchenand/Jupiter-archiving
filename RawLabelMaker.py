from astropy.io import fits
from datetime import date
import glob
import os
from stat import *

#checking for working directory
if 'data_raw' in os.getcwd():
    print('ok')
    for raw_fname in glob.glob('/home/rchenand/jup_supp.naoj-hawaii_comics/data_raw/*/*/*fits*'):
    
        #new PDS4 label file
        new_label = open(raw_fname + '.xml', 'w')
      
        template = open('/home/rchenand/Templates-COMICS/Ground-Based_FITS-raw.xml')
      
        #file basename
        fname = raw_fname.split('/')[-1]
    
        #make sure file ends in .fits
        hdul = fits.open(raw_fname)
        hdr = hdul[0].header
        img = hdul[0].data
    
        for line in template:
            if '$' not in line:
                new_label.write(line)
            else:
                var = line[line.find('$')+1:line.rfind('$')]
                if var == 'PRODUCT_ID': # if reads in 'product_id' from template
                    new_label.write(line.replace('$' + var + '$', 'data_raw:' + fname.lower()))
                elif var == 'MODIFICATION_DATE':
                    new_label.write(line.replace('$' + var + '$', str(date.today())))
                elif var == 'START_TIME':
                    if len(hdr['UT']) == 9:
                        s_time = hdr['DATE-OBS']+'T'+hdr['UT']+'0000'+'Z'
                    elif len(hdr['UT']) == 10:
                        s_time = hdr['DATE-OBS']+'T'+hdr['UT']+'000'+'Z'
                    elif len(hdr['UT']) == 11:
                        s_time = hdr['DATE-OBS']+'T'+hdr['UT']+'00'+'Z'
                    elif len(hdr['UT']) == 12:
                        s_time = hdr['DATE-OBS']+'T'+hdr['UT']+'0'+'Z'
                    elif len(hdr['UT']) >= 14:
                        xting = hdr['UT']
                        s_time = hdr['DATE-OBS']+'T'+hdr['UT']+'Z'
                    else:
                        s_time = hdr['DATE-OBS']+'T'+ hdr['UT']+'Z'
                    new_label.write(line.replace('$' + var + '$', s_time))
                elif var == 'TARGET_NAME':
                    if hdr['OBJECT'] == 'jupiter' or hdr['OBJECT'] == 'Jupiter' or hdr['OBJECT'] == 'DARK' or hdr['OBJECT'] == 'FLAT':
                        new_label.write(line.replace('$' + var + '$', 'Jupiter'))
                    else:
                        new_label.write(line.replace('$' + var + '$', hdr['OBJECT']))
                elif var == 'TARGET_TYPE':
                    if hdr['OBJECT'] == 'jupiter' or hdr['OBJECT'] == 'Jupiter' or hdr['OBJECT'] == 'DARK' or hdr['OBJECT'] == 'FLAT':
                        new_label.write(line.replace('$' + var + '$', 'Planet'))
                    else:
                        new_label.write(line.replace('$' + var + '$', 'Star'))
                elif var == 'LID_REF':
                    if hdr['OBJECT'] == 'jupiter' or hdr['OBJECT'] == 'Jupiter' or hdr['OBJECT'] == 'DARK' or hdr['OBJECT'] == 'FLAT':
                        new_label.write(line.replace('$' + var + '$', 'planet.jupiter'))
                    else:
                        new_label.write(line.replace('$' + var + '$', 'star.'+hdr['OBJECT']))
                elif var == 'FILE_NAME':
                    new_label.write(line.replace('$' + var + '$', fname))
                elif var == 'PRODUCT_CREATION_TIME':
                    c_time = s_time
                    new_label.write(line.replace('$' + var + '$', c_time))
                elif var == 'FILE_SIZE':
                    new_label.write(line.replace('$' + var + '$', str(os.stat(raw_fname).st_size)))
                elif var == 'BYTES':
                    size_offset = ((len(hdr)+1) // 36) * 2880
                    new_label.write(line.replace('$' + var + '$', str(size_offset)))
                elif var == 'TARGET_NAME2':
                    if hdr['OBJECT'] == 'jupiter' or hdr['OBJECT'] == 'Jupiter' or hdr['OBJECT'] == 'DARK' or hdr['OBJECT'] == 'FLAT':
                        new_label.write(line.replace('$' + var + '$', 'Jupiter\'s atmosphere'))
                    else:
                        new_label.write(line.replace('$' + var + '$', hdr['OBJECT']))
                elif var == 'LINE_SAMPLES':
                    new_label.write(line.replace('$' + var + '$', str(hdr['NAXIS1'])))
                elif var == 'LINES':
                    new_label.write(line.replace('$' + var + '$', str(hdr['NAXIS2'])))
        new_label.close()
        template.close()

else:
    print('CANNOT FIND data_raw folder')
