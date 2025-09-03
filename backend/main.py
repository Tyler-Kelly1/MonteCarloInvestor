
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from scipy.stats import norm
from scipy.stats import lognorm


class IntialChoices:
    
    def __init__(self, age, salary, retirementAge = 60, initalNetworth = 0, savingPercentage = .20, investmentPercentage = .20, annualRetrun = 0.08, marketVolatilaity = 0.15, inflationRate = 0.03):
        
        self.age = age
        self.salary = salary
        self.retirementAge = retirementAge
        self.principle = initalNetworth
        self.savePerc = savingPercentage
        self.investPerc = investmentPercentage
        self.annualReturn = annualRetrun
        self.inflationRate = inflationRate
        self.volatility = marketVolatilaity
        

class NetWorthEngine:
    
    def __init__(self, conditions: IntialChoices):
        self.conditions = conditions
        
    def progressIdealYear(self, curInvestment, curSavings, monthlyInvestment, monthlySavings):
        
        invesmentAmount = curInvestment
        savingsAmount = curSavings
             
        if(monthlyInvestment > 0):
            
            ### Annual Return to monthly
            monthlyRate = self.conditions.annualReturn / 12
     
            for _ in range(12):
                invesmentAmount = invesmentAmount * (1 + monthlyRate) + monthlyInvestment
                    
        if(monthlySavings > 0):
                
            savingsAmount += (monthlySavings*12)
                
        return (invesmentAmount, savingsAmount)
            
    def progressStochasticYear(self, curInvestment, monthlyInvestment):
        
        ### Very similar to ideal year but instead of a fixed monthly return rate we hit with a bit of randomness
        
        monthlyRate = np.random.normal(self.conditions.annualReturn, self.conditions.volatility) / 12
        bal = curInvestment
        
        ### Progress the year with the new rate
        for _ in range(12):
            
            if(bal == 0):
                bal = monthlyInvestment
            else:
                bal = bal * (1 + monthlyRate) + monthlyInvestment
        
        ### Return our updated investment balance
        return bal
        
    
    def calculateNetworth(self):
        
        ### SET UP:
        networth = self.conditions.principle
        simulationYears = self.conditions.retirementAge - self.conditions.age
        monthlySalary = self.conditions.salary / 12
        invesmentAmount = self.conditions.investPerc * networth
        savingsAmount = self.conditions.savePerc * networth

        
        networthProgrssion = []
         
        ### STEP 1: Simulate Returns of Investments 
        monthlyInvestment = self.conditions.investPerc * monthlySalary
        monthlySavings = self.conditions.savePerc * monthlySalary
        
        ### DEBUG STATS, DELETE LATER
        print(f"Monthly Salary: ${monthlySalary}")
        print(f"Monthly Investment: ${monthlyInvestment}")
        print(f"Monthly Saving: ${monthlySavings}")

        ### For each year
        for year in range(1,simulationYears+1):
            
            ### Update our new investment and savings amount
            invesmentAmount, savingsAmount = self.progressIdealYear(invesmentAmount, savingsAmount, monthlyInvestment, monthlySavings)
            
            ### update our total networth
            networth = savingsAmount + invesmentAmount
            
            ### Append our current years networth to our progression
            networthProgrssion.append({"year":year+self.conditions.age,"networth":networth, "realNetworth": networth/((1+self.conditions.inflationRate) ** year), "savings":savingsAmount, "investments":invesmentAmount})
        
        return (networth, networthProgrssion)
    
    def monteCarloSim(self, simCount):
        
        ### Need a simulation loop
        monthlyInvestment = (self.conditions.salary * self.conditions.investPerc) / 12
        simulationYears = self.conditions.retirementAge - self.conditions.age
        
        simulationResults = []

        for sim in range(simCount):
            

            ### Inside each simulation we essentially need to run our networth calculator with stoastic progressions.
            ### However since we are focused on investing here we will disregard saving.
            balance = self.conditions.principle
            balanceProgession = []
            
            for year in range(1, simulationYears+1):
            
                ### Update the balance based on each years progression
                balance = self.progressStochasticYear(balance, monthlyInvestment)                    
                             
                ### Now after each year we want to package the results
                balanceProgession.append({"year":year + self.conditions.age, "balance":balance, "realBalance":balance/((1+self.conditions.inflationRate) ** year)})
            
            ### Now we want to add our simulation to the results
            simulationResults.append(balanceProgession)
        
        ### Now lets crunch return our results
        return simulationResults
        
        
    
if __name__ == "__main__":
    
    def main1():
    
        tyler = IntialChoices(24,70000,50,0,0.1,0.2,0.08)
        engine = NetWorthEngine(tyler)
        
        networth,timeline = engine.calculateNetworth()
        
        print(f"Final Networth ${np.round(networth,2)}")
        
        
        years = [entry["year"] for entry in timeline]
        idealValues = [entry["networth"] for entry in timeline]
        realValues = [entry["realNetworth"] for entry in timeline]
        investmentValues = [entry["savings"] for entry in timeline]
        savingValues = [entry["investments"] for entry in timeline]


        plt.figure(figsize=(10, 6))
        plt.plot(years, idealValues, marker='o', linestyle='-', color='green')
        plt.plot(years, realValues, marker='o', linestyle='-', color='red')
        plt.plot(years, investmentValues, marker='o', linestyle='-', color='yellow')
        plt.plot(years, savingValues, marker='o', linestyle='-', color='blue')


        plt.title("Net Worth Progression Over Time")
        plt.legend(['Ideal Combined Total Networth', "Real (With Inflation)", "Investments (Ideal)", "Savings (Ideal)"])
        plt.xlabel("Age")
        plt.ylabel("Net Worth ($)")
        plt.grid(True)
        plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
        plt.tight_layout()
        plt.show()
        
    def main2():
        
        tyler = IntialChoices(20,70000,70, 4000, 0 , 0, 0.08)
        engine = NetWorthEngine(tyler)
        
        results = engine.monteCarloSim(1000)
        print("SIM DONE")

        
        for gen in results:
            
            ### Extract our data to list
            years = [x["year"] for x in gen]
            bal = [x["realBalance"] for x in gen]
            
            plt.plot(years, bal, marker='o', linestyle='-', color='green')
            
       
        plt.xlabel("Age")
        plt.ylabel("Portfollio Value ($)")
        plt.grid(True)
        plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
        plt.tight_layout()
        plt.show()
        
    def mainHG():
        
        tyler = IntialChoices(20,70000,70, 4000, 0 , 0, 0.08)
        engine = NetWorthEngine(tyler)
        
        results = engine.monteCarloSim(10000)
    
        finalBals = [np.round(res[-1]["balance"],2) for res in results]
                
        # Plot histogram
        plt.figure(figsize=(8,5))
        plt.hist(finalBals, bins=8, color='skyblue', edgecolor='black')
        plt.xlabel("Final Portfolio Value ($)")
        plt.ylabel("Frequency (log scale)")
        plt.title("Distribution of Final Balances")

        # Format y-axis with commas and x-axis as currency
        plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
        plt.yscale('log')
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        plt.tight_layout()
        plt.show()
        
    
    def mainND():
        
        tyler = IntialChoices(age = 20, salary= 600, retirementAge= 60, initalNetworth= 5000, savingPercentage= 0, investmentPercentage= 1, annualRetrun=0.08, marketVolatilaity=0.15)
        engine = NetWorthEngine(tyler)
        
        results = engine.monteCarloSim(10000)
    
        finalBals = np.array([(sim[-1])['balance'] for sim in results])
        
        mean = np.mean(finalBals)
        sd = np.std(finalBals)
        
        print(f"Mean: {mean}\nSTD: {sd}")
        print(norm.cdf(mean, loc = mean, scale = sd) * 100)
    
    def mainLogNorm():
        
        tyler = IntialChoices(age = 20, salary= 600, retirementAge= 60, initalNetworth= 5000, savingPercentage= 0, investmentPercentage= 1, annualRetrun=0.08, marketVolatilaity=0.15)
        engine = NetWorthEngine(tyler)
        
        results = engine.monteCarloSim(10000)
    
        finalBals = np.array([(sim[-1])['balance'] for sim in results])
        
        # Fit a lognormal distribution
        shape, loc, scale = lognorm.fit(finalBals, floc=0)  
        # shape = sigma (std dev of log), scale = exp(mu)

        # Get fitted parameters in more intuitive form
        mu = np.log(scale)       # mean of log(balances)
        sigma = shape            # std dev of log(balances)

        print(f"Lognormal fit parameters:")
        print(f"mu (log-space mean): {mu}")
        print(f"sigma (log-space std): {sigma}")
        print(f"Median final balance: {np.exp(mu):,.2f}")
        print(f"Mean final balance: {np.exp(mu + sigma**2 / 2):,.2f}")

        # Plot histogram of actual results
        plt.hist(finalBals, bins=50, density=True, alpha=0.6, color='skyblue')

        # Overlay fitted lognormal PDF
        x = np.linspace(min(finalBals), max(finalBals), 500)
        pdf_fitted = lognorm.pdf(x, shape, loc, scale)
        plt.plot(x, pdf_fitted, 'r-', lw=2, label='Fitted Lognormal PDF')

        plt.yscale('log')  # optional: makes skew easier to see
        plt.xlabel("Final Balance")
        plt.ylabel("Density (log scale)")
        plt.legend()
        plt.show()
        
    

    main2()
        
            
            


        
        
    
    
    

        














