def gross_income_from_sal():
	taxable_lta = (LTA - trav_expense)
	if(taxable_lta < 0):
		taxable_lta = 0				#if bill amount is exceding LTA then taxable LTA should be 0
	return a_basic_salary + taxable_hra + special_allow + taxable_lta - std_deduction;
	

def taxable_hra_calc():	#taxable HRA calculator
	if(city == "Metro" or city == "metro"):		
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
	global hra, a_basic_salary, rent_paid, special_allow, LTA, std_deduction, city, trav_expense;
	print("Enter details on yearly basis");
	std_deduction = float("50000")
	hra = float(input("Enter HRA:"))
	city = input("City of Resedence(Metro/ Non-metro):")
	a_basic_salary = float(input("Enter Basic salary:"))
	rent_paid = float(input("Enter rent paid:"))
	special_allow = float(input("Enter special allowance:"))	
	LTA = float(input("Enter LTA:"))
	trav_expense = float(input("Enter total amount of travel bills submitted: (during leave of atleast 3 days) "))
	
def main():	
	global taxable_hra, gross_sal_income					#main function
	sources()
	taxable_hra = taxable_hra_calc()
	gross_sal_income = gross_income_from_sal()
	print(gross_sal_income)
	#print(taxable_hra)
	#print(hra+"\n"+a_basic_salary+"\n"+rent_paid);

main()
