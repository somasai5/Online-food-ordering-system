import streamlit as st
import os

# ==================== MENU ITEM CLASS ====================

class MenuItem:
    def __init__(self, item_id=0, name="", category="", price=0.0, available=True):
        self.item_id = item_id
        self.name = name
        self.category = category
        self.price = price
        self.available = available

    def display_row(self):
        status = "Available" if self.available else "Not Available"
        return [self.item_id, self.name, self.category, f"{self.price:.2f}", status]

    @staticmethod
    def from_string(line: str):
        parts = line.strip().split(",")
        if len(parts) < 5:
            return None
        item_id = int(parts[0])
        name = parts[1]
        category = parts[2]
        price = float(parts[3])
        available = parts[4].strip() == "1"
        return MenuItem(item_id, name, category, price, available)


# ==================== ORDER ITEM CLASS ====================

class OrderItem:
    def __init__(self, menu_item: MenuItem, quantity: int):
        self.menu_item = menu_item
        self.quantity = quantity

    def get_subtotal(self):
        return self.menu_item.price * self.quantity

    def to_row(self):
        return [
            self.menu_item.name,
            self.quantity,
            f"{self.menu_item.price:.2f}",
            f"{self.get_subtotal():.2f}",
        ]


# ==================== ORDER CLASS ====================

class Order:
    def __init__(self, order_id=0, customer_name=""):
        self.order_id = order_id
        self.customer_name = customer_name
        self.items = []
        self.status = "Pending"
        self.total_amount = 0.0

    def add_item(self, order_item: OrderItem):
        self.items.append(order_item)
        self.calculate_total()

    def calculate_total(self):
        self.total_amount = sum(item.get_subtotal() for item in self.items)

    def get_order_id(self):
        return self.order_id

    def get_customer_name(self):
        return self.customer_name

    def get_total_amount(self):
        return self.total_amount

    def set_status(self, status: str):
        self.status = status

    def bill_text(self):
        lines = []
        lines.append("=========== BILL ===========")
        lines.append(f"Order ID : {self.order_id}")
        lines.append(f"Customer : {self.customer_name}")
        lines.append(f"Status   : {self.status}")
        lines.append("------------------------------")
        lines.append(f"{'Item':<25}{'Qty':<10}{'Price':<10}{'Subtotal':<10}")
        lines.append("------------------------------")
        for it in self.items:
            lines.append(
                f"{it.menu_item.name:<25}{it.quantity:<10}{it.menu_item.price:<10.2f}{it.get_subtotal():<10.2f}"
            )
        lines.append("------------------------------")
        lines.append(f"Total: Rs. {self.total_amount:.2f}")
        lines.append("==============================")
        return "\n".join(lines)


# ==================== MENU CLASS ====================

class Menu:
    def __init__(self, filename="menu.txt"):
        self.items = []
        self.filename = filename
        self.load_from_file()

    def load_from_file(self):
        self.items.clear()
        if not os.path.exists(self.filename):
            st.error(" menu.txt not found. System cannot load menu.")
            return
        with open(self.filename, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                item = MenuItem.from_string(line)
                if item:
                    self.items.append(item)

    def display_table_data(self):
        table = []
        for item in self.items:
            table.append(item.display_row())
        return table

    def find_item(self, item_id: int):
        for item in self.items:
            if item.item_id == item_id:
                return item
        return None


# ==================== QUEUE (LINKED LIST) ====================

class QueueNode:
    def __init__(self, order: Order):
        self.order = order
        self.next = None


class OrderQueue:
    def __init__(self):
        self.front = None
        self.rear = None

    def enqueue(self, order: Order):
        node = QueueNode(order)
        if self.rear is None:
            self.front = self.rear = node
        else:
            self.rear.next = node
            self.rear = node

    def dequeue(self):
        if self.front is None:
            return Order()
        temp = self.front
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        removed_order = temp.order
        del temp
        return removed_order

    def to_list(self):
        result = []
        temp = self.front
        while temp is not None:
            result.append(temp.order)
            temp = temp.next
        return result


# ==================== STACK ====================

class OrderStack:
    def __init__(self):
        self.stack = []

    def push(self, order: Order):
        self.stack.append(order)

    def pop(self):
        if not self.stack:
            return Order()
        return self.stack.pop()

    def to_list(self):
        # top element first
        return list(reversed(self.stack))


# ==================== CUSTOMER ====================

class Customer:
    def __init__(self, name: str, menu: Menu):
        self.name = name
        self.menu = menu

    def place_order_from_quantities(self, qty_map, order_id: int):
        order = Order(order_id, self.name)
        for item in self.menu.items:
            qty = qty_map.get(item.item_id, 0)
            if qty > 0 and item.available:
                order.add_item(OrderItem(item, qty))
        if not order.items:
            return Order()
        return order


# ==================== SECURE ADMIN ====================

class Admin:
    def __init__(self, menu: Menu, filename="admin.txt"):
        self.menu = menu
        self.username = ""
        self.password = ""
        self.filename = filename
        self.load_credentials()

    def load_credentials(self):
        if not os.path.exists(self.filename):
            st.error("admin.txt missing! The system will exit.")
            st.stop()
        with open(self.filename, "r") as f:
            self.username = f.readline().strip()
            self.password = f.readline().strip()

    def check_login(self, u, p):
        return (u == self.username and p == self.password)


# ==================== HELPERS ====================

def save_order_to_file(order: Order, filename="orders.txt"):
    if not order.items:
        return
    with open(filename, "a") as f:
        line = f"OrderID:{order.order_id},Name:{order.customer_name},Total:{order.total_amount:.2f},Status:{order.status}\n"
        f.write(line)


# ==================== STREAMLIT APP ====================

# Initialize session state on first run
if "menu" not in st.session_state:
    st.session_state.menu = Menu()

if "order_queue" not in st.session_state:
    st.session_state.order_queue = OrderQueue()

if "history" not in st.session_state:
    st.session_state.history = OrderStack()

if "order_id_counter" not in st.session_state:
    st.session_state.order_id_counter = 1

if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

menu_obj: Menu = st.session_state.menu
queue_obj: OrderQueue = st.session_state.order_queue
history_obj: OrderStack = st.session_state.history

st.title("Online Food Ordering System (Python + Streamlit + DS)")

page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Customer",
        "Admin",
        "Process Next Order",
        "Pending Orders (Queue)",
        "Delivered Orders (Stack)",
        "Undo Last Delivery",
    ],
)

# -------------------- HOME --------------------
if page == "Home":
    st.header("Welcome ")
    st.write(
        """
This is an Online Food Ordering System implemented in Python using Streamlit for the web interface and custom data structures for order management.

- Uses **Queue (OrderQueue)** for pending orders  
- Uses **Stack (OrderStack)** for delivered orders  
- Uses **MenuItem / Order / OrderItem** classes for menu and order representation 
- Reads **menu.txt** and **admin.txt** files  
    """
    )

# -------------------- CUSTOMER --------------------
elif page == "Customer":
    st.header(" Customer Panel")

    customer_name = st.text_input("Enter your name")
    if customer_name:
        st.subheader("Menu")
        table_data = menu_obj.display_table_data()
        if table_data:
            import pandas as pd
            df = pd.DataFrame(
                table_data, columns=["ID", "Name", "Category", "Price", "Status"]
            )
            st.table(df)
        else:
            st.warning("Menu is empty.")

        st.subheader("Select quantities")
        qty_map = {}
        cols = st.columns(2)
        for idx, item in enumerate(menu_obj.items):
            with cols[idx % 2]:
                if item.available:
                    qty = st.number_input(
                        f"{item.name} (Rs.{item.price:.2f})",
                        min_value=0,
                        step=1,
                        key=f"qty_{item.item_id}",
                    )
                    qty_map[item.item_id] = qty
                else:
                    st.text(f"{item.name} (Not Available)")

        if st.button("Place Order"):
            customer = Customer(customer_name, menu_obj)
            order_id = st.session_state.order_id_counter
            order = customer.place_order_from_quantities(qty_map, order_id)
            if order.get_order_id() == 0 or not order.items:
                st.error("No items selected, order not created.")
            else:
                # add to queue
                queue_obj.enqueue(order)
                st.session_state.order_id_counter += 1
                # show bill
                st.success("Order placed successfully! Here is your bill:")
                st.code(order.bill_text())
                save_order_to_file(order)

# -------------------- ADMIN --------------------
elif page == "Admin":
    st.header(" Admin Panel")

    admin = Admin(menu_obj)

    # Check Login
    if not st.session_state.admin_logged_in:
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")

        if st.button("Login"):
            if admin.check_login(u, p):
                st.session_state.admin_logged_in = True
                st.success("Login Successful!")
            else:
                st.error("Wrong Credentials!")

    else:
        st.success("Logged in as Admin")

        # Show menu
        st.subheader(" Menu Items")
        import pandas as pd
        df = pd.DataFrame(menu_obj.display_table_data(),
                          columns=["ID", "Name", "Category", "Price", "Status"])
        st.table(df)

        st.markdown("---")
        st.subheader("➕ Add New Menu Item")

        new_id = st.number_input("Enter Item ID", step=1)
        new_name = st.text_input("Enter Name")
        new_category = st.text_input("Enter Category")
        new_price = st.number_input("Enter Price", step=1.0)
        new_available = st.selectbox("Availability", ["Available", "Not Available"])

        if st.button("Add Item"):
            available_flag = True if new_available == "Available" else False
            menu_obj.items.append(MenuItem(new_id, new_name,
                                           new_category, new_price, available_flag))

            # Write to file
            with open("menu.txt", "w") as f:
                for it in menu_obj.items:
                    f.write(f"{it.item_id},{it.name},{it.category},{it.price},{1 if it.available else 0}\n")

            st.success("Item Added Successfully!")
            st.rerun()

        st.markdown("---")
        st.subheader("✏ Update Item Availability")

        update_id = st.number_input("Enter Item ID to Update", step=1)
        availability_choice = st.selectbox("Set Status", ["Available", "Not Available"])

        if st.button("Update Availability"):
            item_found = False
            for it in menu_obj.items:
                if it.item_id == update_id:
                    it.available = True if availability_choice == "Available" else False
                    item_found = True

            if item_found:
                with open("menu.txt", "w") as f:
                    for it in menu_obj.items:
                        f.write(f"{it.item_id},{it.name},{it.category},{it.price},{1 if it.available else 0}\n")

                st.success("Item availability updated!")
                st.rerun()
            else:
                st.error("Item ID not found!")

        if st.button("Logout"):
            st.session_state.admin_logged_in = False
            st.rerun()


# -------------------- PROCESS NEXT ORDER --------------------
elif page == "Process Next Order":
    st.header(" Process Next Order (Queue → Stack)")
    if st.button("Process Next"):
        order = queue_obj.dequeue()
        if order.get_order_id() == 0 or not order.items:
            st.error("No pending orders in queue.")
        else:
            order.set_status("Delivered")
            history_obj.push(order)
            st.success(f"Order #{order.get_order_id()} delivered.")
            st.code(order.bill_text())
            save_order_to_file(order)

# -------------------- PENDING ORDERS (QUEUE) --------------------
elif page == "Pending Orders (Queue)":
    st.header("Pending Orders (Queue)")
    orders = queue_obj.to_list()
    if not orders:
        st.info("No pending orders.")
    else:
        for o in orders:
            st.write(
                f"**Order #{o.get_order_id()}** | Customer: {o.get_customer_name()} | Total: Rs.{o.get_total_amount():.2f} | Status: {o.status}"
            )

# -------------------- DELIVERED ORDERS (STACK) --------------------
elif page == "Delivered Orders (Stack)":
    st.header(" Delivered Orders History (Stack)")
    orders = history_obj.to_list()
    if not orders:
        st.info("No delivered orders yet.")
    else:
        for o in orders:
            st.success(
                f"Delivered Order #{o.get_order_id()} | Customer: {o.get_customer_name()} | Rs.{o.get_total_amount():.2f}"
            )

# -------------------- UNDO LAST DELIVERY --------------------
elif page == "Undo Last Delivery":
    st.header("↩ Undo Last Delivery (Stack → Queue)")

    if st.button("Undo Last Delivered Order"):
        last = history_obj.pop()
        if last.get_order_id() == 0 or not last.items:
            st.error("No delivery history to undo.")
        else:
            last.set_status("Pending")
            queue_obj.enqueue(last)
            st.success(f"Order #{last.get_order_id()} restored to queue.")
