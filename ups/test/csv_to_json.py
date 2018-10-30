def get_str():
	two_list = []
	with open('history.csv', 'r', encoding='utf-8') as f:
		line = f.readlines()
		# 二维数组
		for item in line:
			row_list = item.split(',')
			two_list.append(row_list)
	return two_list


def to_json(final_dict):
	result = str(final_dict)
	json_format = result.replace("'", '"')
	json_forma1t = json_format.replace("\\n", '')
	print(json_forma1t)


def csv_to_json():
	two_list = get_str()
	final_dict = {}
	# 遍历每一行
	for item in two_list:
		# 0列
		val_0 = item[0]
		if val_0:
			final_dict.update({val_0: []})

		# 1列
		val_1 = item[1]
		val_0_key = list(final_dict.keys())[0]
		val_0_value = final_dict[val_0_key]
		if val_1:
			val_0_value.append({val_1: []})

		last = val_0_value[-1]
		# 2列
		val_2 = item[2]
		if val_2:
			if val_1:
				for i in val_0_value:
					if val_1 in i.keys():
						i[val_1].append({val_2: []})
			else:
				last_key = list(last.keys())[0]
				last[last_key].append({val_2: []})

		# 3列
		val_3 = item[3]
		if val_1 and val_2:
			for i2 in val_0_value:
				if val_1 in list(i2.keys()):
					i2_val = i2[val_1][0]
					i2_key = list(i2_val.keys())[0]
					i2_val[i2_key].append(val_3)
		else:
			v2_last = last[list(last.keys())[0]][-1]
			v2_last[list(v2_last.keys())[0]].append(val_3)

	to_json(final_dict)


if __name__ == '__main__':
	csv_to_json()
