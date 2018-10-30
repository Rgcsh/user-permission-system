import json


def find(key):
	with open('result.json', 'r', encoding='utf-8') as f:
		json_str = f.read()
		json_format = json.loads(json_str.replace("\\n", ''))
		if key not in json_str:
			return f'不存在关键字：{key}'
		else:
			# 第一层
			first_key = list(json_format.keys())[0]
			if key == first_key:
				return key
			# 第二层
			for sec_item in json_format[first_key]:
				sec_item_key = list(sec_item.keys())[0]
				if key == sec_item_key:
					return f'{first_key}.{sec_item_key}'
				three_list = sec_item[sec_item_key]
				# 第三层
				for three_item in three_list:
					three_item_key = list(three_item.keys())[0]
					if key == three_item_key:
						return f'{first_key}.{sec_item_key}.{three_item_key}'
					# 第四层
					for four_item in three_item[three_item_key]:
						if key == four_item:
							return f'{first_key}.{sec_item_key}.{three_item_key}.{key}'

		return f'不存在关键字：{key}'


if __name__ == '__main__':
	# 精确匹配
	result = find('公历')
	print(result)
