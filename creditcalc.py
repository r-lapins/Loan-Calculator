from math import ceil

class LoanCalc:
    """Class for calculating monthly loan repayments."""
    def __init__(self, loan_principal):
        self.loan_principal = loan_principal

    def months_of_repayment(self, monthly_payment):
        """Calculates the number of months needed to repay the loan."""
        return ceil(self.loan_principal / monthly_payment)

    def monthly_payment(self, months_to_repay):
        """Calculates the monthly repayment and the final instalment."""
        regular_payment = ceil(self.loan_principal / months_to_repay)
        last_payment = self.loan_principal - (months_to_repay - 1) * regular_payment
        return regular_payment, last_payment

def get_positive_int(prompt):
    """Retrieves a positive integer from the user."""
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                raise ValueError
            return value
        except ValueError:
            print("Please enter a positive integer.")

def main():
    print("Welcome to the Loan Calculator!")
    calculator = LoanCalc(get_positive_int("Enter the loan principal:\n"))

    while True:
        choice = input("""What do you want to calculate?
        type "m" for number of monthly payments,
        type "p" for the monthly payment:\n""").strip().lower()
        if choice in {"m", "p"}:
            break
        print("Invalid choice. Please type 'm' or 'p'.")

    if choice == "m":
        n_months = calculator.months_of_repayment(get_positive_int("Enter the monthly payment:\n"))
        print(f"It will take {n_months} months to repay the loan")
    elif choice == "p":
        regular_payment, last_payment = calculator.monthly_payment(get_positive_int("Enter the number of months:\n"))
        loan_message = f"Your monthly payment = {regular_payment}"
        if regular_payment != last_payment:
            loan_message += f" and the last payment = {last_payment}."
        print(loan_message)
    else:
        print("Invalid choice. Please type 'm' or 'p'.")

if __name__ == '__main__':
    main()