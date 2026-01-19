import reflex as rx
from typing import TypedDict
import random
from datetime import datetime, timedelta


class Coupon(TypedDict):
    code: str
    type: str
    value: float
    used: int
    limit: int
    expiry_date: str
    status: str


def _generate_sample_coupons() -> list[Coupon]:
    codes = [
        "BEAUTY20",
        "GLOW15",
        "SKINCARE10",
        "FRAGRANCE25",
        "LUXE50",
        "MAKEUP15",
        "HAIRCARE10",
        "FIRSTORDER",
        "VIPBEAUTY",
        "SUMMERGLOW",
        "HOLIDAYSCENT",
        "FREESHIP",
        "BDAYTREAT",
        "LOYALTY20",
    ]
    types = ["Percentage", "Fixed Amount"]
    statuses = ["Active", "Expired", "Exhausted"]
    coupons = []
    for i in range(25):
        code_base = codes[i % len(codes)]
        suffix = "" if i < len(codes) else str(random.randint(10, 99))
        code = f"{code_base}{suffix}"
        ctype = random.choice(types)
        value = (
            random.randint(5, 40) if ctype == "Percentage" else random.randint(10, 100)
        )
        limit = random.randint(50, 500)
        used = random.randint(0, limit)
        status = "Active"
        expiry = datetime.now() + timedelta(days=random.randint(-60, 120))
        if expiry < datetime.now():
            status = "Expired"
        elif used >= limit:
            status = "Exhausted"
        coupons.append(
            {
                "code": code,
                "type": ctype,
                "value": float(value),
                "used": used,
                "limit": limit,
                "expiry_date": expiry.strftime("%Y-%m-%d"),
                "status": status,
            }
        )
    return coupons


_initial_coupons = _generate_sample_coupons()


class CouponsState(rx.State):
    coupons: list[Coupon] = _initial_coupons
    selected_code: str = _initial_coupons[0]["code"] if _initial_coupons else ""
    search_query: str = ""
    page: int = 1
    items_per_page: int = 8
    is_add_modal_open: bool = False

    @rx.var
    def filtered_coupons(self) -> list[Coupon]:
        if not self.search_query:
            return self.coupons
        query = self.search_query.lower()
        return [c for c in self.coupons if query in c["code"].lower()]

    @rx.var
    def total_items(self) -> int:
        return len(self.filtered_coupons)

    @rx.var
    def total_pages(self) -> int:
        return (self.total_items + self.items_per_page - 1) // self.items_per_page

    @rx.var
    def current_page_coupons(self) -> list[Coupon]:
        start = (self.page - 1) * self.items_per_page
        end = start + self.items_per_page
        return self.filtered_coupons[start:end]

    @rx.var
    def selected_coupon(self) -> Coupon:
        for c in self.coupons:
            if c["code"] == self.selected_code:
                return c
        return self.coupons[0] if self.coupons else {}

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
    def select_coupon(self, code: str):
        self.selected_code = code

    @rx.event
    def toggle_add_modal(self):
        self.is_add_modal_open = not self.is_add_modal_open

    @rx.event
    def add_coupon(self, form_data: dict):
        code = form_data.get("code", "").upper()
        if not code:
            return rx.toast("Coupon Code is required")
        limit = int(form_data.get("limit", 100))
        value = float(form_data.get("value", 0))
        new_coupon: Coupon = {
            "code": code,
            "type": form_data.get("type", "Percentage"),
            "value": value,
            "used": 0,
            "limit": limit,
            "expiry_date": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
            "status": "Active",
        }
        self.coupons.insert(0, new_coupon)
        self.selected_code = new_coupon["code"]
        self.is_add_modal_open = False
        rx.toast("Coupon added successfully")

    @rx.event
    def update_coupon(self, form_data: dict):
        limit = int(form_data.get("limit", 0))
        expiry = form_data.get("expiry_date", "")
        updated_list = []
        for c in self.coupons:
            if c["code"] == self.selected_code:
                updated_c = c.copy()
                updated_c["limit"] = limit
                updated_c["expiry_date"] = expiry
                updated_list.append(updated_c)
            else:
                updated_list.append(c)
        self.coupons = updated_list
        rx.toast("Coupon updated successfully")

    @rx.event
    def delete_coupon(self):
        self.coupons = [c for c in self.coupons if c["code"] != self.selected_code]
        if self.coupons:
            self.selected_code = self.coupons[0]["code"]
        rx.toast("Coupon deleted")