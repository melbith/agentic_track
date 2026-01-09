import gradio as gr
from accounts import Account

# Initialize account with a default deposit
account = None

def create_account(initial_deposit):
    global account
    try:
        account = Account(float(initial_deposit))
        return f"Account created with initial deposit: ${initial_deposit}"
    except Exception as e:
        return f"Error creating account: {str(e)}"

def deposit_funds(amount):
    global account
    if account is None:
        return "Please create an account first"
    try:
        account.deposit(float(amount))
        return f"Deposited ${amount}. New balance: ${account.balance:.2f}"
    except Exception as e:
        return f"Error: {str(e)}"

def withdraw_funds(amount):
    global account
    if account is None:
        return "Please create an account first"
    try:
        success = account.withdraw(float(amount))
        if success:
            return f"Withdrew ${amount}. New balance: ${account.balance:.2f}"
        else:
            return "Insufficient funds - withdrawal would result in negative balance"
    except Exception as e:
        return f"Error: {str(e)}"

def buy_shares(symbol, quantity):
    global account
    if account is None:
        return "Please create an account first"
    try:
        success = account.buy_shares(symbol.upper(), int(quantity))
        if success:
            return f"Bought {quantity} shares of {symbol}. New balance: ${account.balance:.2f}"
        else:
            return "Insufficient funds to buy shares"
    except Exception as e:
        return f"Error: {str(e)}"

def sell_shares(symbol, quantity):
    global account
    if account is None:
        return "Please create an account first"
    try:
        success = account.sell_shares(symbol.upper(), int(quantity))
        if success:
            return f"Sold {quantity} shares of {symbol}. New balance: ${account.balance:.2f}"
        else:
            return "Insufficient shares to sell"
    except Exception as e:
        return f"Error: {str(e)}"

def show_portfolio():
    global account
    if account is None:
        return "Please create an account first"
    
    portfolio_value = account.get_portfolio_value()
    profit_loss = account.get_profit_or_loss()
    holdings = account.get_holdings()
    
    result = f"Cash Balance: ${account.balance:.2f}\n"
    result += f"Total Portfolio Value: ${portfolio_value:.2f}\n"
    result += f"Profit/Loss: ${profit_loss:.2f}\n\n"
    result += "Holdings:\n"
    
    if holdings:
        for symbol, quantity in holdings.items():
            result += f"  {symbol}: {quantity} shares\n"
    else:
        result += "  No shares owned\n"
    
    return result

def show_transactions():
    global account
    if account is None:
        return "Please create an account first"
    
    transactions = account.get_transaction_history()
    
    if not transactions:
        return "No transactions yet"
    
    result = "Transaction History:\n"
    for txn in transactions:
        timestamp = txn['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
        txn_type = txn['type']
        
        if txn_type in ['BUY', 'SELL']:
            result += f"{timestamp} - {txn_type} {txn['quantity']} {txn['symbol']} for ${txn['amount']:.2f}\n"
        else:
            result += f"{timestamp} - {txn_type} ${txn['amount']:.2f}\n"
    
    return result

# Create Gradio interface
with gr.Blocks(title="Trading Account Manager") as demo:
    gr.Markdown("# Trading Account Management System")
    gr.Markdown("A simple demo for managing a trading account")
    
    with gr.Tab("Account Setup"):
        with gr.Row():
            initial_deposit_input = gr.Number(label="Initial Deposit ($)", value=10000)
            create_btn = gr.Button("Create Account")
        create_output = gr.Textbox(label="Status")
        create_btn.click(create_account, inputs=[initial_deposit_input], outputs=[create_output])
    
    with gr.Tab("Deposit/Withdraw"):
        with gr.Row():
            with gr.Column():
                deposit_amount = gr.Number(label="Deposit Amount ($)")
                deposit_btn = gr.Button("Deposit")
                deposit_output = gr.Textbox(label="Deposit Status")
            
            with gr.Column():
                withdraw_amount = gr.Number(label="Withdraw Amount ($)")
                withdraw_btn = gr.Button("Withdraw")
                withdraw_output = gr.Textbox(label="Withdraw Status")
        
        deposit_btn.click(deposit_funds, inputs=[deposit_amount], outputs=[deposit_output])
        withdraw_btn.click(withdraw_funds, inputs=[withdraw_amount], outputs=[withdraw_output])
    
    with gr.Tab("Trade Shares"):
        gr.Markdown("Available symbols: AAPL ($150), TSLA ($200), GOOGL ($100)")
        
        with gr.Row():
            with gr.Column():
                buy_symbol = gr.Textbox(label="Symbol to Buy", placeholder="AAPL")
                buy_quantity = gr.Number(label="Quantity", value=1)
                buy_btn = gr.Button("Buy Shares")
                buy_output = gr.Textbox(label="Buy Status")
            
            with gr.Column():
                sell_symbol = gr.Textbox(label="Symbol to Sell", placeholder="AAPL")
                sell_quantity = gr.Number(label="Quantity", value=1)
                sell_btn = gr.Button("Sell Shares")
                sell_output = gr.Textbox(label="Sell Status")
        
        buy_btn.click(buy_shares, inputs=[buy_symbol, buy_quantity], outputs=[buy_output])
        sell_btn.click(sell_shares, inputs=[sell_symbol, sell_quantity], outputs=[sell_output])
    
    with gr.Tab("Portfolio & History"):
        with gr.Row():
            portfolio_btn = gr.Button("Show Portfolio")
            transactions_btn = gr.Button("Show Transactions")
        
        portfolio_output = gr.Textbox(label="Portfolio Summary", lines=10)
        transactions_output = gr.Textbox(label="Transaction History", lines=10)
        
        portfolio_btn.click(show_portfolio, outputs=[portfolio_output])
        transactions_btn.click(show_transactions, outputs=[transactions_output])

if __name__ == "__main__":
    demo.launch()