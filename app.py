from flask import Flask, render_template, request
import pandas as pd
import joblib
import numpy as np
from sklearn.preprocessing import StandardScaler

with open('models/xgb_cv_compact_individual_final.pkl', 'rb') as f:
    clf_individual = joblib.load(f)
with open('models/gb_cv_compact_joint.pkl', 'rb') as f:
    clf_joint = joblib.load(f)
with open('models/knn_regression.pkl', 'rb') as f:
    knn = joblib.load(f)

ss = StandardScaler()


app = Flask(__name__)

# feature space
df_train_jl_scale = pd.read_csv("data/df_train_jl_scale.csv")
# load APR table
df_fico_apr = pd.read_csv("data/grade_to_apr.csv")

df_macro_mean = pd.read_csv(
    'data/df_macro_mean.csv', index_col=0, dtype=np.float64)

df_macro_std = pd.read_csv('data/df_macro_std.csv',
                           index_col=0, dtype=np.float64)

home_to_int = {'MORTGAGE': 4,
               'RENT': 3,
               'OWN': 5,
               'ANY': 2,
               'OTHER': 1,
               'NONE': 0}

sub_grade_to_char = {1: 'A1', 2: 'A2', 3: 'A3', 4: 'A4', 5: 'A5', 6: 'B1', 7: 'B2', 8: 'B3', 9: 'B4', 10: 'B5', 11: 'C1', 12: 'C2', 13: 'C3', 14: 'C4', 15: 'C5', 16: 'D1', 17: 'D2',
                     18: 'D3', 19: 'D4', 20: 'D5', 21: 'E1', 22: 'E2', 23: 'E3', 24: 'E4', 25: 'E5', 26: 'F1', 27: 'F2', 28: 'F3', 29: 'F4', 30: 'F5', 31: 'G1', 32: 'G2', 33: 'G3', 34: 'G4', 35: 'G5'}


@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html', title="Home - Lending Rupee")


@app.route("/individual", methods=['GET', 'POST'])
def individual():
    if request.method == 'GET':
        return (render_template('individual.html', title="Individual Loan Approval Prediction - Lending Rupee"))

    if request.method == 'POST':
        # fico score as integer
        cibil_score = int(request.form['cibil_score'])
        # loan amount as integer
        loan_amnt = float(request.form['loan_amnt'])
        # term as integer: 36 or 60
        term = int(request.form['term'])
        # debt to income as float
        currEmi = float(request.form['currEmi'])
        # home ownership as string
        home_ownership = request.form['home_ownership']
        # number or mortgage accounts as integer
        mort_acc = int(request.form['mort_acc'])
        # annual income as float
        annual_inc = float(request.form['annual_inc'])
        # number of open accounts as integer
        open_acc = int(request.form['open_acc'])
        # verification status as 0, 1, 2
        verification_status = int(request.form['verification_status'])
        # revolving utilization as float
        revol_util = float(request.form['revol_util'])
        # The total number of credit lines currently in the borrower's credit file
        total_acc = int(request.form['total_acc'])

        credit_line_ratio = open_acc/total_acc
        balance_annual_inc = loan_amnt/annual_inc
        # calculate grade from FICO
        sub_grade = knn.predict(np.reshape([cibil_score], (1, -1)))[0]
        # calculate grade
        grade = round(sub_grade/5) + 1
        # get interest rate
        apr_row = df_fico_apr[df_fico_apr['grade_num'] == sub_grade]

        # use equal monthly installment formula
        if term == 36:
            int_rate = 14/12/100
            emi = int_rate/36
            installment = loan_amnt * \
                (int_rate*(1+int_rate)**36) / ((1+int_rate)**36 - 1)
            term = 1

        else:
            int_rate = 14/12/100
            emi = int_rate/60
            installment = loan_amnt * \
                (int_rate*(1+int_rate)**36) / ((1+int_rate)**36 - 1)
            term = 2

        # make integer
        installment = int(installment)
        inst_amnt_ratio = installment/loan_amnt
        dti = (currEmi/(annual_inc/12)) * 100
        interest = 14/100

        temp = pd.DataFrame(index=[0])
        #temp['fico'] = fico

        temp['term'] = term
        temp['sub_grade'] = sub_grade
        temp['home_ownership'] = home_to_int[home_ownership.upper()]
        temp['annual_inc'] = np.log(annual_inc)
        temp['verification_status'] = verification_status
        temp['dti'] = dti
        temp['revol_util'] = revol_util
        temp['mort_acc'] = mort_acc
        temp['credit_line_ratio'] = credit_line_ratio
        temp['bal_annual_inc'] = balance_annual_inc
        temp['cibil_score'] = cibil_score
        temp['int_rate'] = interest
        temp['inst_anmt_ratio'] = inst_amnt_ratio

        # create original output dict
        output_dict = dict()
        output_dict['Provided Annual Income'] = annual_inc
        output_dict['Provided CIBIL Score'] = cibil_score
        output_dict['Interest Rate (%)'] = int(
            interest * 100)  # revert back to percentage
        output_dict['Estimated Installment Amount'] = installment
        output_dict['Number of Payments'] = 36 if term == 1 else 60
        output_dict['Sub Grade'] = sub_grade_to_char[35-int(sub_grade)]
        output_dict['Loan Amount'] = loan_amnt
        code = np.random.randint(99)
        # create deep copy
        scale = temp.copy()
        for feat in df_macro_mean.columns:
            scale[feat] = (scale[feat] - df_macro_mean.loc[code,
                                                           feat]) / df_macro_std.loc[code, feat]

        # make prediction
        pred = clf_individual.predict(scale)

        if dti > 43:
            res = 'Debt to income too high!'
        elif balance_annual_inc >= 0.43:
            res = 'Debt to income too high!'
        elif revol_util >= 90:
            res = 'Amount of credit used up too high!'
        elif pred == 1:
            res = 'Loan Denied'
        else:
            print(scale)
            print(pred)
            res = 'Congratulations! Approved!'

        CalEmi = ((annual_inc/12)*0.5) - currEmi
        amnt = (((1+int_rate)**term)-1) / ((1+int_rate) ** term) * 2.85
        principal = (CalEmi/int_rate) * amnt
        output_dict['Maximum Loan Amount Eligible (₹)'] = int(principal) * 12

        # render form again and add prediction
        return (render_template('individual.html',
                                original_input=output_dict,
                                result=res, title="Individual Loan Approval Prediction - Lending Rupee",
                                ))


@app.route("/joint", methods=['GET', 'POST'])
def joint():
    if request.method == 'GET':
        return render_template("joint.html", title="Joint Loan Approval Prediction - Lending Rupee")
    if request.method == 'POST':
        # get input
        # fico score as integer
        sec_cibil_score = int(request.form['cibil_score2'])
        cibil_score = int(request.form['cibil_score'])
        # loan amount as integer
        loan_amnt = float(request.form['loan_amnt'])
        # term as integer: 36 or 60
        term = int(request.form['term'])
        # debt to income as float
        currEmi = float(request.form['currEmi'])
        # home ownership as string
        home_ownership = request.form['home_ownership']
        # number or mortgage accounts as integer
        mort_acc = int(request.form['mort_acc'])
        # annual income as float
        annual_inc = float(request.form['annual_inc'])
        # annual income as float
        sec_annual_inc = float(request.form['sec_annual_inc'])
        # number of open accounts as integer
        inq_last_12m = int(request.form['inq_last_6mths'])
        # revolving utilization as float
        revol_util = float(request.form['revol_util'])
        total_bal_il = float(request.form['total_bal_il'])

        balance_annual_inc = loan_amnt/annual_inc
        sec_balance_annual_inc = loan_amnt/sec_annual_inc

        # calculate grade from FICO
        sub_grade = knn.predict(np.reshape([cibil_score], (1, -1)))[0]
        # calculate grade
        grade = round(sub_grade/5) + 1
        # get interest rate
        apr_row = df_fico_apr[df_fico_apr['grade_num'] == sub_grade]

        # use equal monthly installment formula
        if term == 36:
            int_rate = apr_row['36_mo'].values[0]/100
            emi = int_rate/36
            installment = loan_amnt * \
                (int_rate*(1+int_rate)**36) / ((1+int_rate)**36 - 1)
            term = 1

        else:
            int_rate = apr_row['60_mo'].values[0]/100
            emi = int_rate/60
            installment = loan_amnt * \
                (int_rate*(1+int_rate)**36) / ((1+int_rate)**36 - 1)
            term = 2

        # make integer
        installment = int(installment)
        inst_amnt_ratio = installment/loan_amnt
        dti_joint = (currEmi/int(((annual_inc+sec_annual_inc)/2)*12)) * 100

        temp = pd.DataFrame(index=[1])
        #temp['fico'] = fico

        temp['term'] = term
        temp['int_rate'] = int_rate
        temp['sub_grade'] = sub_grade
        temp['inst_amnt_ratio'] = inst_amnt_ratio
        temp['home_ownership'] = home_to_int[home_ownership.upper()]
        temp['dti_joint'] = dti_joint
        temp['sec_app_revol_util'] = revol_util
        temp['sec_app_mort_acc'] = mort_acc
        temp['balance_annual_inc'] = balance_annual_inc
        temp['sec_balance_annual_inc'] = sec_balance_annual_inc
        temp['sec_cibil_score'] = sec_cibil_score
        temp['total_bal_il'] = np.log(total_bal_il)
        temp['inq_last_12m'] = inq_last_12m

        # create original output dict
        output_dict = dict()
        output_dict['Given Annual Income'] = annual_inc
        output_dict['Calculated Avg CIBIL Score'] = cibil_score
        output_dict['Predicted Interest Rate'] = int_rate * \
            100  # revert back to percentage
        output_dict['Predicted Installment'] = installment
        output_dict['Number of Payments'] = 36 if term == 1 else 60
        output_dict['Sub Grade'] = sub_grade_to_char[35-int(sub_grade)]
        output_dict['Loan Amount'] = loan_amnt

        # create deep copy
        X_train = df_train_jl_scale[temp.columns]
        ss.fit(X_train)

        scale = temp.copy()
        scale = ss.transform(scale)

        # make prediction
        pred = clf_joint.predict(scale)

        if dti_joint > 43:
            res = 'Debt to income too high for secondary applicant'
        elif balance_annual_inc >= 0.43:
            res = 'Debt to income too high!'
        elif revol_util >= 90:
            res = 'Amount of credit used up too high for secondary applicant'
        elif pred == 1:
            res = 'Loan Denied!'
        else:
            res = 'Congratulations! Approved!'

        CalEmi = ((annual_inc/12)*0.5) - currEmi
        amnt = (((1+int_rate)**term)-1) / ((1+int_rate) ** term) * 2.85
        principal = (CalEmi/int_rate) * amnt
        output_dict['Maximum Loan Amount Eligible (₹)'] = int(principal) * 12

        # render form again and add prediction
        return render_template('joint.html',
                               original_input=output_dict,
                               result=res, title="Joint Loan Approval Prediction - Lending Rupee", 
                               )


@app.route("/emi_calculator")
def emi_calculator():
    return render_template("emi.html", title="EMI Calculator - Lending Rupee")


@app.route("/inflation_calculator")
def inflation_calculator():
    return render_template("inflation.html", title="Inflation Calculator - Lending Rupee")


if __name__ == "__main__":
    app.run(debug=True)
