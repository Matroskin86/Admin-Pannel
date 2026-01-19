import reflex as rx


class NavState(rx.State):
    active_item: str = "Customers"
    search_query: str = ""
    menu_items: list[dict[str, str]] = [
        {"label": "Customers", "icon": "users", "value": "customers"},
        {"label": "Orders", "icon": "shopping-cart", "value": "orders"},
        {"label": "Products", "icon": "package", "value": "products"},
        {"label": "Trials", "icon": "timer", "value": "trials"},
        {"label": "Coupons", "icon": "ticket", "value": "coupons"},
    ]

    @rx.event
    def set_active(self, item_label: str):
        self.active_item = item_label

    @rx.event
    async def set_search(self, query: str):
        self.search_query = query
        if self.active_item == "Customers":
            from app.states.customers_state import CustomersState

            state = await self.get_state(CustomersState)
            state.search_query = query
        elif self.active_item == "Orders":
            from app.states.orders_state import OrdersState

            state = await self.get_state(OrdersState)
            state.search_query = query
        elif self.active_item == "Products":
            from app.states.products_state import ProductsState

            state = await self.get_state(ProductsState)
            state.search_query = query
        elif self.active_item == "Trials":
            from app.states.trials_state import TrialsState

            state = await self.get_state(TrialsState)
            state.search_query = query
        elif self.active_item == "Coupons":
            from app.states.coupons_state import CouponsState

            state = await self.get_state(CouponsState)
            state.search_query = query