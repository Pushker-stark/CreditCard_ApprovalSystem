from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Customer,LoanData
from .serializers import CustomerSerializer,LoanSerializer

class RegisterCustomerView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            # Calculate the approved_limit based on the provided formula
            serializer.validated_data['approved_limit'] = round(36 * serializer.validated_data['monthly_salary'] / 100000) * 100000
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckEligibilityView(APIView):
    def post(self, request, *args, **kwargs):
        # Extract data from the request
        customer_id = request.data.get('customer_id')
        loan_amount = request.data.get('loan_amount')
        interest_rate = request.data.get('interest_rate')
        tenure = request.data.get('tenure')

        # Assume you have a Loan model and serializer
        loans = LoanData.objects.filter(customer_id=customer_id)

        # Calculate credit score based on specified components
        credit_score = self.calculate_credit_score(loans)

        # Check eligibility based on credit score and other conditions
        if credit_score > 50:
            approval = True
        elif 30 < credit_score <= 50 and interest_rate > 12:
            approval = True
        elif 10 < credit_score <= 30 and interest_rate > 16:
            approval = True
        else:
            approval = False

        # Calculate corrected interest rate if needed
        corrected_interest_rate = self.calculate_corrected_interest_rate(interest_rate, credit_score)

        # Other eligibility checks (e.g., sum of current EMIs)
        # ...

        # Return the response
        response_data = {
            'customer_id': customer_id,
            'approval': approval,
            'interest_rate': interest_rate,
            'corrected_interest_rate': corrected_interest_rate,
            'tenure': tenure,
            'monthly_installment': self.calculate_monthly_installment(loan_amount, corrected_interest_rate, tenure),
        }

        return Response(response_data, status=status.HTTP_200_OK)

    def calculate_credit_score(self, loans):
        # Implement logic to calculate credit score based on specified components
        # This can involve calculations using loan data
        # Return the calculated credit score
        return credit_score

    def calculate_corrected_interest_rate(self, interest_rate, credit_score):
        # Implement logic to correct interest rate based on credit score
        # Return the corrected interest rate
        return corrected_interest_rate

    def calculate_monthly_installment(self, loan_amount, interest_rate, tenure):
        # Implement logic to calculate the monthly installment
        # Return the calculated monthly installment
        return monthly_installment

class CreateLoanView(APIView):
    def post(self, request, *args, **kwargs):
        # Extract data from the request
        customer_id = request.data.get('customer_id')
        loan_amount = request.data.get('loan_amount')
        interest_rate = request.data.get('interest_rate')
        tenure = request.data.get('tenure')

        # Retrieve the customer
        try:
            customer = Customer.objects.get(pk=customer_id)
        except Customer.DoesNotExist:
            return Response({'message': 'Customer not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Check eligibility (you may implement the eligibility check logic here)
        eligibility_status, corrected_interest_rate, monthly_installment = self.check_eligibility(customer, loan_amount, interest_rate, tenure)

        # Process the loan based on eligibility
        if eligibility_status:
            # Create the loan
            loan = LoanData.objects.create(
                customer=customer,
                loan_amount=loan_amount,
                interest_rate=corrected_interest_rate,
                tenure=tenure,
                monthly_repayment=self.calculate_monthly_installment(loan_amount, corrected_interest_rate, tenure),
                emis_paid_on_time=0,  # Initial value
                # Add other loan attributes as needed
            )

            # Return the response with loan details
            response_data = {
                'loan_id': loan.id,
                'customer_id': customer_id,
                'loan_approved': True,
                'message': 'Loan approved.',
                'monthly_installment': monthly_installment,
            }

            return Response(response_data, status=status.HTTP_201_CREATED)

        else:
            # Return the response if the loan is not approved
            response_data = {
                'loan_id': None,
                'customer_id': customer_id,
                'loan_approved': False,
                'message': 'Loan not approved.',
                'monthly_installment': None,
            }

            return Response(response_data, status=status.HTTP_200_OK)

    def check_eligibility(self, customer, loan_amount, interest_rate, tenure):
        # Implement your eligibility check logic here
        # Return eligibility status, corrected interest rate, and monthly installment
        # You may use the provided components and criteria for eligibility
        # ...
        return eligibility_status, corrected_interest_rate, monthly_installment

    def calculate_monthly_installment(self, loan_amount, interest_rate, tenure):
        # Implement logic to calculate the monthly installment
        # Return the calculated monthly installment
        return monthly_installment


class ViewLoanDetailsView(APIView):
    def get(self, request, loan_id, *args, **kwargs):
        try:
            # Retrieve the loan with the given loan_id
            loan = LoanData.objects.get(pk=loan_id)
        except LoanData.DoesNotExist:
            return Response({'message': 'Loan not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the loan data
        loan_serializer = LoanSerializer(loan)

        # Serialize the customer data
        customer_serializer = loan_serializer.fields['customer']
        customer_data = customer_serializer.to_representation(loan.customer)

        # Construct the response data
        response_data = {
            'loan_id': loan.id,
            'customer': customer_data,
            'loan_amount': loan.loan_amount,
            'interest_rate': loan.interest_rate,
            'monthly_installment': loan.monthly_repayment,
            'tenure': loan.tenure,
        }

        return Response(response_data, status=status.HTTP_200_OK)


class ViewCustomerLoansView(APIView):
    def get(self, request, customer_id, *args, **kwargs):
        try:
            # Retrieve all loans for the given customer_id
            loans = LoanData.objects.filter(customer_id=customer_id)
        except LoanData.DoesNotExist:
            return Response({'message': 'Loans not found for the customer.'}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the list of loans
        loan_serializer = LoanSerializer(loans, many=True)

        # Construct the response data
        response_data = []
        for loan_data in loan_serializer.data:
            response_data.append({
                'loan_id': loan_data['id'],
                'loan_amount': loan_data['loan_amount'],
                'interest_rate': loan_data['interest_rate'],
                'monthly_installment': loan_data['monthly_repayment'],
                'repayments_left': self.calculate_repayments_left(loan_data),
            })

        return Response(response_data, status=status.HTTP_200_OK)

    def calculate_repayments_left(self, loan_data):
        # Implement logic to calculate the number of EMIs left
        # You may use the loan_data to calculate this based on your requirements
        # ...
        return repayments_left