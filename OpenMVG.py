import subprocess
import os
import sys

def openMVG_main(path):
    # OpenMVG

    print("Running OpenMVG on " + path + "List of images in the directory")
    run_cmd = "openMVG_main_SfMInit_ImageListing -i " + path + " -o " + path+"/init -d /Users/pierre/Development/openMVG/src/openMVG/exif/sensor_width_database/sensor_width_camera_database.txt -f 2340"
    subprocess.call(run_cmd, shell=True)
    
    print("Running OpenMVG on " + path + "Compute Features")
    run_cmd = "openMVG_main_ComputeFeatures -i " + path+"/init/sfm_data.json -o " + path+"/matches -m SIFT"
    subprocess.call(run_cmd, shell=True)

    print("Running OpenMVG on " + path + "Compute matching pairs")
    run_cmd = "openMVG_main_PairGenerator -i " + path+"/init/sfm_data.json -o " + path+"/matches/pairs.bin"
    subprocess.call(run_cmd, shell=True)

    print("Running OpenMVG on " + path + "Compute Matches")
    run_cmd = "openMVG_main_ComputeMatches -i " + path+"/init/sfm_data.json -p "+ path+"/matches/pairs.bin -o " + path+"/matches/matches.putative.bin"
    subprocess.call(run_cmd, shell=True)

    print("Running OpenMVG on " + path + "Compute Geometric Filter matches")
    run_cmd = "openMVG_main_GeometricFilter -i " + path+"/init/sfm_data.json -m " + path+"/matches/matches.putative.bin -g f -o " + path+"/matches/matches.f.bin"
    subprocess.call(run_cmd, shell=True)

    print("Running OpenMVG on " + path + "Incremental Structure from Motion")
    run_cmd = "openMVG_main_Sfm --sfm_engine INCREMENTAL --input_file " + path+"/init/sfm_data.json --match_dir " + path+"/matches/ --output_dir " + path+"/reconstruction"
    subprocess.call(run_cmd, shell=True)

    print("Colorize Structure from Motion")
    run_cmd = "openMVG_main_ComputeSfM_DataColor -i " + path+"/reconstruction/sfm_data.bin -o " + path+"/reconstruction/colorized.ply"
    subprocess.call(run_cmd, shell=True)

