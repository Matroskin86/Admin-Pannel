import reflex as rx
from typing import TypedDict
import random
from datetime import datetime, timedelta


class Product(TypedDict):
    id: str
    name: str
    image: str
    price: float
    stock: int
    category: str
    status: str
    created_date: str


def _generate_sample_products() -> list[Product]:
    categories = ["Fragrance", "Skincare", "Makeup", "Hair Care", "Bath & Body"]
    base_products = [
        ("Chanel No. 5 Eau de Parfum", "chanel5", "Fragrance", 135.0),
        ("Dior Sauvage Elixir", "sauvage", "Fragrance", 155.0),
        ("YSL Black Opium", "yslblack", "Fragrance", 130.0),
        ("Estée Lauder Advanced Night Repair", "nightrepair", "Skincare", 105.0),
        ("La Mer Crème de la Mer", "lamer", "Skincare", 380.0),
        ("SK-II Facial Treatment Essence", "skii", "Skincare", 185.0),
        ("Fenty Beauty Pro Filt'r Foundation", "fentyfoundation", "Makeup", 39.0),
        ("Pat McGrath Mothership Palette", "pmglabs", "Makeup", 128.0),
        ("NARS Orgasm Blush", "narsblush", "Makeup", 32.0),
        ("Olaplex No. 3 Hair Perfector", "olaplex", "Hair Care", 30.0),
        ("Dyson Airwrap Multi-Styler", "dyson", "Hair Care", 599.0),
        ("Moroccanoil Treatment", "moroccanoil", "Hair Care", 44.0),
        ("Sol de Janeiro Bum Bum Cream", "bumbum", "Bath & Body", 48.0),
        ("L'Occitane Almond Shower Oil", "loccitane", "Bath & Body", 29.0),
        ("Jo Malone Lime Basil & Mandarin", "jomalone", "Fragrance", 145.0),
        ("Charlotte Tilbury Pillow Talk Lipstick", "pillowtalk", "Makeup", 34.0),
        ("Tatcha The Dewy Skin Cream", "tatcha", "Skincare", 69.0),
        ("Tom Ford Black Orchid", "tomford", "Fragrance", 150.0),
        ("Anastasia Beverly Hills Brow Wiz", "abhbrow", "Makeup", 23.0),
        ("Aesop Resurrection Hand Wash", "aesop", "Bath & Body", 40.0),
        ("Kerastase Elixir Ultime Oil", "kerastase", "Hair Care", 52.0),
        ("Urban Decay All Nighter Setting Spray", "urbandecay", "Makeup", 33.0),
        ("Sunday Riley Good Genes", "sundayriley", "Skincare", 85.0),
        (
            "Maison Francis Kurkdjian Baccarat Rouge 540",
            "baccarat540",
            "Fragrance",
            325.0,
        ),
    ]
    statuses = ["In Stock", "Low Stock", "Out of Stock"]
    products = []
    for i in range(40):
        base = base_products[i % len(base_products)]
        stock = random.randint(0, 150)
        status = "In Stock"
        if stock == 0:
            status = "Out of Stock"
        elif stock < 20:
            status = "Low Stock"
        products.append(
            {
                "id": f"{random.randint(10000000, 99999999)}-FE",
                "name": base[0],
                "image": f"https://api.dicebear.com/9.x/thumbs/svg?seed={base[1] + str(i)}",
                "price": base[3],
                "stock": stock,
                "category": base[2],
                "status": status,
                "created_date": (
                    datetime.now() - timedelta(days=random.randint(1, 365))
                ).strftime("%d %b %Y %I:%M %p"),
            }
        )
    return products


_initial_products = _generate_sample_products()


class ProductsState(rx.State):
    products: list[Product] = _initial_products
    selected_product_id: str = _initial_products[0]["id"] if _initial_products else ""
    search_query: str = ""
    page: int = 1
    items_per_page: int = 8
    is_add_modal_open: bool = False

    @rx.var
    def filtered_products(self) -> list[Product]:
        if not self.search_query:
            return self.products
        query = self.search_query.lower()
        return [
            p
            for p in self.products
            if query in p["name"].lower()
            or query in p["category"].lower()
            or query in p["id"].lower()
        ]

    @rx.var
    def total_items(self) -> int:
        return len(self.filtered_products)

    @rx.var
    def total_pages(self) -> int:
        return (self.total_items + self.items_per_page - 1) // self.items_per_page

    @rx.var
    def current_page_products(self) -> list[Product]:
        start = (self.page - 1) * self.items_per_page
        end = start + self.items_per_page
        return self.filtered_products[start:end]

    @rx.var
    def selected_product(self) -> Product:
        for p in self.products:
            if p["id"] == self.selected_product_id:
                return p
        return self.products[0] if self.products else {}

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
    def select_product(self, product_id: str):
        self.selected_product_id = product_id

    @rx.event
    def toggle_add_modal(self):
        self.is_add_modal_open = not self.is_add_modal_open

    @rx.event
    def add_product(self, form_data: dict):
        name = form_data.get("name", "")
        category = form_data.get("category", "")
        price = float(form_data.get("price", 0))
        stock = int(form_data.get("stock", 0))
        if not name:
            return rx.toast("Product name is required")
        new_product: Product = {
            "id": f"{random.randint(10000000, 99999999)}-FE",
            "name": name,
            "image": f"https://api.dicebear.com/9.x/thumbs/svg?seed={name}",
            "price": price,
            "stock": stock,
            "category": category,
            "status": "In Stock" if stock > 0 else "Out of Stock",
            "created_date": datetime.now().strftime("%d %b %Y %I:%M %p"),
        }
        self.products.insert(0, new_product)
        self.selected_product_id = new_product["id"]
        self.is_add_modal_open = False
        rx.toast("Product added successfully")

    @rx.event
    def update_product(self, form_data: dict):
        price = float(form_data.get("price", 0))
        stock = int(form_data.get("stock", 0))
        updated_list = []
        for p in self.products:
            if p["id"] == self.selected_product_id:
                updated_p = p.copy()
                updated_p["price"] = price
                updated_p["stock"] = stock
                updated_p["status"] = "In Stock" if stock > 0 else "Out of Stock"
                if stock < 20 and stock > 0:
                    updated_p["status"] = "Low Stock"
                updated_list.append(updated_p)
            else:
                updated_list.append(p)
        self.products = updated_list
        rx.toast("Product updated successfully")

    @rx.event
    def delete_product(self):
        self.products = [
            p for p in self.products if p["id"] != self.selected_product_id
        ]
        if self.products:
            self.selected_product_id = self.products[0]["id"]
        rx.toast("Product deleted")