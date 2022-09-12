import requests
import sys

if sys.argv[4]=="s":
    RESULT_URL = 'https://ducmc.com/ajax/get_program_by_exam.php'
else:
    RESULT_URL = 'http://ducmc.com/ajax/get_program_by_exam.php'

REQUEST_DATA = {
    'reg_no':'',
    'pro_id':'1',
    'sess_id':'17',
    'exam_id':'201',
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

results = []
hons = []
pass_count = 0
place_count = 0
eligible_count = 0
hons_count = 0
sub_hons = {'med':0, 'surg':0, 'gyn':0}

reg_start = int(sys.argv[1])
reg_end = int(sys.argv[2])
write_to_file = int(sys.argv[3])
if write_to_file:
    filename = input("Enter filename: ")

for roll in range(reg_start,reg_end+1):
    REQUEST_DATA['reg_no'] = f'{roll}'
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

    if passed_idx>0:
        results.append(f'{roll}\t{name}\tP\t \t{hons_data if hons_data else ""}\t{place_data if place_data else ""}\n')
        pass_count+=1
        if hons_data:
            hons_count+=1
            hons.append(f'{roll}\t{name}\t{hons_data}\n')
            if 'Med' in hons_data:
                sub_hons['med']+=1
            if 'Gyn' in hons_data:
                sub_hons['gyn']+=1
            if 'Surg' in hons_data:
                sub_hons['surg']+=1
            if place_data:
                place_count+=1
            print(f'{roll}\t{name}\tHonours')
        else:
            print(f'{roll}\t{name}\tPassed')
    else:
        results.append(f'{roll}\t{name}\tF\t{fail_data}\t\n')
        print(f'{roll}\t{name}\t404')
    if write_to_file:
        with open(filename, 'a') as f:
            f.writelines(results[-1])

print(pass_count / eligible_count)
print(hons_count)
print(sub_hons)
print(place_count)
