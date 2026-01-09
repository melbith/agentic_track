# accounts.py
from datetime import datetime
from typing import Dict, List, Optional


def get_share_price(symbol: str) -> float:
    """Test implementation that returns fixed prices for specific symbols."""
    prices = {
        'AAPL': 150.0,
        'TSLA': 200.0,
        'GOOGL': 100.0
    }
    return prices.get(symbol, 0.0)


class Account:
    """Account management system for a trading simulation platform."""
    
    def __init__(self, initial_deposit: float) -> None:
        """Initialize a new user account with the initial deposit amount.
        
        Args:
            initial_deposit: The initial amount deposited into the account
        """
        self.initial_deposit = initial_deposit
        self.balance = initial_deposit
        self.holdings: Dict[str, int] = {}
        self.transaction_history: List[Dict] = []
        
        # Record initial deposit
        self._record_transaction(
            transaction_type='DEPOSIT',
            amount=initial_deposit
        )
    
    def deposit(self, amount: float) -> None:
        """Deposit a given amount into the user's account balance.
        
        Args:
            amount: The amount to deposit
        """
        self.balance += amount
        self._record_transaction(
            transaction_type='DEPOSIT',
            amount=amount
        )
    
    def withdraw(self, amount: float) -> bool:
        """Withdraw a given amount from the user's account balance.
        
        Args:
            amount: The amount to withdraw
            
        Returns:
            True if successful, False if withdrawal would lead to negative balance
        """
        if self.balance - amount < 0:
            return False
        
        self.balance -= amount
        self._record_transaction(
            transaction_type='WITHDRAWAL',
            amount=amount
        )
        return True
    
    def buy_shares(self, symbol: str, quantity: int) -> bool:
        """Buy a given quantity of shares of a specified symbol.
        
        Args:
            symbol: The stock symbol
            quantity: The number of shares to buy
            
        Returns:
            True if successful, False if insufficient balance
        """
        share_price = get_share_price(symbol)
        total_cost = share_price * quantity
        
        if self.balance < total_cost:
            return False
        
        self.balance -= total_cost
        
        if symbol in self.holdings:
            self.holdings[symbol] += quantity
        else:
            self.holdings[symbol] = quantity
        
        self._record_transaction(
            transaction_type='BUY',
            symbol=symbol,
            quantity=quantity,
            amount=total_cost
        )
        return True
    
    def sell_shares(self, symbol: str, quantity: int) -> bool:
        """Sell a given quantity of shares of a specified symbol.
        
        Args:
            symbol: The stock symbol
            quantity: The number of shares to sell
            
        Returns:
            True if successful, False if insufficient shares
        """
        if symbol not in self.holdings or self.holdings[symbol] < quantity:
            return False
        
        share_price = get_share_price(symbol)
        total_value = share_price * quantity
        
        self.balance += total_value
        self.holdings[symbol] -= quantity
        
        # Remove symbol from holdings if quantity is 0
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]
        
        self._record_transaction(
            transaction_type='SELL',
            symbol=symbol,
            quantity=quantity,
            amount=total_value
        )
        return True
    
    def get_portfolio_value(self) -> float:
        """Calculate and return the total value of the user's portfolio.
        
        Returns:
            Total value including cash balance and owned shares
        """
        total_value = self.balance
        
        for symbol, quantity in self.holdings.items():
            total_value += self._get_share_value(symbol)
        
        return total_value
    
    def get_profit_or_loss(self) -> float:
        """Calculate and return profit or loss.
        
        Returns:
            Difference between current portfolio value and initial deposit
        """
        return self.get_portfolio_value() - self.initial_deposit
    
    def get_holdings(self) -> Dict[str, int]:
        """Return current share holdings.
        
        Returns:
            Dictionary with symbols as keys and quantities as values
        """
        return self.holdings.copy()
    
    def get_transaction_history(self) -> List[Dict]:
        """Return list of all transactions.
        
        Returns:
            List of transaction records
        """
        return self.transaction_history.copy()
    
    def _record_transaction(self, transaction_type: str, symbol: str = "", 
                          quantity: int = 0, amount: float = 0.0) -> None:
        """Record a transaction in the account's transaction history.
        
        Args:
            transaction_type: Type of transaction (DEPOSIT, WITHDRAWAL, BUY, SELL)
            symbol: Stock symbol (for buy/sell transactions)
            quantity: Number of shares (for buy/sell transactions)
            amount: Transaction amount
        """
        transaction = {
            'timestamp': datetime.now(),
            'type': transaction_type,
            'symbol': symbol,
            'quantity': quantity,
            'amount': amount
        }
        self.transaction_history.append(transaction)
    
    def _get_share_value(self, symbol: str) -> float:
        """Calculate the total value of all shares held for a given symbol.
        
        Args:
            symbol: The stock symbol
            
        Returns:
            Total value of shares for the given symbol
        """
        if symbol not in self.holdings:
            return 0.0
        
        share_price = get_share_price(symbol)
        return share_price * self.holdings[symbol]