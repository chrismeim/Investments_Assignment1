import pandas as pd
import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt

mpr = pd.read_excel(r"C:\Users\Chris\Desktop\Imperial Reading Material\Autumn Term\Investments and Portfolio Management\Assignment1\mpr.xls")
mpr.head(3)

factor3_model = pd.read_excel(r"C:\Users\Chris\Desktop\Imperial Reading Material\Autumn Term\Investments and Portfolio Management\Assignment1\data (1).xls")
factor3_model.head(3)


'''
Here I run the first pass regression
'''
column_names = factor3_model.columns.tolist() #create a list with all the column names from factor3_model

cap_names = []
for i in range(5,15):
    cap_names.append(column_names[i])          #list called cap_names in order to append the portfolio names of factor3_model

parameters = factor3_model[["Mkt (vwretd)", "SMB", "HML"]]
parameters = sm.add_constant(parameters)             #this adds a constant to the parameters, but through the results we see that it is not statistically significant

parameters.iloc[0]

Y_variable = {}      #These new dictionaries will incorporate my 10 regressions later on, based on the name of each portfolio
models = {}
results = {}
coef_mod = {}

for i in range(10):
    Y_variable[cap_names[i]] = factor3_model[cap_names[i]] - factor3_model["Risk-Free"]   #here I calculate the Y variable (dependend variable), which is the risk premium, for each of the 10 portfolios

for i in range(10):                                        #Here I regress my Y variable with the parameters of the model
    models[i] = sm.OLS(Y_variable[cap_names[i]], parameters)
    results[i] = models[i].fit()
    coef_mod[i] = results[i].params   

for i in range(10):
    print(f"Coefficients of {cap_names[i]}") 
    print(coef_mod[i])

results[0] = models[0].fit()   #Example if I want to showcase also other statistics of the regression
print(results[0].summary())    

for i in range(10):
    results[i] = models[i].fit()
    print(f"Summary of {cap_names[i]}")
    print(results[i].summary()) 

'''
As we can derive from the above results, the variables are statisticaly significant with a confidence level of 99%
The constant is not statisticaly significant > 0.05
'''

'''
Here I calculate the predicted variable based on the betas of my regression
After that, we plot the data in a scatter plot, this is for Portfolio 1
'''

x1 = []
for i in range(155):
    x1.append(coef_mod[0][1] * factor3_model["Mkt (vwretd)"][i])    
x2 = []
for i in range(155):
    x2.append(coef_mod[0][2] * factor3_model["SMB"][i])

x3 = []
for i in range(155):
    x3.append(coef_mod[0][3] * factor3_model["HML"][i])


x = []
for i in range(155):
    x.append(x1[i] + x2[i] + x3[i])


y = []
y1 = factor3_model["CAP1RET"]
y2 = factor3_model["Risk-Free"]
for i in range(155):
    y.append(y1[i] - y2[i])

reg = np.polyfit(x,y, deg = 1)
reg

trend = np.polyval(reg, x)
plt.scatter(x,y)
plt.xlabel('Predicted Returns')
plt.ylabel('Actual Returns')
plt.title('Regression of Portfolio 1')
plt.plot(x, trend)


''' 
Second Regression
'''

beta_const = []
beta_Mkt = []
beta_SMB = []
beta_HML = []

#appended the betas of each of the 10 regressions to their "specific" variable list, in order to take these variable as the independent variables in the next regression

for i in range(10):     
        beta_const.append(coef_mod[i][0])
        beta_Mkt.append(coef_mod[i][1])
        beta_SMB.append(coef_mod[i][2])
        beta_HML.append(coef_mod[i][3])

parameters2 = [beta_const, beta_Mkt, beta_SMB, beta_HML]
coef_mod2 = {"beta_const":beta_const, "risk_premium_Mkt": beta_Mkt, "risk_premium_SMB":beta_SMB, "risk_premium_HML": beta_HML}
coef_mod2 = pd.DataFrame(coef_mod2)

Y_var2 = []   #here I calculate the average return of each of the 10 portfolios for the given period
for j in range(1,11):
    x = 0
    for i in range(len(mpr)): 
        x += mpr.iloc[i][j]
    x = x/12
    Y_var2.append(x)

dependent_data = pd.DataFrame(Y_var2, columns=["Y_var2"]) #here I make Y_var2 a data frame
dependent_data

model2 = sm.OLS(dependent_data, coef_mod2)
result2 = model2.fit()  
print(result2.summary())  

'''
based on the above results we can conclude that the model describes in a very good maner the underlying returns.
In specific the risk spread of the Market along with the beta of SMB are statisticaly significant and the model gives us a 99% accuracy.
'''

xa_1 = []
for i in range(10):
    xa_1.append(-0.5162*coef_mod2["risk_premium_Mkt"][i])
xa_2 = []
for i in range(10):
    xa_2.append(0.777*coef_mod2["risk_premium_SMB"][i])


xa = []
for i in range(10):
    xa.append(xa_1[i]+xa_2[i])

reg2 = np.polyfit(xa,Y_var2, deg = 1)
reg2

trend2 = np.polyval(reg2, xa )
plt.scatter(xa,Y_var2)

plt.plot(xa, trend2)
plt.xlabel('Predicted Returns')
plt.ylabel('Actual Returns')
plt.title('Second Regression')







