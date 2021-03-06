#!/usr/bin/env python

import os
import argparse
import pymatgen as mp

def make_input(potcar_path, amobt_path, scripts_path, id = 'noid',  GEOM = False, SELF = False, NSELF = False, NSELF_AMOBT = False, 
DIEL = False, PHONON = False, DEFORM = False, AMOBT = False, SOC = False, computer = 'partita'):
	mp_api_key = 'fDJKEZpxSyvsXdCt'
	with open('MIKECAR','w') as input:
		input.write('EMAIL = alireza@wustl.edu \n')
		input.write('MP_API_KEY = ' + mp_api_key + ' \n')
		input.write('JOB_NAME = See_Folder \n')
		input.write('COMP_NAME = ' + id + ' \n')
		input.write('%s %s \n' % ('GEOM =', GEOM))
		input.write('%s %s \n' % ('SELF =', SELF))
		input.write('%s %s \n' % ('NSELF =', NSELF))
		input.write('%s %s \n' % ('NSELF_AMOBT =', NSELF_AMOBT))
		input.write('%s %s \n' % ('DIEL =', DIEL))
		input.write('%s %s \n' % ('PHONON =', PHONON))
		api = mp.MPRester(mp_api_key)
		if ('mp-' in id) or ('mvc-' in id):
			structure = api.get_structure_by_material_id(id)
			structure.to(filename="POSCAR")
			with open('POSCAR','r') as poscar:
				counter = 0
				natoms = 0
				for line in poscar:
					counter += 1
					if counter == 7:
						for i in line.split():
							natoms += int(i)
			os.system('rm POSCAR')
			if natoms < 10:
				input.write('DIM = 2x2x2 \n')
			else:
				input.write('DIM = 1x1x1 \n')
		else:
			input.write('DIM = 1x1x1 \n')
		input.write('%s %s \n' % ('DEFORM =', DEFORM))
		input.write('RANGE = -5,5 \n')
		input.write('POSCAR = default \n')
		input.write('INCAR = default \n')
		input.write('%s %s \n' % ('AMOBT =', AMOBT))
		input.write('%s %s \n' % ('SOC =', SOC))	
		input.write('%s %s \n' % ('COMPUTER =', computer))	
		input.write('%s %s \n' % ('AMOBT_PATH =', amobt_path)) 
		input.write('%s %s \n' % ('SCRIPTS_PATH =', scripts_path))
		input.write('%s %s \n' % ('POTCAR_PATH =', potcar_path))

def run_dekode_for(materials_list, potcar_path, amobt_path, scripts_path, GEOM = False, SELF = False, NSELF = False, NSELF_AMOBT = 
False, DIEL = False, PHONON = False, DEFORM = False, AMOBT = False, SOC = False, computer = 'partita'):
	if SOC:
		if not os.path.exists('SOC'):
			os.system('mkdir SOC')
		os.chdir('SOC')
	for id in materials_list:
		if not os.path.exists(id):
			os.system('mkdir ' + id) 
                	if not os.path.exists('dekode.py'):
                	        os.system('%s %s%s %s' % ('cp', scripts_path, 'dekode.py', id))
                	else:
                	        os.system('cp dekode.py ' + id)
                	if not os.path.exists(computer + '.sh'):
                	        os.system('%s %s%s %s' % ('cp', scripts_path, computer + '.sh', id))
                	else:
                	        os.system('cp ' + computer + '.sh ' + id)
                	if not os.path.exists('vasp-*'):
                	        os.system('cp ~/vasp-ib2.csh ' + id)
                	else:
                	        os.system('cp vasp* ' + id)
			os.chdir(id)
			make_input(potcar_path, amobt_path, scripts_path, id, GEOM, SELF, NSELF, NSELF_AMOBT, DIEL, PHONON, DEFORM, AMOBT, SOC, computer)
			os.system('rm python_job.*')
			os.system('qsub partita.sh')
			os.chdir('../')

if __name__ == "__main__":
	
	# The following are the first 9 n-type TCO's
	amobt_path = '/research-projects/partita/faghaniniaa/current_jobs/carrier_scattering/VERSIONS/latest_aMoBT/'
	scripts_path = '~/dekode/'
	potcar_path = '/cluster/caml/vasp-pot/PBE/'

	list = [
	'mp-628643',
	'mp-605863',
	'mp-568088'	# Yb14MnSb11
	]
	SOC = False

	parser = argparse.ArgumentParser()
	parser.add_argument("-pa","--mp_id", help="The Materials Project ID", required = False)
	args = parser.parse_args()

	run_dekode_for(list, potcar_path, amobt_path, scripts_path, GEOM = True, SELF = True, NSELF = True, \
	NSELF_AMOBT = True, DIEL = True, PHONON = True, DEFORM = True, AMOBT = True, SOC = False, computer = 'partita')

#	run_dekode_for(some_exp_TCOs, potcar_path, amobt_path, scripts_path, GEOM = False, SELF = False, NSELF = False, \
#	NSELF_AMOBT = True, DIEL = True, PHONON = True, DEFORM = True, AMOBT = True, SOC = False, computer = 'partita')

# Just aMoBT:
#	run_dekode_for(['mp-866132'], potcar_path, amobt_path, scripts_path, GEOM = False, SELF = False, NSELF = False, \
#	NSELF_AMOBT = False, DIEL = False, PHONON = False, DEFORM = False, AMOBT = True, SOC = False, computer = 'partita')
