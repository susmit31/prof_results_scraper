# ==================== Usage =============================
# ========================================================
# result_scraper.py <START_REG> <END_REG> <SAVE_RESULTS>
# ========================================================
# ========================================================

# Tunable parameters (in-code): 
# S_ID: session ID
# X_ID: exam ID
# SUBS: list containing names of subjects

X_ID = '1129'
S_ID = '22'
SUBS = {'pharm':"Pharmacology and Therapeutics", 'fm':"Forensic Medicine and Toxicology"}

import argparse
import requests
import sys
import time

RESULT_URL = 'https://www.cmc.du.ac.bd/ajax/get_program_by_exam.php'

REQUEST_DATA = {
    'reg_no':'',
    'pro_id':'1',
    'sess_id':S_ID,
    'exam_id':X_ID,
    'gdata':'99'   
}

def find_name(text):
    text = text[text.find("Student\'s Name")+23:]
    name = text[:text.find('</td>')]
    return name

def find_hons(text):
    hons_idx = text.find('Hons')
    if hons_idx==-1: return None
    text = text[hons_idx+6:]
    hons_text = text[:text.find('</span>')]
    return hons_text

def find_fail(text):
    fail_idx = text.find('Referred')
    if fail_idx == -1: return None
    text = text[fail_idx+len('Referred<br><small>'):]
    fail_text = text[:text.find('</small>')]
    return fail_text

def find_place(text):
    pos_idx = text.find('Position')
    if pos_idx==-1: return None
    text = text[pos_idx+len('Position: '):]
    pos_text = text[:3]
    return pos_text

def find_college(text):
    clg_idx_0 = text.find('College Name')
    if clg_idx_0 == -1: return None
    clg_idx_1 = text.find('</td>',clg_idx_0)
    clg_name = text[clg_idx_0+len('College Name</th><td>'):clg_idx_1]
    return clg_name

print(sys.argv)

results = []
hons = []
pass_count = 0
place_count = 0
eligible_count = 0
hons_count = 0
sub_hons = {k:0 for k in SUBS}

reg_start = int(sys.argv[1])
reg_end = int(sys.argv[2])
write_to_file = int(sys.argv[3])
if write_to_file:
    filename = input("Enter filename: ")

clg_stats = {}
for roll in range(reg_start,reg_end+1):
    REQUEST_DATA['reg_no'] = f"{roll}"
    res = requests.post(RESULT_URL, REQUEST_DATA)

    name = find_name(res.text)
    if 't-danger' in name: 
        print(f'{roll}\t    \t--')
        continue
    
    eligible_count+=1
    
    passed_idx = res.text.find('Passed')
    hons_data = find_hons(res.text)
    fail_data = find_fail(res.text)
    place_data = find_place(res.text)
    clg_name = find_college(res.text)

    if clg_name in clg_stats:
        if passed_idx > 0:
            clg_stats[clg_name][0] += 1
        else:
            clg_stats[clg_name][1] += 1
    else:
        clg_stats[clg_name] = [0,0] 
        if passed_idx > 0:
            clg_stats[clg_name][0] += 1
        else:
            clg_stats[clg_name][1] += 1
        
    
    if passed_idx>0:
        results.append(f'{roll}\t{name}\tP\t{hons_data if hons_data else "-"}\t{place_data if place_data else "-"}\t{clg_name}\n')
        pass_count+=1
        if hons_data:
            hons_count+=1
            hons.append(f'{roll}\t{name}\t{hons_data}\n')
            for sub in SUBS:
                if sub in hons_data:
                    sub_hons[sub]+=1
            if place_data:
                place_count+=1
            print(f'{roll}\t{name}\tHonours\t{clg_name}')
        else:
            print(f'{roll}\t{name}\tPassed\t{clg_name}')
    else:
        results.append(f'{roll}\t{name}\tF\t{fail_data}\t-\t{clg_name}\n')
        print(f'{roll}\t{name}\t404\t{clg_name}')
    if write_to_file:
        with open(filename, 'a') as f:
            f.writelines(results[-1])
    #time.sleep(1)
    
print(f"Pass percentage: {pass_count / eligible_count}")
print(f"Honours holders: {hons_count}")
print(f"Honours by subjects: {sub_hons}")
print(f"Placed students: {place_count}")
