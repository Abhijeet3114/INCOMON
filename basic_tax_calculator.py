def taxable_hra_calc(hra, a_basic_salary, rent_paid, city):	#taxable HRA calculator
	if(city == "Metro" || city == "metro"):		
		half_ab = a_basic_salary * 0.5;
	else:
		half_ab = a_basic_salary * 0.4;
	ten_ab = a_basic_salary * 0.1;
	excess_rent = rent_paid - ten_ab;
	if(excess_rent < half_ab):
		return hra - excess_rent
	else:
		return hra - half_ab
def sources():						#input
	global hra, a_basic_salary, rent_paid, special_allow, LTA, std_deduc, city;
	std_deduction = float("50000");
	hra = float(input("Enter HRA:"))
	city = input("City of Resedence(Metro/ Non-metro):");
	a_basic_salary = float(input("Enter Basic salary:"))
	rent_paid = float(input("Enter rent paid:"))
	special_allow = float(input("Enter special allowance:"))
	LTA
	
def main():						#main function
	sources()
	taxable_hra = taxable_hra_calc(hra, a_basic_salary, rent_paid, city)
	print(taxable_hra)
	#print(hra+"\n"+a_basic_salary+"\n"+rent_paid);

main()
