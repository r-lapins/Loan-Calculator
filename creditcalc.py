import argparse
from math import ceil, log
from sys import exit

class LoanCalc:
    """Class for calculating monthly loan repayments."""
    def __init__(self, type, interest, principal=None, payment=None, periods=None):
        self.type = type
        self.principal = principal
        self.payment = payment
        self.interest = interest / 12 / 100
        self.periods = periods

    def months_of_repayment(self):
        """Calculates the number of months needed to repay the loan."""
        P, A, i = self.principal, self.payment, self.interest

        if A <= i * P:
            return "Invalid payment amount: Payment is too low to cover interest."

        x = (A / (A - i * P))
        base = 1 + i
        n = ceil(log(x, base))
        self.periods = n

        years = n // 12
        months = n % 12
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
        return f"It will take {answer} to repay this loan!\nOverpayment = {int(A * n - P)}"

    def monthly_payment(self):
        """Calculates the monthly payment (the annuity payment)."""
        P, n, i = self.principal, self.periods, self.interest

        f = (1 + i)**n
        A = ceil(P * i * f / (f - 1))
        self.payment = A
        return f"Your monthly payment = {A}!\nOverpayment = {int(A * n - P)}"

    def loan_principal(self):
        """Calculates the loan principal."""
        A, n, i = self.payment, self.periods, self.interest

        f = (1 + i)**n
        P = ceil(A * (f - 1) / (i * f))
        self.principal = P
        return f"Your loan principal = {P}!\nOverpayment = {int(A * n - P)}"

    def diff_payment(self):
        """Calculates the monthly payments (the differential payment)."""
        P, n, i = self.principal, self.periods, self.interest
        total = 0
        for m in range(n):
            m += 1
            D_m = ceil(P / n + i * (P - P * (m - 1) / n))
            total += D_m
            print(f"Month {m}: payment is {D_m}")
        return f"\nOverpayment = {int(total - P)}"

# def are_params_correct(args):
    # """Verifies that the values of the arguments are positive. If not, retrieves the correct value from the user."""
    # for key, value in vars(args).items():
    #     if value is None or type(value) is str:
    #         continue
    #     while value <= 0:
    #         try:
    #             if value > 0:
    #                 break
    #             value = float(input(f"Please enter a positive number for \"--{key}\" (current value: {value}): "))
    #             if value <= 0:
    #                 raise ValueError
    #             setattr(args, key, value)
    #         except ValueError:
    #             print(f"Invalid input. \"--{key}\" must be a positive number.")
    # return args

def main():
    parser = argparse.ArgumentParser(description="This program calculates the number of monthly payments, the monthly payment amount, and the loan principal depending on what is missing from the input data.")
    parser.add_argument("--type", type=str, help="You need to choose only one type from the list.")
    parser.add_argument("--principal", type=float, help="You can get its value if you know the interest, annuity payment, and number of months.")
    parser.add_argument("--payment", type=float, help="The payment amount. It can be calculated using the provided principal, interest, and number of months.")
    parser.add_argument("--periods", type=int, help="Denotes the number of months needed to repay the loan. It's calculated based on the interest, annuity payment, and principal.")
    parser.add_argument("--interest", type=float, help="Specified without a percent sign. It must always be provided.")

    # args = parser.parse_args(['--type', 'diff', '--principal', '1000000', '--periods', '10', '--interest', '10'])
    args = parser.parse_args()
    t, p, a, n, i = args.type, args.principal, args.payment, args.periods, args.interest

    # Checks the correctness of the parameters
    if None in [t, i]:
        print("Incorrect parameters")
        exit()
    elif any([x is not None and x < 0 for x in [p, a, n, i]]):
        print("Incorrect parameters")
        exit()

    calculator = LoanCalc(t, i, p, a, n)

    if t == "annuity":
        if all([not p, a, n]):
            print(calculator.loan_principal())
        elif all([p, not a, n]):
            print(calculator.monthly_payment())
        elif all([p, a, not n]):
            print(calculator.months_of_repayment())
        else:
            print("Incorrect parameters")
    elif t == "diff" and all([p, n]):
        print(calculator.diff_payment())
    else:
        print("Incorrect parameters")

if __name__ == '__main__':
    main()