# Assumptions for the Lendify Banking Loans System

## User Roles and Signup Process

1. **LoanProvider and LoanCustomer Signup**:

   - Only **LoanProviders** and **LoanCustomers** are allowed to sign up for user accounts.
   - During signup, users must choose their role (**LoanProvider** or **LoanCustomer**).

2. **BankPersonnel Addition**:
   - **BankPersonnels** cannot sign up through the public interface.
   - BankPersonnels are added exclusively by an admin through the **Django Admin Interface**.

---

## Fund Management

1. **Fund Storage**:

   - Funds are managed in a separate database table (`Fund`).
   - The table tracks:
     - **Total available funds**.
     - **Funding limits**, ensuring overfunding prevention.

2. **Funding Limit Management**:
   - Only **BankPersonnels** are authorized to set or modify the funding limit.

---

## Loan Application and Approval

1. **LoanCustomer Balance**:
   - Each LoanCustomer has a **balance** field in their profile.
   - When a **BankPersonnel** accepts a LoanCustomer's **LoanApplication**, the loan amount is automatically credited to the customer's balance.

---
