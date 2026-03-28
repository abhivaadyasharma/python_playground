# Author: Abhivaadya Sharma

import logging
from datetime import datetime

class CurrencyConverter:
    """Class for currency conversion using exchange rates."""
    
    exchange_rates = {
        'INR': 1,  # Base currency is INR (Indian Rupee)
        'USD': 74.0,
        'EUR': 88.0,
        'GBP': 100.0,
        'AUD': 55.0
    }
    
    @staticmethod
    def convert(amount, from_currency, to_currency):
        """Convert amount from one currency to another."""
        if from_currency == to_currency:
            return amount
        # Convert the amount to INR first, then convert to the target currency
        amount_in_inr = amount * CurrencyConverter.exchange_rates[from_currency]
        return amount_in_inr / CurrencyConverter.exchange_rates[to_currency]

class CEO:
    def add_product(self, product_name, cost_price, selling_price, category=None, region=None, currency='INR'):
        """Add a product to the catalog with cost and selling prices."""
        self.products[product_name] = {
            'cost_price': cost_price,
            'selling_price': selling_price,
            'category': category,
            'region': region,
            'currency': currency
        }
        print(f"Added product {product_name} with cost: {cost_price} {currency} and selling price: {selling_price} {currency}.")

    def profitability_analysis(self, by='product', currency='INR'):
        """Analyze profitability by product, category, or region."""
        if by == 'product':
            print("Profitability Analysis by Product:")
            for product_name, details in self.products.items():
                # Convert to the required currency
                cost_price = CurrencyConverter.convert(details['cost_price'], details['currency'], currency)
                selling_price = CurrencyConverter.convert(details['selling_price'], details['currency'], currency)
                
                profit = selling_price - cost_price
                profit_margin = (profit / selling_price) * 100
                print(f"{product_name} - Profit: {profit:.2f} {currency}, Profit Margin: {profit_margin:.2f}%")


# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Chatbot class
class Chatbot:
    """Simple Chatbot for customer queries and support."""
    
    def __init__(self):
        self.responses = {
            "what is your name": "I am your friendly support bot.",
            "how can I contact support": "You can contact support via email at support@yahoo.com.",
            "what products do you offer": "We offer a wide range of products including electronics, home appliances, and more.",
            "how do I return a product": "You can return a product by visiting our Returns page or contacting our customer support.",
            "what is the currency conversion rate": "The current exchange rates are:\n1 USD = 74 INR, 1 EUR = 88 INR, etc.",
            "how can I track my order": "Please enter your order ID on our tracking page to check the status of your order."
        }

        # Sample order status for tracking
        self.order_status = {
            "12345": "Shipped - Expected delivery: 3 days",
            "67890": "Processing - Expected shipment: 1 day",
            "11223": "Delivered - Order completed on 2025-03-17",
            "44556": "Cancelled - Order was cancelled due to payment issues"
        }

    def respond(self, query):
        """Generate a response based on the customer query."""
        query = query.lower()
        
        # Check if the query is about order tracking
        if "track my order" in query or "order status" in query:
            order_id = self.extract_order_id(query)
            if order_id and order_id in self.order_status:
                return f"Order {order_id} status: {self.order_status[order_id]}"
            return "Sorry, I couldn't find an order with that ID. Please check the ID and try again."

        # Handle other queries
        for keyword, response in self.responses.items():
            if keyword in query:
                return response
        return "Sorry, I didn't understand that. Could you please clarify?"

    def extract_order_id(self, query):
        """Extract order ID from the query (assuming format like 'order ID 12345')."""
        words = query.split()
        for word in words:
            if word.isdigit() and len(word) == 5:  # Assuming order IDs are 5 digits
                return word
        return None

class DevelopmentTeam:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def login(self, username, password):
        """Authenticate development team login."""
        if self.username == username and self.password == password:
            return True
        return False

    def send_code(self):
        """Send code to the system."""
        print("Code has been sent to the system.")


class CEO:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.managers = []  # List of Manager objects
        self.development_team = []  # List of DevelopmentTeam members
        self.products = {}  # Product catalog with cost price and selling price

    def login(self, username, password):
        """Authenticate CEO login."""
        if self.username == username and self.password == password:
            return True
        return False

    def hire_manager(self, name, username, password):
        """Hire a new sales manager."""
        manager = Manager(username, password)
        self.managers.append(manager)
        print(f"Hired {name} as a Manager.")

    def fire_manager(self, username):
        """Fire an existing sales manager."""
        for manager in self.managers:
            if manager.username == username:
                self.managers.remove(manager)
                print(f"Fired manager {username}.")
                return
        print("Manager not found.")

    def hire_development_team(self, name, username, password):
        """Hire a new development team member."""
        dev = DevelopmentTeam(username, password)
        self.development_team.append(dev)
        print(f"Hired {name} as a Development Team member.")

    def fire_development_team(self, username):
        """Fire an existing development team member."""
        for dev in self.development_team:
            if dev.username == username:
                self.development_team.remove(dev)
                print(f"Fired development team member {username}.")
                return
        print("Development team member not found.")

    def view_company_performance(self):
        """View overall company performance."""
        print("Company Performance:")
        for manager in self.managers:
            manager.view_performance()

    def add_product(self, product_name, cost_price, selling_price, category=None, region=None):
        """Add a product to the catalog with cost and selling prices."""
        self.products[product_name] = {
            'cost_price': cost_price,
            'selling_price': selling_price,
            'category': category,
            'region': region
        }
        print(f"Added product {product_name} with cost: {cost_price} Rs and selling price: {selling_price} Rs.")

    def profitability_analysis(self, by='product'):
        """Analyze profitability by product, category, or region."""
        if by == 'product':
            print("Profitability Analysis by Product:")
            for product_name, details in self.products.items():
                profit = details['selling_price'] - details['cost_price']
                profit_margin = (profit / details['selling_price']) * 100
                print(f"{product_name} - Profit: {profit} Rs, Profit Margin: {profit_margin:.2f}%")
        
        elif by == 'category':
            print("Profitability Analysis by Category:")
            categories = {}
            for product_name, details in self.products.items():
                category = details['category']
                if category not in categories:
                    categories[category] = []
                profit = details['selling_price'] - details['cost_price']
                categories[category].append(profit)

            for category, profits in categories.items():
                total_profit = sum(profits)
                average_profit_margin = (total_profit / len(profits)) / self.products[product_name]['selling_price'] * 100
                print(f"Category: {category} - Total Profit: {total_profit} Rs, Average Profit Margin: {average_profit_margin:.2f}%")

        elif by == 'region':
            print("Profitability Analysis by Region:")
            regions = {}
            for product_name, details in self.products.items():
                region = details['region']
                if region not in regions:
                    regions[region] = []
                profit = details['selling_price'] - details['cost_price']
                regions[region].append(profit)

            for region, profits in regions.items():
                total_profit = sum(profits)
                average_profit_margin = (total_profit / len(profits)) / self.products[product_name]['selling_price'] * 100
                print(f"Region: {region} - Total Profit: {total_profit} Rs, Average Profit Margin: {average_profit_margin:.2f}%")
        
        else:
            print("Invalid option for profitability analysis. Please choose 'product', 'category', or 'region'.")


class Manager:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.sales_men = []  # List of SalesMan objects
        self.items = []  # Items in stock to add/manage

    
    def set_sales_goal(self, username, goal):
        """Set a sales goal for a specific salesman."""
        for salesman in self.sales_men:
            if salesman.username == username:
                salesman.set_goal(goal)
                print(f"Set sales goal of {goal} items for {username}.")
                return
        print(f"Salesman {username} not found.")

    def login(self, username, password):
        """Authenticate manager login."""
        if self.username == username and self.password == password:
            return True
        return False

    def add_item(self, item_name, qty):
        """Add items to stock."""
        self.items.append({'item_name': item_name, 'quantity': qty})
        print(f"Added item: {item_name} with {qty} units.")

    def update_item(self, item_name, new_qty):
        """Update the stock quantity for an item."""
        for item in self.items:
            if item['item_name'] == item_name:
                item['quantity'] = new_qty
                print(f"Updated {item_name} to {new_qty} units.")
                return
        print(f"Item {item_name} not found in stock.")

    def remove_item(self, item_name):
        """Remove an item from stock."""
        for item in self.items:
            if item['item_name'] == item_name:
                self.items.remove(item)
                print(f"Removed {item_name} from stock.")
                return
        print(f"Item {item_name} not found in stock.")

    def view_sales(self):
        """View sales report for each salesman."""
        print("Sales report:")
        for salesman in self.sales_men:
            total_sales = salesman.total_sales()  # Total items sold
            commission = salesman.calculate_commission()
            print(f"{salesman.username}: Sold {total_sales} items. Commission: {commission} Rs.")

    def view_performance(self):
        """View performance of each salesman."""
        print("Salesman performance:")
        for salesman in self.sales_men:
            total_sales = salesman.total_sales()
            commission = salesman.calculate_commission()
            print(f"{salesman.username}: Total Sales = {total_sales}, Commission = {commission} Rs.")

    def pay_salary(self):
        """Calculate and pay salaries to all salesmen based on sales."""
        for salesman in self.sales_men:
            total_sales = salesman.total_sales()  # Total items sold
            salary = total_sales * 1000  # 1000 Rs per item sold
            salesman.receive_salary(salary)
            print(f"Paid {salesman.username} {salary} Rs for {total_sales} items sold.")

    def hire_salesman(self, name, username, password):
        """Hire a new salesman."""
        salesman = SalesMan(username, password, {})
        self.sales_men.append(salesman)
        print(f"Hired {name} as a salesman.")

    def fire_salesman(self, username):
        """Fire an existing salesman."""
        for salesman in self.sales_men:
            if salesman.username == username:
                self.sales_men.remove(salesman)
                print(f"Fired salesman {username}.")
                return
        print("Salesman not found.")

    def send_notification_to_salesmen(self, message):
        """Send notifications to all salesmen."""
        for salesman in self.sales_men:
            salesman.receive_notification(message)

    def send_performance_notification(self):
        """Send a notification about the performance of each salesman."""
        for salesman in self.sales_men:
            total_sales = salesman.total_sales()
            if total_sales > 50:  # Example goal for good performance
                message = f"Great job, {salesman.username}! You've sold {total_sales} items."
            else:
                message = f"Keep pushing, {salesman.username}! You sold {total_sales} items."
            salesman.receive_notification(message)

    def view_team_leaderboard(self):
        """Display leaderboard showing sales performance by salesman."""
        leaderboard = []
        for salesman in self.sales_men:
            total_sales = salesman.total_sales()
            commission = salesman.calculate_commission()
            leaderboard.append({
                'username': salesman.username,
                'total_sales': total_sales,
                'commission': commission
            })

        # Sort the leaderboard by total sales (descending)
        leaderboard.sort(key=lambda x: x['total_sales'], reverse=True)

        print("Team Leaderboard:")
        for index, entry in enumerate(leaderboard, start=1):
            print(f"{index}. {entry['username']} - Sold: {entry['total_sales']} items, Commission: {entry['commission']} Rs.")


class SalesMan:
    def __init__(self, username, password, stock):
        self.username = username
        self.password = password
        self.stock = stock  # Stock is a dictionary of items and their quantities
        self.sales = {}  # Track sales made (item: quantity sold)
        self.rough_sheet = []  # Rough Sheet to track products sold (product, quantity, date)
        self.sales_target = 0  # Sales target for the salesman
        self.notifications = []  # To keep track of notifications for the salesman
        self.feedback = []  # To store feedback from customers

    def login(self, username, password):
        """Authenticate user login."""
        if self.username == username and self.password == password:
            return True
        return False

    def view_items(self):
        """View available items for sale."""
        print("Items available for sale:")
        for item, qty in self.stock.items():
            print(f"{item}: {qty} in stock")

    def sell_item(self, item, qty_sold):
        """Sell an item and track the sale."""
        if item in self.stock and self.stock[item] >= qty_sold:
            self.stock[item] -= qty_sold
            self.sales[item] = self.sales.get(item, 0) + qty_sold
            # Record the sale in the rough sheet
            sale_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.rough_sheet.append({'item': item, 'quantity': qty_sold, 'date': sale_date})
            logging.info(f"Sold {qty_sold} {item} by {self.username}. Remaining stock: {self.stock[item]}")
            return True
        logging.error(f"Not enough stock for {item}. Sale failed.")
        return False

    def return_item(self, item, qty_returned):
        """Handle product returns and update stock."""
        if item in self.sales and self.sales[item] >= qty_returned:
            self.sales[item] -= qty_returned
            self.stock[item] += qty_returned
            # Record the return in the rough sheet
            return_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.rough_sheet.append({'item': item, 'quantity': -qty_returned, 'date': return_date})
            logging.info(f"Returned {qty_returned} {item} by {self.username}. Updated stock: {self.stock[item]}")
            return True
        logging.error(f"Return failed: Not enough items sold or invalid product.")
        return False

    def total_sales(self):
        """Calculate total sales made by the salesman."""
        return sum(self.sales.values())

    def calculate_commission(self, commission_rate=0.05):
        """Calculate commission based on sales."""
        total_sales = self.total_sales()
        commission = total_sales * commission_rate
        print(f"{self.username} earned a commission of {commission} Rs.")
        return commission

    def receive_salary(self, salary):
        """Receive salary after sales."""
        print(f"{self.username} received salary: {salary} Rs")

    def reset_password(self, new_password):
        """Allow salesmen to reset their password."""
        self.password = new_password
        print(f"{self.username}'s password has been updated.")

    def receive_notification(self, message):
        """Receive notifications (for sales, updates, etc.)."""
        self.notifications.append(message)
        print(f"Notification for {self.username}: {message}")

    def view_rough_sheet(self):
        """View the rough sheet of sales for the salesman."""
        print(f"Rough Sheet for {self.username}:")
        if not self.rough_sheet:
            print("No sales or returns recorded yet.")
        else:
            for record in self.rough_sheet:
                action = "Sold" if record['quantity'] > 0 else "Returned"
                print(f"{action} {abs(record['quantity'])} {record['item']} on {record['date']}")

    def set_sales_target(self, target):
        """Set a sales target for the salesman."""
        self.sales_target = target
        print(f"Sales target set to {target} items for {self.username}.")

    def track_sales_target(self):
        """Track progress towards the sales target."""
        sold = self.total_sales()
        if sold >= self.sales_target:
            print(f"{self.username} has reached the sales target of {self.sales_target} items!")
        else:
            print(f"{self.username} has sold {sold}/{self.sales_target} items. Keep going!")

    def collect_feedback(self):
        """Collect customer feedback on products and sales experience."""
        product_feedback = input("Enter feedback for the product: ")
        sales_experience_feedback = input("Enter feedback on the sales experience: ")
        feedback_entry = {
            'product_feedback': product_feedback,
            'sales_experience_feedback': sales_experience_feedback,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.feedback.append(feedback_entry)
        print("Feedback collected successfully!")

    def view_feedback(self):
        """View the collected feedback."""
        print(f"Feedback collected by {self.username}:")
        if not self.feedback:
            print("No feedback collected yet.")
        else:
            for entry in self.feedback:
                print(f"Product Feedback: {entry['product_feedback']}")
                print(f"Sales Experience Feedback: {entry['sales_experience_feedback']}")
                print(f"Timestamp: {entry['timestamp']}\n")


def main():
    # Initialize app data
    ceo = CEO("ceo_username", "ceo_password")
    manager = Manager("manager_username", "manager_password")
    developer = DevelopmentTeam("dev_username", "dev_password")
    chatbot = Chatbot()  # Initialize chatbot instance

    # Assign manager and developer to CEO
    ceo.managers.append(manager)
    ceo.development_team.append(developer)

    # Sample SalesMan creation by Manager
    salesman = SalesMan("salesman_username", "salesman_password", {'item1': 100, 'item2': 50})
    manager.sales_men.append(salesman)

    # User input loop
    while True:
        print("\nLogin as:\n1. SalesMan\n2. Manager\n3. Development Team\n4. CEO\n5. Chatbot (Customer Support)\n6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            for salesman in manager.sales_men:
                if salesman.login(username, password):
                    print("Logged in as SalesMan.")
                    salesman.view_items()
                    item = input("Enter item to sell: ")
                    qty = int(input("Enter quantity to sell: "))
                    salesman.sell_item(item, qty)
                    salesman.track_sales_target()
                    break
            else:
                print("Invalid login!")

        elif choice == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            if manager.login(username, password):
                print("Logged in as Manager.")
                action = input("1. Add Item\n2. View Sales\n3. Pay Salary\n4. Hire SalesMan\n5. Fire SalesMan\n6. Send Notification\n7. View Performance\n")
                if action == '1':
                    item_name = input("Enter item name: ")
                    qty = int(input("Enter quantity: "))
                    manager.add_item(item_name, qty)
                elif action == '2':
                    manager.view_sales()
                elif action == '3':
                    manager.pay_salary()
                elif action == '4':
                    name = input("Enter SalesMan name: ")
                    username = input("Enter username: ")
                    password = input("Enter password: ")
                    manager.hire_salesman(name, username, password)
                elif action == '5':
                    username = input("Enter SalesMan username to fire: ")
                    manager.fire_salesman(username)
                elif action == '6':
                    message = input("Enter notification message: ")
                    manager.send_notification_to_salesmen(message)
                elif action == '7':
                    manager.view_performance()
            else:
                print("Invalid login!")

        elif choice == '3':
            username = input("Enter username: ")
            password = input("Enter password: ")
            if developer.login(username, password):
                print("Logged in as Development Team.")
                developer.send_code()
            else:
                print("Invalid login!")

        elif choice == '4':
            username = input("Enter username: ")
            password = input("Enter password: ")
            if ceo.login(username, password):
                print("Logged in as CEO.")
                ceo.view_company_performance()
            else:
                print("Invalid login!")

        elif choice == '5':  # Customer Support / Chatbot
            print("\nWelcome to our Customer Support Chatbot!")
            while True:
                customer_query = input("Ask me something (type 'exit' to end): ")
                if customer_query.lower() == 'exit':
                    print("Thank you for using the chatbot. Have a great day!")
                    break
                response = chatbot.respond(customer_query)  # Process query in chatbot
                print(response)

        elif choice == '6':
            print("Exiting...")
            print ("Have a good day!")
            break

        else:
            print ("Invalid choice!!!")

# Run the program
if __name__ == "__main__":
    main()