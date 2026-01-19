import reflex as rx
from typing import TypedDict
import random
from datetime import datetime, timedelta


class Customer(TypedDict):
    id: str
    name: str
    email: str
    phone: str
    company: str
    avatar: str
    status: str
    created_date: str


def _generate_sample_customers() -> list[Customer]:
    names = [
        "Alice Smith",
        "Bob Johnson",
        "Carol Williams",
        "David Brown",
        "Eva Davis",
        "Frank Miller",
        "Grace Wilson",
        "Henry Moore",
        "Isabel Taylor",
        "Jack Anderson",
        "Kelly Thomas",
        "Liam Jackson",
        "Mia White",
        "Noah Harris",
        "Olivia Martin",
        "Peter Thompson",
        "Quinn Garcia",
        "Ryan Martinez",
        "Sophia Robinson",
        "Tyler Clark",
    ]
    companies = [
        "Acme Corp",
        "Globex",
        "Soylent Corp",
        "Initech",
        "Umbrella Corp",
        "Stark Ind",
        "Wayne Ent",
        "Cyberdyne",
    ]
    statuses = ["Active", "Inactive", "Pending", "VIP"]
    customers = []
    for i, name in enumerate(names):
        first_name = name.split(" ")[0]
        customers.append(
            {
                "id": f"CUST-{1000 + i}",
                "name": name,
                "email": f"{first_name.lower()}@example.com",
                "phone": f"+1 (555) {random.randint(100, 999)}-{random.randint(1000, 9999)}",
                "company": random.choice(companies),
                "avatar": f"https://api.dicebear.com/9.x/notionists/svg?seed={name}",
                "status": random.choice(statuses),
                "created_date": (
                    datetime.now() - timedelta(days=random.randint(1, 365))
                ).strftime("%Y-%m-%d"),
            }
        )
    return customers


_initial_customers = _generate_sample_customers()


class CustomersState(rx.State):
    customers: list[Customer] = _initial_customers
    selected_customer_id: str = (
        _initial_customers[0]["id"] if _initial_customers else ""
    )
    search_query: str = ""
    page: int = 1
    items_per_page: int = 7
    is_add_modal_open: bool = False

    @rx.var
    def filtered_customers(self) -> list[Customer]:
        if not self.search_query:
            return self.customers
        query = self.search_query.lower()
        return [
            c
            for c in self.customers
            if query in c["name"].lower()
            or query in c["email"].lower()
            or query in c["company"].lower()
        ]

    @rx.var
    def total_items(self) -> int:
        return len(self.filtered_customers)

    @rx.var
    def total_pages(self) -> int:
        return (self.total_items + self.items_per_page - 1) // self.items_per_page

    @rx.var
    def current_page_customers(self) -> list[Customer]:
        start = (self.page - 1) * self.items_per_page
        end = start + self.items_per_page
        return self.filtered_customers[start:end]

    @rx.var
    def selected_customer(self) -> Customer:
        for c in self.customers:
            if c["id"] == self.selected_customer_id:
                return c
        return self.customers[0] if self.customers else {}

    @rx.var
    def showing_text(self) -> str:
        if self.total_items == 0:
            return "No entries found"
        start = (self.page - 1) * self.items_per_page + 1
        end = min(start + self.items_per_page - 1, self.total_items)
        return f"Showing {start} - {end} from {self.total_items} entries"

    @rx.var
    def page_numbers(self) -> list[int]:
        return list(range(1, self.total_pages + 1))

    @rx.event
    def set_search(self, query: str):
        self.search_query = query
        self.page = 1

    @rx.event
    def set_page(self, page: int):
        self.page = page

    @rx.event
    def next_page(self):
        if self.page < self.total_pages:
            self.page += 1

    @rx.event
    def prev_page(self):
        if self.page > 1:
            self.page -= 1

    @rx.event
    def select_customer(self, customer_id: str):
        self.selected_customer_id = customer_id

    @rx.event
    def toggle_add_modal(self):
        self.is_add_modal_open = not self.is_add_modal_open

    @rx.event
    def add_customer(self, form_data: dict):
        name = form_data.get("name", "")
        email = form_data.get("email", "")
        if not name or not email:
            return rx.toast("Name and Email are required")
        new_customer: Customer = {
            "id": f"CUST-{random.randint(2000, 9999)}",
            "name": name,
            "email": email,
            "phone": form_data.get("phone", ""),
            "company": form_data.get("company", ""),
            "avatar": f"https://api.dicebear.com/9.x/notionists/svg?seed={name}",
            "status": "Active",
            "created_date": datetime.now().strftime("%Y-%m-%d"),
        }
        self.customers.insert(0, new_customer)
        self.is_add_modal_open = False
        self.selected_customer_id = new_customer["id"]
        rx.toast("Customer added successfully")

    @rx.event
    def update_customer(self, form_data: dict):
        updated_customers = []
        for c in self.customers:
            if c["id"] == self.selected_customer_id:
                updated_c = c.copy()
                updated_c.update(form_data)
                updated_customers.append(updated_c)
            else:
                updated_customers.append(c)
        self.customers = updated_customers
        rx.toast("Customer updated successfully")

    @rx.event
    def delete_customer(self):
        self.customers = [
            c for c in self.customers if c["id"] != self.selected_customer_id
        ]
        if self.customers:
            self.selected_customer_id = self.customers[0]["id"]
        rx.toast("Customer deleted")