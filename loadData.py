import csvReader

def load_genusData(filename) :
	#read csv file
	csv_list, nrows, ncols = csvReader.csv_reader(filename)

	x_data = csv_list[0][2:]

	genus_dic = {}

	table_sum = [0 for i in range(len(x_data))]
	bottom_data = {}
	bottom_data[0] =[0 for i in range(len(x_data))]

	for row_num in range(1,nrows):
		current_genus = csv_list[row_num][0]
		current_type = csv_list[row_num][1]
		
		genus_dic[row_num] = {}
		genus_dic[row_num]['type']= current_type
		genus_dic[row_num]['rate']= csv_list[row_num][2:]
		genus_dic[row_num]['name'] = current_genus

		table_sum = [i+j for i,j in zip(table_sum, csv_list[row_num][2:])]
		bottom_data[row_num] = table_sum

	#conver to percent
	for row_num in range(1,nrows):
		genus_dic[row_num]['rate']= [i/j*100 for i,j in zip(genus_dic[row_num]['rate'],table_sum)]
		bottom_data[row_num] = [i/j*100 for i,j in zip(bottom_data[row_num], table_sum)]

	return nrows, x_data, genus_dic, bottom_data


def load_speciesData(filename) :
	#read csv file
	csv_list, nrows, ncols = csvReader.csv_reader(filename)

	x_data = csv_list[0][2:]

	species_dic = {}
	bottom_data = {}

	for row_num in range(1, nrows):
		current_genus = csv_list[row_num][0]
		current_species = csv_list[row_num][1]

		if(species_dic.get(current_genus) == None) : 
			n=1
			species_dic[current_genus] = {}
			bottom_data[current_genus] = {}
			bottom_data[current_genus][0] = [0 for i in range(len(x_data))]
			n = n-1

		n = n+1

		# print n
		species_dic[current_genus][n] = {}
		# print species_dic[current_genus][n]

		species_dic[current_genus][n]['rate']= csv_list[row_num][2:]
		species_dic[current_genus][n]['name']= current_species

		bottom_data[current_genus][n] = [i+j for i,j in zip(bottom_data[current_genus][n-1], csv_list[row_num][2:])]

	return nrows, x_data, species_dic, bottom_data