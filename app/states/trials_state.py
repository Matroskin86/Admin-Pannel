import reflex as rx
from typing import TypedDict
import random
from datetime import datetime, timedelta


class Trial(TypedDict):
    id: str
    customer_name: str
    product_name: str
    start_date: str
    end_date: str
    status: str
    image: str


def _generate_sample_trials() -> list[Trial]:
    products = [
        (
            "Chanel No. 5 Eau de Parfum",
            "https://api.dicebear.com/9.x/thumbs/svg?seed=chanel5",
        ),
        ("Dior Sauvage Elixir", "https://api.dicebear.com/9.x/thumbs/svg?seed=sauvage"),
        ("YSL Black Opium", "https://api.dicebear.com/9.x/thumbs/svg?seed=yslblack"),
        (
            "La Mer Crème de la Mer",
            "https://api.dicebear.com/9.x/thumbs/svg?seed=lamer",
        ),
        (
            "Fenty Beauty Pro Filt'r Foundation",
            "https://api.dicebear.com/9.x/thumbs/svg?seed=fentyfoundation",
        ),
        ("NARS Orgasm Blush", "https://api.dicebear.com/9.x/thumbs/svg?seed=narsblush"),
        (
            "Olaplex No. 3 Hair Perfector",
            "https://api.dicebear.com/9.x/thumbs/svg?seed=olaplex",
        ),
        (
            "Charlotte Tilbury Pillow Talk Lipstick",
            "https://api.dicebear.com/9.x/thumbs/svg?seed=pillowtalk",
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
    ]
    statuses = ["Active", "Expired", "Converted", "Pending"]
    customer_names = [
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
    ]
    trials = []
    for i in range(1, 46):
        prod = random.choice(products)
        customer = customer_names[i % len(customer_names)]
        start_date = datetime.now() - timedelta(days=random.randint(0, 30))
        duration = random.randint(7, 14)
        end_date = start_date + timedelta(days=duration)
        status = random.choice(statuses)
        if end_date < datetime.now() and status == "Active":
            status = "Expired"
        trials.append(
            {
                "id": f"TRL-{1000 + i}",
                "customer_name": customer,
                "product_name": prod[0],
                "image": prod[1],
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d"),
                "status": status,
            }
        )
    return trials


_initial_trials = _generate_sample_trials()


class TrialsState(rx.State):
    trials: list[Trial] = _initial_trials
    selected_trial_id: str = _initial_trials[0]["id"] if _initial_trials else ""
    search_query: str = ""
    page: int = 1
    items_per_page: int = 8
    is_add_modal_open: bool = False

    @rx.var
    def filtered_trials(self) -> list[Trial]:
        if not self.search_query:
            return self.trials
        query = self.search_query.lower()
        return [
            t
            for t in self.trials
            if query in t["customer_name"].lower()
            or query in t["product_name"].lower()
            or query in t["id"].lower()
        ]

    @rx.var
    def total_items(self) -> int:
        return len(self.filtered_trials)

    @rx.var
    def total_pages(self) -> int:
        return (self.total_items + self.items_per_page - 1) // self.items_per_page

    @rx.var
    def current_page_trials(self) -> list[Trial]:
        start = (self.page - 1) * self.items_per_page
        end = start + self.items_per_page
        return self.filtered_trials[start:end]

    @rx.var
    def selected_trial(self) -> Trial:
        for t in self.trials:
            if t["id"] == self.selected_trial_id:
                return t
        return self.trials[0] if self.trials else {}

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
    def select_trial(self, trial_id: str):
        self.selected_trial_id = trial_id

    @rx.event
    def toggle_add_modal(self):
        self.is_add_modal_open = not self.is_add_modal_open

    @rx.event
    def add_trial(self, form_data: dict):
        customer = form_data.get("customer_name", "")
        product = form_data.get("product_name", "")
        if not customer or not product:
            return rx.toast("Customer and Product are required")
        start_date = datetime.now()
        end_date = start_date + timedelta(days=14)
        new_trial: Trial = {
            "id": f"TRL-{random.randint(2000, 9999)}",
            "customer_name": customer,
            "product_name": product,
            "image": f"https://api.dicebear.com/9.x/thumbs/svg?seed={product}",
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "status": "Pending",
        }
        self.trials.insert(0, new_trial)
        self.selected_trial_id = new_trial["id"]
        self.is_add_modal_open = False
        rx.toast("Trial added successfully")

    @rx.event
    def update_trial(self, form_data: dict):
        status = form_data.get("status", "")
        updated_list = []
        for t in self.trials:
            if t["id"] == self.selected_trial_id:
                updated_t = t.copy()
                updated_t["status"] = status
                updated_list.append(updated_t)
            else:
                updated_list.append(t)
        self.trials = updated_list
        rx.toast("Trial updated successfully")

    @rx.event
    def delete_trial(self):
        self.trials = [t for t in self.trials if t["id"] != self.selected_trial_id]
        if self.trials:
            self.selected_trial_id = self.trials[0]["id"]
        rx.toast("Trial deleted")