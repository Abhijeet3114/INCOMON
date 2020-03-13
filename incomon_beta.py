def tax_calculator():
	global taxable_hra, gross_sal_income, gross_income, taxable_income, total_deduction, tax_liable
	taxable_hra = taxable_hra_calc()
	gross_sal_income = gross_income_from_sal()
	total_deduction = total_deduction_calculator()
	gross_income =	gross_income_calculator()
	taxable_income = taxable_income_calculator()
	temp_income = taxable_income
	liable = 0;
	slab_range = 250000;
	n = int(temp_income / slab_range)
	if(n <= 0):
		return 0
	percentage = 0;
	for i in range(n):
		liable += slab_range * (percentage / 100)
		temp_income = temp_income - slab_range;
		percentage = percentage + 5;
		if(temp_income < slab_range):
			break;
	liable += temp_income * (percentage / 100)
	liable = liable + (liable * 0.04)
	return liable 
	
def gross_income_calculator():
	return gross_sal_income + interest + other_sources
	
def taxable_income_calculator():
	return gross_income - total_deduction;
	
def  total_deduction_calculator():
	self_health = health1;
	parents = health2;
	d_80c = pf_n_other
	d_80tta = interest
	if(self_health > 25000):
		self_health = 25000
	if(parents > 50000):
		parents = 50000
	if(d_80c > 150000):
		d_80c = 150000
	if(d_80tta > 10000):
		d_80tta = 10000
	return d_80tta + d_80c + parents + self_health
	
def gross_income_from_sal():
	taxable_lta = (LTA - trav_expense)
	if(taxable_lta < 0):
		taxable_lta = 0				#if bill amount is exceding LTA then taxable LTA should be 0
	return a_basic_salary + taxable_hra + special_allow + taxable_lta - std_deduction;
	

def taxable_hra_calc():	#taxable HRA calculator
	result = hra;
	if(city == "Metro" or city == "metro"):		
		half_ab = a_basic_salary * 0.5;
	else:
		half_ab = a_basic_salary * 0.4;
	ten_ab = a_basic_salary * 0.1;
	excess_rent = rent_paid - ten_ab;
	if(excess_rent < half_ab):
		result = hra - excess_rent
	else:
		result = hra - half_ab
	if(result > 0):
		return result
	else:	
		return 0 

def sources():						#input
	global hra, a_basic_salary, rent_paid, special_allow, LTA, std_deduction, city, trav_expense, interest, pf_n_other, health1, health2, other_sources;
	print("INCOMON CLI beta\n*****Income Details*****");
	std_deduction = float("50000")
	hra = float(input("Enter HRA: "))
	city = input("City of Resedence(Metro/ Non-metro): ")
	a_basic_salary = float(input("Enter Basic salary: "))
	rent_paid = float(input("Enter rent paid: "))
	special_allow = float(input("Enter special allowance: "))	
	LTA = float(input("Enter LTA:"))
	trav_expense = float(input("Enter total amount of travel bills submitted: (during leave of atleast 3 days) "))
	print("\n*****DEDUCTIONS*****")
	interest = float(input("Total savings account interest received: "))		#under 80TTA
	pf_n_other = float(input("Total investment in PPF, ELSS, LIP, EPF: "))	# split in next version and this is under 80c
	health1 = float(input("investment in health insurance policy for self and family: "))			# self UNDER 80D
	health2 = float(input("Investment in health ins. policy for parents: "))							#parents under 80D
	print("\n*****OTHER*****")
	other_sources = float(input("Income from other sources"))

def main():							#main function
	sources()
	tax_liable = tax_calculator()
	print("\n\n\tREPORT GENERATED\n")
	print("TAXABLE HRA:\t\t\t"+str(taxable_hra))
	print("TOTAL DEDUCTIONS:\t\t"+str(total_deduction))
	print("GROSS INCOME FROM SALARY:\t"+str(gross_sal_income))
	print("GROSS INCOME:\t\t\t"+str(gross_income))
	print("TAXABLE INCOME:\t\t\t"+str(taxable_income))
	print("TOTAL INCOME TAX LIABILITY:\t"+str(tax_liable))
	#print(hra+"\n"+a_basic_salary+"\n"+rent_paid);

main()
