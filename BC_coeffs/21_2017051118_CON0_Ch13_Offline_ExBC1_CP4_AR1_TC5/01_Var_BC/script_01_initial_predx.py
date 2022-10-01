import os
import re
import time
import datetime
from subroutine import file_operations as fo

dir_GOES   = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction'
dir_wrfout = dir_GOES + '/24_Revision/BC_coeffs/01_run_wrf/wrfout_and_wrfrst'
dir_main   = dir_GOES + '/24_Revision/BC_coeffs/21_2017051118_CON0_Ch13_Offline_ExBC1_CP4_AR1_TC5/01_Var_BC'
dir_bufr   = dir_GOES + '/Data/abi'
dir_option = dir_main + '/option_01'
dir_diag   = dir_main + '/save_files'

anl_start_time   = datetime.datetime(2017, 5, 11, 18, 0, 0)
anl_end_time     = datetime.datetime(2017, 5, 11, 18, 0, 0)
cycling_interval = 6
forecast_hours   = [6]
domains          = ['d01']

time_now = anl_start_time
while time_now <= anl_end_time:
    for dom in domains:
        for fhours in forecast_hours:

            time_now_str = time_now.strftime('%Y%m%d%H')
            dir_save     = dir_diag + '/' + time_now_str + '_99'
            os.system('mkdir ' + dir_save)

            ftime        = time_now + datetime.timedelta(hours = fhours)
            ftime_str    = ftime.strftime('%Y%m%d%H')

            run_gsi_dir  = dir_main + '/' + ftime_str
            print(time_now_str + ': ' + str(fhours).zfill(2) + ' forecast hours')
            print('forecast time: ' + ftime_str)
            os.system('mkdir ' + run_gsi_dir)

            print('Create bkg folder, and copy wrfout to bkg')
            bkg_dir = run_gsi_dir + '/bkg'
            wrfout  = dir_wrfout + '/' + time_now_str + '/wrfout_' + dom + '_' + ftime.strftime('%Y-%m-%d_%H:00:00')
            os.system('mkdir ' + bkg_dir)
            os.system('cp ' + wrfout + ' ' + bkg_dir)

            print('Create obs folder, and copy abi bufr to obs')
            obs_dir = run_gsi_dir + '/obs'
            bufr    = dir_bufr + '/' + ftime.strftime('%Y%m%d') + '/gdas.t' + ftime.strftime('%H') + 'z.goesrabi.tm00.bufr_d'
            os.system('mkdir ' + obs_dir)
            os.system('cp ' + bufr + ' ' + obs_dir)

            print('Copy, revise, and the script of running gsi at ', ftime_str)
            run_gsi_input = fo.change_content(dir_option + '/run_GSI_ABI.sh')
            run_gsi_input.substitude_string('ANAL_TIME', '=', ftime_str)
            run_gsi_input.substitude_string('DOMAIN_NAME', '=', dom)
            run_gsi_input.save_content()

            info = os.popen('cd ' + dir_option + ' && sbatch ./run_GSI_ABI.sh').read()
            jobid = re.findall(r"\d+\.?\d*", info)
            print('Run gsi for domain ', dom, ' at ', ftime_str, ', jobid: ', jobid)
            flag = True
            while flag:
                time.sleep(30)
                flag = False
                info = os.popen('squeue -u u1237353').read()
                number_in_info = re.findall(r"\d+\.?\d*", info)
                for num in number_in_info:
                    if num == jobid[0]:
                        flag = True
            print('Finish running gsi at ', ftime_str, ' for ', dom)

            diag_ges    = dir_save + "/diag_abi_g16_ges." + ftime_str + "." + dom
            results_ges = dir_save + "/results_abi_g16_ges." + ftime_str + "." + dom
            f = open(dir_option + '/namelist.rad', 'w')
            f.write("&iosetup\n")
            f.write(" infilename='" + diag_ges + "',\n")
            f.write(" outfilename='" + results_ges + "',\n")
            f.write("/")
            f.close()

            print('Copy ges diag files')
            os.system('cp ' + run_gsi_dir + '/case_' + dom + '/diag_abi_g16_ges.* ' + diag_ges)

            print('Run read_diag_rad_ges.x')
            info = os.popen('cd ' + dir_option + ' && sbatch ./run_read_diag_rad_ges.sh').read()
            jobid = re.findall(r"\d+\.?\d*", info)
            print('Run read_diag_rad for domain ', dom, ' at ', ftime_str, ', jobid: ', jobid)
            flag = True
            while flag:
                time.sleep(30)
                flag = False
                info = os.popen('squeue -u u1237353').read()
                number_in_info = re.findall(r"\d+\.?\d*", info)
                for num in number_in_info:
                    if num == jobid[0]:
                        flag = True

            diag_anl    = dir_save + "/diag_abi_g16_anl." + ftime_str + "." + dom
            results_anl = dir_save + "/results_abi_g16_anl." + ftime_str + "." + dom
            f = open(dir_option + '/namelist.rad', 'w')
            f.write("&iosetup\n")
            f.write(" infilename='" + diag_anl + "',\n")
            f.write(" outfilename='" + results_anl + "',\n")
            f.write("/")
            f.close()

            print('Copy anl diag files')
            os.system('cp ' + run_gsi_dir + '/case_' + dom + '/diag_abi_g16_anl.* ' + diag_anl)

            print('Run read_diag_rad_anl.x')
            info = os.popen('cd ' + dir_option + ' && sbatch ./run_read_diag_rad_anl.sh').read()
            jobid = re.findall(r"\d+\.?\d*", info)
            print('Run read_diag_rad for domain ', dom, ' at ', ftime_str, ', jobid: ', jobid)
            flag = True
            while flag:
                time.sleep(30)
                flag = False
                info = os.popen('squeue -u u1237353').read()
                number_in_info = re.findall(r"\d+\.?\d*", info)
                for num in number_in_info:
                    if num == jobid[0]:
                        flag = True

            print('Copy satbias_in')
            diag_satbias = dir_save + "/satbias_in." + ftime_str + "." + dom
            os.system('cp ' + run_gsi_dir + '/case_' + dom + '/satbias_in ' + diag_satbias)

            print('Copy satbias_out')
            diag_satbias = dir_save + "/satbias_out." + ftime_str + "." + dom
            os.system('cp ' + run_gsi_dir + '/case_' + dom + '/satbias_out ' + diag_satbias)

            print('Copy satbias_pc')
            diag_satbias = dir_save + "/satbias_pc." + ftime_str + "." + dom
            os.system('cp ' + run_gsi_dir + '/case_' + dom + '/satbias_pc ' + diag_satbias)

            print('Copy satbias_pc.out')
            diag_satbias = dir_save + "/satbias_pc.out." + ftime_str + "." + dom
            os.system('cp ' + run_gsi_dir + '/case_' + dom + '/satbias_pc.out ' + diag_satbias)

            print('Copy satbias_out to satbias_in')
            diag_satbias = dir_save + "/satbias_out." + ftime_str + "." + dom
            os.system('cp ' + diag_satbias + ' ' + run_gsi_dir + '/case_' + dom + '/satbias_in')

            print('Copy satbias_pc.out to satbias_pc')
            diag_satbias = dir_save + "/satbias_pc.out." + ftime_str + "." + dom
            os.system('cp ' + diag_satbias + ' ' + run_gsi_dir + '/case_' + dom + '/satbias_pc')

            print('Copy diag_abi_g16_anl to diag_abi_g16')
            diag_anl = dir_save + "/diag_abi_g16_anl." + ftime_str + "." + dom
            os.system('cp ' + diag_anl + ' ' + run_gsi_dir + '/case_' + dom + '/diag_abi_g16')

            os.system('cp ' + dir_option + '/run_gsi.sh ' + run_gsi_dir + '/case_' + dom + '/run_gsi.sh')
            info = os.popen('cd ' + run_gsi_dir + '/case_' + dom + ' && sbatch ./run_gsi.sh').read()
            jobid = re.findall(r"\d+\.?\d*", info)
            print('Run gsi for domain ', dom, ' at ', ftime_str, ', jobid: ', jobid)
            flag = True
            while flag:
                time.sleep(30)
                flag = False
                info = os.popen('squeue -u u1237353').read()
                number_in_info = re.findall(r"\d+\.?\d*", info)
                for num in number_in_info:
                    if num == jobid[0]:
                        flag = True
            print('Finish running gsi at ', ftime_str, ' for ', dom)

            time_now_str = time_now.strftime('%Y%m%d%H')
            dir_save     = dir_diag + '/' + time_now_str + '_00'
            os.system('mkdir ' + dir_save)

            diag_ges    = dir_save + "/diag_abi_g16_ges." + ftime_str + "." + dom
            results_ges = dir_save + "/results_abi_g16_ges." + ftime_str + "." + dom
            f = open(dir_option + '/namelist.rad', 'w')
            f.write("&iosetup\n")
            f.write(" infilename='" + diag_ges + "',\n")
            f.write(" outfilename='" + results_ges + "',\n")
            f.write("/")
            f.close()

            print('Copy ges diag files')
            os.system('cp ' + run_gsi_dir + '/case_' + dom + '/diag_abi_g16_ges.* ' + diag_ges)

            print('Run read_diag_rad_ges.x')
            info = os.popen('cd ' + dir_option + ' && sbatch ./run_read_diag_rad_ges.sh').read()
            jobid = re.findall(r"\d+\.?\d*", info)
            print('Run read_diag_rad for domain ', dom, ' at ', ftime_str, ', jobid: ', jobid)
            flag = True
            while flag:
                time.sleep(30)
                flag = False
                info = os.popen('squeue -u u1237353').read()
                number_in_info = re.findall(r"\d+\.?\d*", info)
                for num in number_in_info:
                    if num == jobid[0]:
                        flag = True

            diag_anl    = dir_save + "/diag_abi_g16_anl." + ftime_str + "." + dom
            results_anl = dir_save + "/results_abi_g16_anl." + ftime_str + "." + dom
            f = open(dir_option + '/namelist.rad', 'w')
            f.write("&iosetup\n")
            f.write(" infilename='" + diag_anl + "',\n")
            f.write(" outfilename='" + results_anl + "',\n")
            f.write("/")
            f.close()

            print('Copy anl diag files')
            os.system('cp ' + run_gsi_dir + '/case_' + dom + '/diag_abi_g16_anl.* ' + diag_anl)

            print('Run read_diag_rad_anl.x')
            info = os.popen('cd ' + dir_option + ' && sbatch ./run_read_diag_rad_anl.sh').read()
            jobid = re.findall(r"\d+\.?\d*", info)
            print('Run read_diag_rad for domain ', dom, ' at ', ftime_str, ', jobid: ', jobid)
            flag = True
            while flag:
                time.sleep(30)
                flag = False
                info = os.popen('squeue -u u1237353').read()
                number_in_info = re.findall(r"\d+\.?\d*", info)
                for num in number_in_info:
                    if num == jobid[0]:
                        flag = True

            print('Copy satbias_in')
            diag_satbias = dir_save + "/satbias_in." + ftime_str + "." + dom
            os.system('cp ' + run_gsi_dir + '/case_' + dom + '/satbias_in ' + diag_satbias)

            print('Copy satbias_out.int')
            diag_satbias = dir_save + "/satbias_out." + ftime_str + "." + dom
            os.system('cp ' + run_gsi_dir + '/case_' + dom + '/satbias_out.int ' + diag_satbias)

            print('Copy satbias_pc')
            diag_satbias = dir_save + "/satbias_pc." + ftime_str + "." + dom
            os.system('cp ' + run_gsi_dir + '/case_' + dom + '/satbias_pc ' + diag_satbias)

            print('Copy satbias_pc.out')
            diag_satbias = dir_save + "/satbias_pc.out." + ftime_str + "." + dom
            os.system('cp ' + run_gsi_dir + '/case_' + dom + '/satbias_pc.out ' + diag_satbias)

            print('Delete: ' + run_gsi_dir)
            os.system('rm -rf ' + run_gsi_dir)
            os.system('rm -rf ' + dir_option + '/slurm*')

    time_now = time_now + datetime.timedelta(hours = cycling_interval)
