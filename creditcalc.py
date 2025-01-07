import argparse
from math import ceil, log

class LoanCalc:
    """Class for calculating monthly loan repayments."""
    def __init__(self, interest, principal=None, payment=None, periods=None):
        self.principal = principal
        self.payment = payment
        self.interest = interest / 12 / 100
        self.periods = periods

    def print(self):
        return f"{self.principal, self.payment, self.interest, self.periods}"

    def months_of_repayment(self):
        """Calculates the number of months needed to repay the loan."""
        P, A, i = self.principal, self.payment, self.interest

        if A <= i * P:
            return "Invalid payment amount: Payment is too low to cover interest."

        x = (A / (A - i * P))
        base = 1 + i
        self.periods = ceil(log(x, base))

        years = self.periods // 12
        months = self.periods % 12
        answer = ""

        if years:
            answer = f"{years} year"
            if years > 1:
                answer += "s"
        if months:
            if years:
                answer += " and "
            answer += f"{months} month"
            if months > 1:
                answer += "s"
        return f"It will take {answer} to repay this loan!"

    def monthly_payment(self):
        """Calculates the monthly payment (the annuity payment)."""
        P, n, i = self.principal, self.periods, self.interest

        f = (1 + i)**n
        A = P * i * f / (f - 1)
        self.payment = ceil(A)
        return f"Your monthly payment = {self.payment}!"

    def loan_principal(self):
        """Calculates the loan principal."""
        A, n, i = self.payment, self.periods, self.interest

        f = (1 + i)**n
        P = A * (f - 1) / (i * f)
        return f"Your loan principal = {round(P)}!"

def are_they_positive(args):
    """Verifies that the values of the arguments are positive. If not, retrieves the correct value from the user."""
    for key, value in vars(args).items():
        if value is None:
            continue
        while value <= 0:
            try:
                if value > 0:
                    break
                value = float(input(f"Please enter a positive number for \"--{key}\" (current value: {value}): "))
                if value <= 0:
                    raise ValueError
                setattr(args, key, value)
            except ValueError:
                print(f"Invalid input. \"--{key}\" must be a positive number.")
    return args

def main():
    parser = argparse.ArgumentParser(description="This program calculates the number of monthly payments, the monthly payment amount, and the loan principal depending on what is missing from the input data.")
    parser.add_argument("--principal", type=float, help="You can get its value if you know the interest, annuity payment, and number of months.")
    parser.add_argument("--payment", type=float, help="The payment amount. It can be calculated using the provided principal, interest, and number of months.")
    parser.add_argument("--periods", type=int, help="Denotes the number of months needed to repay the loan. It's calculated based on the interest, annuity payment, and principal.")
    parser.add_argument("--interest", required=True, type=float, help="Specified without a percent sign. It must always be provided.")

    args = parser.parse_args()
    # args = parser.parse_args(['--principal', '-1000000', '--periods', '0', '--interest', '-10'])
    are_they_positive(args)

    calculator = LoanCalc(args.interest, args.principal, args.payment, args.periods)
    if args.periods is None and args.payment and args.principal:
        print(calculator.months_of_repayment())
    elif args.payment is None and args.principal and args.periods:
        print(calculator.monthly_payment())
    elif args.principal is None and args.payment and args.periods:
        print(calculator.loan_principal())
    else:
        print("Insert also a value for a missing one out of these: \"--principal\", \"--payment\", \"--periods\", \"--interest\"!!!")

if __name__ == '__main__':
    main()