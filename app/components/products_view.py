import reflex as rx
from app.states.products_state import ProductsState, Product


def product_status_badge(status: str) -> rx.Component:
    return rx.match(
        status,
        (
            "In Stock",
            rx.el.span(
                "In Stock",
                class_name="px-2.5 py-1 rounded-lg text-xs font-medium bg-green-50 text-green-700 w-fit border border-green-100",
            ),
        ),
        (
            "Low Stock",
            rx.el.span(
                "Low Stock",
                class_name="px-2.5 py-1 rounded-lg text-xs font-medium bg-orange-50 text-orange-700 w-fit border border-orange-100",
            ),
        ),
        (
            "Out of Stock",
            rx.el.span(
                "Out of Stock",
                class_name="px-2.5 py-1 rounded-lg text-xs font-medium bg-red-50 text-red-700 w-fit border border-red-100",
            ),
        ),
        rx.el.span(status),
    )


def product_row(product: Product) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.span(
                product["id"].split("-")[0],
                class_name="font-mono text-gray-400 text-xs",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.div(
                rx.image(
                    src=product["image"],
                    class_name="h-10 w-10 rounded-lg bg-gray-50 object-cover border border-gray-100",
                ),
                rx.el.span(
                    product["name"], class_name="font-medium text-gray-900 text-sm"
                ),
                class_name="flex items-center gap-3",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(
                product["category"], class_name="text-sm text-gray-500 font-medium"
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(
                f"${product['price']:.0f}",
                class_name="text-sm text-gray-900 font-semibold",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(
                product["stock"], class_name="text-sm text-gray-600 font-medium"
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            product_status_badge(product["status"]),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        on_click=lambda: ProductsState.select_product(product["id"]),
        class_name=rx.cond(
            ProductsState.selected_product_id == product["id"],
            "hover:bg-teal-50/80 bg-teal-50 cursor-pointer transition-colors border-l-4 border-teal-500",
            "hover:bg-gray-50 cursor-pointer transition-colors border-l-4 border-transparent",
        ),
    )


def products_pagination() -> rx.Component:
    return rx.el.div(
        rx.el.p(
            ProductsState.showing_text, class_name="text-sm text-gray-500 font-medium"
        ),
        rx.el.div(
            rx.el.button(
                "Previous",
                on_click=ProductsState.prev_page,
                disabled=ProductsState.page == 1,
                class_name="px-3 py-1 text-sm font-medium text-gray-600 hover:text-gray-900 disabled:opacity-50 disabled:cursor-not-allowed",
            ),
            rx.foreach(
                ProductsState.page_numbers,
                lambda p: rx.el.button(
                    p,
                    on_click=lambda: ProductsState.set_page(p),
                    class_name=rx.cond(
                        ProductsState.page == p,
                        "w-8 h-8 flex items-center justify-center rounded-lg bg-teal-600 text-white text-sm font-medium shadow-sm",
                        "w-8 h-8 flex items-center justify-center rounded-lg hover:bg-gray-100 text-gray-600 text-sm font-medium",
                    ),
                ),
            ),
            rx.el.button(
                "Next",
                on_click=ProductsState.next_page,
                disabled=ProductsState.page == ProductsState.total_pages,
                class_name="px-3 py-1 text-sm font-medium text-gray-600 hover:text-gray-900 disabled:opacity-50 disabled:cursor-not-allowed",
            ),
            class_name="flex items-center gap-2",
        ),
        class_name="flex items-center justify-between px-6 py-4 border-t border-gray-100",
    )


def products_table() -> rx.Component:
    return rx.el.div(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    rx.el.th(
                        "ID",
                        class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider w-16",
                    ),
                    rx.el.th(
                        "Product Name",
                        class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                    ),
                    rx.el.th(
                        "Category",
                        class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                    ),
                    rx.el.th(
                        "Price",
                        class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                    ),
                    rx.el.th(
                        "Quantity",
                        class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                    ),
                    rx.el.th(
                        "Status",
                        class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                    ),
                    class_name="bg-gray-50/50",
                )
            ),
            rx.el.tbody(
                rx.foreach(ProductsState.current_page_products, product_row),
                class_name="divide-y divide-gray-100 bg-white",
            ),
            class_name="min-w-full divide-y divide-gray-200",
        ),
        products_pagination(),
        class_name="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden flex flex-col justify-between h-full",
    )


def product_details_panel() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Product Details", class_name="text-lg font-bold text-gray-900 mb-6"
            ),
            rx.el.div(
                rx.image(
                    src=ProductsState.selected_product["image"],
                    class_name="h-24 w-24 rounded-xl bg-gray-50 object-cover border border-gray-100 shadow-sm",
                ),
                rx.el.div(
                    rx.el.p(
                        "Product Name :",
                        class_name="text-xs text-gray-400 font-medium mb-1",
                    ),
                    rx.el.h2(
                        ProductsState.selected_product["name"],
                        class_name="text-base font-bold text-gray-900 mb-2 leading-tight",
                    ),
                    rx.el.p(
                        f"ID : {ProductsState.selected_product['id']}",
                        class_name="text-xs font-mono text-gray-500 bg-gray-100 px-2 py-1 rounded w-fit",
                    ),
                    class_name="flex flex-col flex-1",
                ),
                class_name="flex items-start gap-4 mb-8 pb-8 border-b border-gray-100",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "dollar-sign", class_name="text-gray-400 mb-1", size=18
                        ),
                        rx.el.p(
                            "Unit Price",
                            class_name="text-xs text-gray-500 font-medium mb-1",
                        ),
                        rx.el.p(
                            f"${ProductsState.selected_product['price']:.2f}",
                            class_name="text-xl font-bold text-gray-900",
                        ),
                    ),
                    rx.el.div(class_name="w-px bg-gray-100 h-12 mx-2"),
                    rx.el.div(
                        rx.icon("package", class_name="text-gray-400 mb-1", size=18),
                        rx.el.p(
                            "Quantity",
                            class_name="text-xs text-gray-500 font-medium mb-1",
                        ),
                        rx.el.p(
                            ProductsState.selected_product["stock"],
                            class_name="text-xl font-bold text-gray-900",
                        ),
                    ),
                    class_name="flex items-center gap-6 mb-8",
                ),
                rx.el.div(
                    rx.icon("clock", class_name="text-gray-400 mr-2", size=16),
                    rx.el.span("Created At : ", class_name="text-gray-500"),
                    rx.el.span(
                        ProductsState.selected_product["created_date"],
                        class_name="text-gray-900 font-medium ml-1",
                    ),
                    class_name="flex items-center text-xs bg-gray-50 p-3 rounded-lg mb-8",
                ),
            ),
            rx.el.button(
                rx.icon("trash-2", size=16, class_name="mr-2"),
                "Delete Product",
                on_click=ProductsState.delete_product,
                class_name="flex items-center justify-center w-full py-2.5 text-red-600 hover:bg-red-50 bg-white border border-red-100 rounded-xl text-sm font-medium transition-colors mb-8",
            ),
        ),
        rx.el.div(
            rx.el.h4(
                "Update Quantity & Price",
                class_name="text-sm font-bold text-gray-900 mb-4",
            ),
            rx.el.form(
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Quantity",
                            class_name="block text-xs font-semibold text-gray-500 uppercase mb-2",
                        ),
                        rx.el.div(
                            rx.icon(
                                "package",
                                size=16,
                                class_name="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400",
                            ),
                            rx.el.input(
                                name="stock",
                                type="number",
                                default_value=ProductsState.selected_product["stock"],
                                key=f"stock-{ProductsState.selected_product_id}",
                                class_name="w-full pl-9 pr-4 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm font-medium focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 outline-none",
                            ),
                            class_name="relative",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Unit Price",
                            class_name="block text-xs font-semibold text-gray-500 uppercase mb-2",
                        ),
                        rx.el.div(
                            rx.icon(
                                "dollar-sign",
                                size=16,
                                class_name="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400",
                            ),
                            rx.el.input(
                                name="price",
                                type="number",
                                step="0.01",
                                default_value=ProductsState.selected_product["price"],
                                key=f"price-{ProductsState.selected_product_id}",
                                class_name="w-full pl-9 pr-4 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm font-medium focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 outline-none",
                            ),
                            class_name="relative",
                        ),
                        class_name="mb-6",
                    ),
                ),
                rx.el.button(
                    rx.icon("save", size=18, class_name="mr-2"),
                    "Save Changes",
                    type="submit",
                    class_name="w-full flex items-center justify-center py-2.5 bg-white border border-teal-600 text-teal-700 hover:bg-teal-50 font-medium rounded-xl transition-all shadow-sm",
                ),
                on_submit=ProductsState.update_product,
            ),
            class_name="border-t border-gray-100 pt-6",
        ),
        class_name="p-6 bg-white rounded-2xl shadow-sm border border-gray-100 h-full flex flex-col",
    )


def add_product_modal() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                "Add New Product", class_name="text-lg font-bold text-gray-900 mb-6"
            ),
            rx.el.form(
                rx.el.div(
                    rx.el.label(
                        "Product Name",
                        class_name="text-sm font-medium text-gray-700 mb-1 block",
                    ),
                    rx.el.input(
                        name="name",
                        placeholder="e.g. Wireless Headphones",
                        required=True,
                        class_name="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Category",
                        class_name="text-sm font-medium text-gray-700 mb-1 block",
                    ),
                    rx.el.select(
                        rx.el.option("Fragrance", value="Fragrance"),
                        rx.el.option("Skincare", value="Skincare"),
                        rx.el.option("Makeup", value="Makeup"),
                        rx.el.option("Hair Care", value="Hair Care"),
                        rx.el.option("Bath & Body", value="Bath & Body"),
                        name="category",
                        class_name="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Price ($)",
                            class_name="text-sm font-medium text-gray-700 mb-1 block",
                        ),
                        rx.el.input(
                            name="price",
                            type="number",
                            step="0.01",
                            placeholder="0.00",
                            required=True,
                            class_name="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent",
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Initial Stock",
                            class_name="text-sm font-medium text-gray-700 mb-1 block",
                        ),
                        rx.el.input(
                            name="stock",
                            type="number",
                            placeholder="0",
                            required=True,
                            class_name="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent",
                        ),
                    ),
                    class_name="grid grid-cols-2 gap-4 mb-6",
                ),
                rx.el.div(
                    rx.dialog.close(
                        rx.el.button(
                            "Cancel",
                            type="button",
                            class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 mr-2",
                        )
                    ),
                    rx.el.button(
                        "Add Product",
                        type="submit",
                        class_name="px-4 py-2 text-sm font-medium text-white bg-teal-600 rounded-lg hover:bg-teal-700 shadow-sm",
                    ),
                    class_name="flex justify-end",
                ),
                on_submit=ProductsState.add_product,
                reset_on_submit=True,
            ),
            class_name="bg-white p-6 rounded-2xl shadow-xl max-w-md w-full",
        ),
        open=ProductsState.is_add_modal_open,
        on_open_change=ProductsState.toggle_add_modal,
    )


def products_header() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                f"Products ({ProductsState.total_items})",
                class_name="text-2xl font-bold text-gray-900",
            ),
            rx.el.p(
                "Manage your product inventory and pricing.",
                class_name="text-gray-500 font-medium text-sm",
            ),
        ),
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "search",
                    class_name="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400",
                    size=18,
                ),
                rx.el.input(
                    placeholder="Search product...",
                    on_change=ProductsState.set_search,
                    class_name="pl-10 pr-4 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 outline-none w-64 transition-all",
                    default_value=ProductsState.search_query,
                ),
                class_name="relative",
            ),
            rx.el.button(
                rx.icon("plus", size=18),
                rx.el.span("Add Product"),
                on_click=ProductsState.toggle_add_modal,
                class_name="flex items-center gap-2 px-4 py-2 bg-teal-600 hover:bg-teal-700 text-white text-sm font-medium rounded-xl shadow-sm shadow-teal-200 transition-all active:scale-[0.98]",
            ),
            class_name="flex items-center gap-4",
        ),
        class_name="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6",
    )


def products_view() -> rx.Component:
    return rx.el.div(
        add_product_modal(),
        products_header(),
        rx.el.div(
            rx.el.div(
                products_table(), class_name="col-span-12 lg:col-span-8 flex flex-col"
            ),
            rx.el.div(
                rx.cond(
                    ProductsState.products,
                    product_details_panel(),
                    rx.el.div(
                        "No product selected",
                        class_name="flex items-center justify-center h-full text-gray-400 bg-white rounded-2xl border border-gray-100 p-8",
                    ),
                ),
                class_name="col-span-12 lg:col-span-4 h-fit",
            ),
            class_name="grid grid-cols-12 gap-6 items-start",
        ),
        class_name="p-6 sm:p-8 max-w-7xl mx-auto w-full",
    )