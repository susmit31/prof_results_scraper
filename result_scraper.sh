#! /bin/bash

REQ_URL="https://ducmc.com/ajax/get_program_by_exam.php"
PRO_ID=1
SESS_ID=16
EXAM_ID=32
GDATA=99

echo "Enter start reg no.: "
read var_reg

echo "Enter end reg no.: "
read var_reg_max

while (("$var_reg" < "$var_reg_max"))
	do
		form_data="reg_no=$var_reg&pro_id=$PRO_ID&sess_id=$SESS_ID&exam_id=$EXAM_ID&gdata=$GDATA"
		response=$(curl -s -X POST -d $form_data $REQ_URL)
		if  echo $response | grep -c -q Passed
		then
			if echo $response | grep -c -q Hons
			then
				hons="furti"
			else
				hons="ok"
			fi
			echo "$var_reg $hons"
		elif echo $response | grep -c -q "t-danger"
		then
			echo "$var_reg -"
		else
			echo "$var_reg 404"
		fi
		var_reg=$(($var_reg+1))
done