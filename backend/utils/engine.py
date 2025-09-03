from copy import deepcopy as dp
import numpy as np
### A class that wraps all simulation conditions nicely into one object

class SimulationConditions:
        
    def __init__(self, startingBalance, monthlyInvestment, monthlySavings, avgMarket = 0.08, avgVol = 0.15, avgInflation = 0.03):
        
        self.principle = startingBalance
        self.monthlyInv = monthlyInvestment
        self.monthlySav = monthlySavings
        self.marketReturn = avgMarket
        self.avgVol = avgVol
        self.avgInf = avgInflation
    
    def monteCarloSim(self, simulationCount:int , duration: int):
    
        ### Creates an array of balances
        balances = np.zeros((simulationCount, duration))
        
        ### Real balances are injusted for inflation
        realBalances = np.zeros((simulationCount, duration))

        ### Assigns the starting balance to each simulation
        balances[:, 0] = self.principle
        realBalances[:, 0] = self.principle
        
        ### Creates a random matrix of return values for each year in each sim, same shape as balance matrix.
        ### np.random.normal picks a values random from the normal distribituon of the avg market return and volaitliy
        ### it adds 1, to account for the balance being scaled
        
        returns = 1 + np.random.normal(self.marketReturn, self.avgVol, size=(simulationCount, duration))

        ### For each year
        for year in range(1,duration):
            
            ### First if there are monthly contributions add them to the year
            if self.monthlyInv > 0:
                balances[:,year - 1] += (self.monthlyInv * 12)
            
            ### For each balance in each sim multiply by the corresponding yearly return in the return matrix
            balances[:,year] = balances[:,year - 1] * returns[:, year-1]

        ### If there is a inflation rate then create an inflation factor 
        inflation_factor = (1 + self.avgInf) ** np.arange(duration)  # 1.0, 1.03, 1.03^2, ...
        
        ### Multiply each balence per year by the corresponding compoudning inflation :( 
        realBalances = balances / inflation_factor  # elementwise division, auto-broadcast

        return balances[:, -1], realBalances[:,-1], balances, realBalances
    
    def JSONFY(self, results, stats):
        
        # Convert to list before jsonify
        data = {
            "Final_Bals": results[0].tolist(),
            "Real_Final_Bals": results[1].tolist(),
            "Bals": results[2].tolist(),
            "Real_Bals": results[3].tolist(),
        }
        
        package = {
            "DataPoints" : data,
            "Stats" : stats,
            "Error" : False
        }  
        
        return package
    
    def calcStats(self, results, simDuration):
        
        fbals, frealbals, bals, realbals = results
        totalInvestment = self.principle + (self.monthlyInv * 12 * simDuration)
        
        stats = {
            "Median_Final" : np.round(np.median(fbals),2),
            "Median_Gain" : np.round(np.median(fbals - totalInvestment),2),
            "Average_Final" : np.round(np.mean(fbals),2),
            "STD_Final": np.round(np.std(fbals), 2),
            "Max_Final" : np.round(np.max(fbals),2),
            "Min_Final" : np.round(np.min(fbals),2),
        }
        
        return stats
        
        



def testing():
    Tyler = SimulationConditions(0, 500, 0, avgMarket=0.08)
    simDuration = 30

    finalBalances, realFinalBalances, balances, realbalences = monteCarloSim(Tyler, 10000, simDuration)
    totalInvestment = Tyler.principle + (Tyler.monthlyInv * 12 * simDuration)

    print(f"""
        
        Starting Bal: ${Tyler.principle}
        Monthly Investment: ${Tyler.monthlyInv}
        Total Invested: ${totalInvestment}
        
        Median Total Nominal Realized Gain: ${np.round(np.median(finalBalances - totalInvestment),2)}
        Median Total Real Realized Gain: ${np.round(np.median(realFinalBalances - totalInvestment),2)}

        Nominal Median Final Bal: ${np.round(np.median(finalBalances),2)}
        Nominal Max Final Bal: ${np.round(np.max(finalBalances),2)} 
        Nominal Min Final Bal: ${np.round(np.min(finalBalances),2)}
        
        Real Median Final Bal: ${np.round(np.median(realFinalBalances),2)}
        Real Max Final Bal: ${np.round(np.max(realFinalBalances),2)} 
        Real Min Final Bal: ${np.round(np.min(realFinalBalances),2)}
        
        """)
