import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import date

risk_free_rate = 0.5

class capm:
    def __init__(self,stocks,start,end):
        self.stocks = stocks
        self.start = start
        self.end = end
    def download(self):
        data = {}
        print("Current portfolio is ",self.stocks)
        for stock in self.stocks:
            ticker = yf.download(stock,self.start,self.end)
            data[stock] = ticker['Adj Close']

        df = pd.DataFrame(data)

        print(pd.DataFrame(data))
        df.plot()
        return pd.DataFrame(data)


    def initialize(self):
        stock_data = self.download()
        print("\n resampling monthly basis \n")
        stock_data = stock_data.resample('M').last()
        print(stock_data)
        self.data = pd.DataFrame({'Stock_returns':stock_data[self.stocks[0]],'Adjusted_closing_prices':stock_data[self.stocks[1]]})
        print(self.data)
        print("\n logarthmic monthly return \n")
        self.data[['Stock_log_returns','monthly_returns']] = np.log(self.data[['Stock_returns','Adjusted_closing_prices']]/self.data[['Stock_returns','Adjusted_closing_prices']].shift(1))
        self.data = self.data[1:]
        print(self.data)

    def calculate_beta(self):
        matrix = self.data['Stock_log_returns'],self.data['monthly_returns']
        print(matrix)
        print(np.cov(matrix))
        cov_matrix = np.cov(self.data['Stock_log_returns'],self.data['monthly_returns'])
        print(cov_matrix)
        beta = cov_matrix[0,1]/cov_matrix[1,1]
        print("***************************************")
        print("******************************************")
        print("The beta value is ",beta)
        print("*******************************************")
        print("*********************************************")
        print("\n-Note::\n Beta = 1(Stocks moving with market)\nBETA > 1(Stock more volatile than market)\n BETA < 1(Stock less volatile than market)")

    def regression(self):
        beta,alpha = np.polyfit(self.data['Stock_log_returns'],self.data['monthly_returns'],deg=1)
        print("Beta from polyfit regression is ",beta)
        expected_return = risk_free_rate + beta * (self.data['Stock_log_returns'].mean()*12 - risk_free_rate)
        print("Expected return as per regressio ",expected_return)
        self.plot_regression(alpha,beta)

    def plot_regression(self,alpha,beta):
        fig,axis = plt.subplots(1,figsize=(20,10))
        axis.scatter(self.data['Stock_log_returns'],self.data['monthly_returns'],label = 'Data points')
        axis.plot(self.data['Stock_log_returns'],beta * self.data['Stock_log_returns']+alpha,color='red')
        plt.title('Capital asses pricing model')
        plt.xlabel('Market return')
        plt.ylabel('Stock return')
        #plt.legend()
        plt.grid(True)
        plt.show()
        plt.legend()


if __name__ == '__main__':
    stocks = []
    a = input("Enter stock needed to be validated ")
    stocks.append(a)
    stocks.append('^GSPC')
    print(stocks)
    capm = capm(stocks,date(2005,1,1),date(2022,12,9))
    capm.initialize()
    capm.calculate_beta()
    capm.regression()