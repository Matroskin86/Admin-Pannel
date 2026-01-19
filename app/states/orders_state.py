import reflex as rx
from typing import TypedDict, Optional
import random
from datetime import datetime, timedelta


class Order(TypedDict):
    id: str
    product_name: str
    image: str
    quantity: int
    price: float
    total: float
    status: str
    date: str
    customer_name: str
    customer_email: str


def _generate_sample_orders() -> list[Order]:
    products = [
        (
            "Chanel No. 5 Eau de Parfum",
            "https://api.dicebear.com/9.x/thumbs/svg?seed=chanel5",
        ),
        ("Dior Sauvage Elixir", "https://api.dicebear.com/9.x/thumbs/svg?seed=sauvage"),
        ("YSL Black Opium", "https://api.dicebear.com/9.x/thumbs/svg?seed=yslblack"),
        (
            "Fenty Beauty Pro Filt'r Foundation",
            "https://api.dicebear.com/9.x/thumbs/svg?seed=fentyfoundation",
        ),
        ("NARS Orgasm Blush", "https://api.dicebear.com/9.x/thumbs/svg?seed=narsblush"),
        (
            "La Mer Crème de la Mer",
            "https://api.dicebear.com/9.x/thumbs/svg?seed=lamer",
        ),
        (
            "Olaplex No. 3 Hair Perfector",
            "https://api.dicebear.com/9.x/thumbs/svg?seed=olaplex",
        ),
        (
            "Sol de Janeiro Bum Bum Cream",
            "https://api.dicebear.com/9.x/thumbs/svg?seed=bumbum",
        ),
        (
            "Dyson Airwrap Multi-Styler",
            "https://api.dicebear.com/9.x/thumbs/svg?seed=dyson",
        ),
        (
            "Maison Francis Kurkdjian Baccarat Rouge 540",
            "https://api.dicebear.com/9.x/thumbs/svg?seed=baccarat540",
        ),
        (
            "Estée Lauder Advanced Night Repair",
            "https://api.dicebear.com/9.x/thumbs/svg?seed=nightrepair",
        ),
        (
            "Charlotte Tilbury Pillow Talk Lipstick",
            "https://api.dicebear.com/9.x/thumbs/svg?seed=pillowtalk",
        ),
    ]
    statuses = ["Completed", "Pending", "Processing", "Refunded"]
    generated = []
    for i in range(1, 46):
        prod = products[i % len(products)]
        qty = random.randint(1, 5)
        price = round(random.uniform(25.0, 350.0), 2)
        order: Order = {
            "id": f"ORD-{1000 + i}",
            "product_name": prod[0],
            "image": prod[1],
            "quantity": qty,
            "price": price,
            "total": round(qty * price, 2),
            "status": statuses[i % len(statuses)],
            "date": (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d"),
            "customer_name": f"Customer {i}",
            "customer_email": f"customer{i}@example.com",
        }
        generated.append(order)
    return generated


_initial_orders = _generate_sample_orders()


class OrdersState(rx.State):
    orders: list[Order] = _initial_orders
    selected_order_id: str = _initial_orders[0]["id"] if _initial_orders else ""
    search_query: str = ""
    page: int = 1
    items_per_page: int = 8

    @rx.var
    def filtered_orders(self) -> list[Order]:
        if not self.search_query:
            return self.orders
        query = self.search_query.lower()
        return [
            o
            for o in self.orders
            if query in o["product_name"].lower()
            or query in o["id"].lower()
            or query in o["customer_name"].lower()
        ]

    @rx.var
    def total_items(self) -> int:
        return len(self.filtered_orders)

    @rx.var
    def total_pages(self) -> int:
        return (self.total_items + self.items_per_page - 1) // self.items_per_page

    @rx.var
    def current_page_orders(self) -> list[Order]:
        start = (self.page - 1) * self.items_per_page
        end = start + self.items_per_page
        return self.filtered_orders[start:end]

    @rx.var
    def selected_order(self) -> Order:
        for order in self.orders:
            if order["id"] == self.selected_order_id:
                return order
        return self.orders[0] if self.orders else {}

    @rx.var
    def showing_text(self) -> str:
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
    def select_order(self, order_id: str):
        self.selected_order_id = order_id

    @rx.event
    def delete_order(self):
        self.orders = [o for o in self.orders if o["id"] != self.selected_order_id]
        if self.orders:
            self.selected_order_id = self.orders[0]["id"]

    @rx.event
    def update_order(self, form_data: dict):
        new_qty = int(form_data.get("quantity", 0))
        new_price = float(form_data.get("price", 0))
        updated_orders = []
        for order in self.orders:
            if order["id"] == self.selected_order_id:
                updated_order = order.copy()
                updated_order["quantity"] = new_qty
                updated_order["price"] = new_price
                updated_order["total"] = round(new_qty * new_price, 2)
                updated_orders.append(updated_order)
            else:
                updated_orders.append(order)
        self.orders = updated_orders